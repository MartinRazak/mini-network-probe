import socket
import time

def test_host(host):
    print(f"\nTesting: {host}")

    try:
        ip = socket.gethostbyname(host)
        print(f"DNS result: {host} → {ip}")
    except socket.gaierror:
        print("DNS failed")
        return

    port = 443
    start = time.time()

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((ip, port))
        end = time.time()

        print(f"TCP connection to port {port}: SUCCESS")
        print(f"Latency (TCP connect time): {(end - start)*1000:.2f} ms")

        sock.close()

    except Exception as e:
        print(f"Connection failed: {e}")


# enter the domain name of the website you wish to test, I use github.com as an example
test_host("github.com")