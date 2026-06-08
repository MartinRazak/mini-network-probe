import socket
import ssl
import time
from urllib.parse import urlparse


def test_host(host, port=443):
    print("=" * 60)
    print(f"Testing: {host}")
    print("=" * 60)

    try:
        start_dns = time.perf_counter()

        addr_info = socket.getaddrinfo(
            host,
            port,
            proto=socket.IPPROTO_TCP
        )

        dns_time = (time.perf_counter() - start_dns) * 1000

        ips = sorted(set(item[4][0] for item in addr_info))

        print(f"DNS Resolution: SUCCESS ({dns_time:.2f} ms)")
        for ip in ips:
            print(f"  └─ {ip}")

    except socket.gaierror as e:
        print(f"DNS Resolution: FAILED ({e})")
        return

    try:
        start_tcp = time.perf_counter()

        sock = socket.create_connection(
            (host, port),
            timeout=5
        )

        tcp_time = (time.perf_counter() - start_tcp) * 1000

        print(f"\nTCP Connection ({port}): SUCCESS")
        print(f"TCP Latency: {tcp_time:.2f} ms")

    except Exception as e:
        print(f"\nTCP Connection ({port}): FAILED")
        print(f"Reason: {e}")
        return

    try:
        context = ssl.create_default_context()

        start_tls = time.perf_counter()

        tls_sock = context.wrap_socket(
            sock,
            server_hostname=host
        )

        tls_time = (time.perf_counter() - start_tls) * 1000

        cert = tls_sock.getpeercert()

        print(f"\nTLS Handshake: SUCCESS")
        print(f"TLS Time: {tls_time:.2f} ms")
        print(f"TLS Version: {tls_sock.version()}")

        if cert:
            subject = dict(x[0] for x in cert["subject"])
            print(
                f"Certificate CN: "
                f"{subject.get('commonName', 'Unknown')}"
            )

    except Exception as e:
        print("\nTLS Handshake: FAILED")
        print(f"Reason: {e}")
        return

    # HTTP Test
    try:
        request = (
            f"HEAD / HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            f"Connection: close\r\n\r\n"
        )

        start_http = time.perf_counter()

        tls_sock.sendall(request.encode())

        response = tls_sock.recv(4096).decode(
            errors="ignore"
        )

        http_time = (time.perf_counter() - start_http) * 1000

        first_line = response.splitlines()[0]

        print("\nHTTP Response: SUCCESS")
        print(f"Response Time: {http_time:.2f} ms")
        print(f"Status: {first_line}")

    except Exception as e:
        print("\nHTTP Test: FAILED")
        print(f"Reason: {e}")

    finally:
        try:
            tls_sock.close()
        except:
            pass


if __name__ == "__main__":
    hosts = [
        "github.com",
        "google.com",
        "cloudflare.com"
    ]

    for host in hosts:
        test_host(host)