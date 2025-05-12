import socket

def scan_open_ports(start_port=1, end_port=1024, timeout=0.2):
    open_ports = []
    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                result = sock.connect_ex(('127.0.0.1', port))
                if result == 0:
                    try:
                        service = socket.getservbyport(port)
                    except OSError:
                        service = "Unknown"
                    open_ports.append((port, service))
        except socket.error:
            continue
    return open_ports
