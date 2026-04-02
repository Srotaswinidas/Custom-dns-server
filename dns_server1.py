import socket
import time
import threading

dns_table = {
    "example.com": "93.184.216.34",
    "mywebsite.com": "192.168.1.10",
    "test.com": "1.2.3.4",
    "localserver.com": "10.0.0.5",
    "college.edu": "172.16.0.1",
    "lab.local": "127.0.0.1",
    "intranet.company": "192.168.0.100"
}

cache = {}
TTL = 60


def extract_domain(data):
    domain = ""
    i = 12
    while True:
        length = data[i]
        if length == 0:
            break
        i += 1
        domain += data[i:i+length].decode() + "."
        i += length
    return domain[:-1]


def build_response(data, ip):
    transaction_id = data[:2]
    flags = b'\x81\x80'
    qdcount = b'\x00\x01'
    ancount = b'\x00\x01'
    nscount = b'\x00\x00'
    arcount = b'\x00\x00'

    header = transaction_id + flags + qdcount + ancount + nscount + arcount
    query = data[12:]

    answer = b'\xc0\x0c'
    answer += b'\x00\x01'
    answer += b'\x00\x01'
    answer += b'\x00\x00\x00\x3c'
    answer += b'\x00\x04'
    answer += socket.inet_aton(ip)

    return header + query + answer


def forward_query(data):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)
        sock.sendto(data, ("8.8.8.8", 53))
        response, _ = sock.recvfrom(512)
        return response
    except:
        return None


def extract_ip(response):
    try:
        return socket.inet_ntoa(response[-4:])
    except:
        return None


def handle_client(data, addr, server_socket):
    try:
        start = time.time()   # START TIMER

        if len(data) < 12:
            return

        domain = extract_domain(data)
        print("Query:", domain)

        response = None

        # Cache check
        if domain in cache:
            ip, timestamp = cache[domain]
            if time.time() - timestamp < TTL:
                print("Cache HIT")
                response = build_response(data, ip)
            else:
                del cache[domain]

        # Local DNS table
        if response is None and domain in dns_table:
            print("Resolved locally")
            ip = dns_table[domain]
            response = build_response(data, ip)

        # Forwarding
        if response is None:
            print("Forwarding")
            forwarded = forward_query(data)

            if forwarded:
                ip = extract_ip(forwarded)
                if ip:
                    cache[domain] = (ip, time.time())
                    print("Stored in cache:", ip)
                response = forwarded
            else:
                return

        server_socket.sendto(response, addr)

        end = time.time()   # END TIMER
        print("Response Time:", round((end - start)*1000, 2), "ms\n")

    except Exception as e:
        print("Error:", e)


def start_dns_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("0.0.0.0", 5354))

    print("DNS Server running on port 5354\n")

    while True:
        try:
            data, addr = server_socket.recvfrom(512)

            thread = threading.Thread(
                target=handle_client,
                args=(data, addr, server_socket)
            )
            thread.start()

        except Exception as e:
            print("Error:", e)


start_dns_server()
