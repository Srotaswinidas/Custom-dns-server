# Custom DNS Server using Python

## Project Overview

This project implements a custom Domain Name System (DNS) server using Python and UDP socket programming. The server resolves domain names into IP addresses using a combination of local DNS records, a caching mechanism with Time-To-Live (TTL), and forwarding to an external DNS server (Google DNS).

The project demonstrates core networking concepts such as socket communication, protocol handling, caching, and concurrent request handling.

---

## Objectives

* Understand low-level UDP socket programming
* Implement DNS query and response handling
* Design a system with caching and forwarding
* Support multiple concurrent clients using threading
* Evaluate system performance under multiple requests

---

## System Architecture

Client → Custom DNS Server → External DNS Server (8.8.8.8)
↑                      ↓
←────────── Response ──────────

### Description

1. The client sends a DNS query to the server
2. The server checks the cache
3. If not found, it checks the local DNS table
4. If still not found, it forwards the request to an external DNS server
5. The response is returned to the client
6. The result is stored in cache for future queries

---

## Features

* Local DNS resolution using predefined records
* DNS caching with TTL
* Forwarding to external DNS server
* UDP-based communication
* Multi-client support using threading
* Basic error handling

---

## Technologies Used

* Python 3
* Socket Programming (UDP)
* Threading


---


## How to Run

### Step 1: Start the DNS Server

```bash
py server.py
```

Expected output:
DNS Server running on port 5354

---

### Step 2: Run the Client

```bash
py client.py
```

Enter a domain name when prompted.

---


## Sample Execution

Example server output:

Query: example.com
Resolved locally

Query: google.com
Forwarding
Stored in cache: 142.250.x.x

Query: google.com
Cache HIT

---

## How It Works

1. The server listens for incoming UDP DNS queries
2. The domain name is extracted from the request packet
3. The server checks:

   * Cache
   * Local DNS table
4. If not found, the query is forwarded to an external DNS server
5. The response is received and processed
6. The result is cached for future use
7. The response is sent back to the client

---

## Performance Evaluation

The system was tested under multiple scenarios:

* Single client requests
* Multiple concurrent clients using threading
* Repeated queries to observe caching

Observations:

* Forwarded queries take higher time due to external DNS lookup
* Cached queries are significantly faster
* The server successfully handles multiple client requests concurrently

---

## Limitations

* Supports only IPv4 (A records)
* Simplified DNS packet parsing
* No SSL/TLS security implemented
* Uses UDP, which does not support direct SSL/TLS integration

---

## Future Improvements

* Implement DNS over TLS (DoT) using TCP for secure communication
* Improve DNS packet parsing for broader compatibility
* Add support for IPv6 (AAAA records)
* Enhance performance monitoring with detailed metrics
* Develop a graphical interface for monitoring queries

---

