import subprocess
import re
import socket

def scan_open_ports():
    """
    Devuelve una lista de tuplas (protocolo, puerto, servicio) para
    todos los puertos TCP en LISTENING y puertos UDP abiertos.
    """
    open_ports = []
    # Llamada a netstat -an para Windows
    result = subprocess.run(
        ["netstat", "-an"],
        capture_output=True,
        text=True,
        shell=True  # necesario en Windows
    )
    # Regex para líneas TCP LISTENING
    tcp_re = re.compile(r"^ *TCP +[\d\.\[\]]+:(\d+) +[\d\.\[\]]+:[\d\*]+ +LISTENING", re.IGNORECASE)
    # Regex para líneas UDP (no tienen “LISTENING”)
    udp_re = re.compile(r"^ *UDP +[\d\.\[\]]+:(\d+)", re.IGNORECASE)

    for line in result.stdout.splitlines():
        tcp_m = tcp_re.match(line)
        if tcp_m:
            port = int(tcp_m.group(1))
            try:
                service = socket.getservbyport(port, "tcp")
            except OSError:
                service = "Unknown"
            open_ports.append(("TCP", port, service))
            continue

        udp_m = udp_re.match(line)
        if udp_m:
            port = int(udp_m.group(1))
            try:
                service = socket.getservbyport(port, "udp")
            except OSError:
                service = "Unknown"
            open_ports.append(("UDP", port, service))

    return sorted(open_ports, key=lambda x: (x[0], x[1]))



