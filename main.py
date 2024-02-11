from info import get_server_info
import concurrent.futures
import socket
import signal
import sys

def scan_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)

    try:
        sock.connect((host, port))

        request = b"GET / HTTP/1.1\r\nHost: " + host.encode() + b"\r\n\r\n"
        sock.sendall(request)

        response = sock.recv(1024).decode('utf-8')
        return port, get_server_info(response)

    except socket.error:
        return None
    finally:
        sock.close()

def scan_ports(host, start_port, end_port, max_threads=100):
    open_ports = []

    with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
        futures = {executor.submit(scan_port, host, port): port for port in range(start_port, end_port + 1)}

        try:
            for future in concurrent.futures.as_completed(futures):
                port = futures[future]
                try:
                    result = future.result()
                    if result is not None:
                        open_ports.append(result)
                        print(f"Port {result[0]} is open. Server type: {result[1]}")
                except Exception as e:
                    print(f"Error scanning port {port}: {e}")

        except KeyboardInterrupt:
            print("Scan interrupted by user (Ctrl+C). Stopping...")
            sys.exit()

    return open_ports

if __name__ == "__main__":
    target_host = input("Enter the target host IP or hostname: ")
    start_port = 0
    end_port = 65535

    print(f"Scanning ports on {target_host} from {start_port} to {end_port}")
    open_ports = scan_ports(target_host, start_port, end_port)

    if open_ports:
        print("Open ports:", open_ports)
    else:
        print("No open ports found.")