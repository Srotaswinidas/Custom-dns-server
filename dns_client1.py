import socket
import random

def build_query(domain):
    transaction_id = random.randint(0, 65535).to_bytes(2, 'big')
    flags = b'\x01\x00'
    qdcount = b'\x00\x01'
    ancount = b'\x00\x00'
    nscount = b'\x00\x00'
    arcount = b'\x00\x00'

    header = transaction_id + flags + qdcount + ancount + nscount + arcount

    query = b''
    for part in domain.split('.'):
        query += bytes([len(part)]) + part.encode()
    query += b'\x00'

    query += b'\x00\x01'
    query += b'\x00\x01'

    return header + query

def extract_ip(response):
    try:
        return socket.inet_ntoa(response[-4:])
    except:
        return "Unknown"

def send_query(domain):
    server = ("127.0.0.1", 5354)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3)

    try:
        query = build_query(domain)
        sock.sendto(query, server)

        response, _ = sock.recvfrom(512)
        ip = extract_ip(response)

        print(domain, "->", ip)

    except socket.timeout:
        print("Request timed out")

while True:
    domain = input("Enter domain (or 'exit'): ")

    if domain.lower() == "exit":
        break

    if domain.strip() == "":
        continue

    send_query(domain)
