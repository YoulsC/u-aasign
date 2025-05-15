import subprocess
import re
import socket

def Scan_puertos():
   
    puertos_abiertos = []
   
    resultado = subprocess.run(
        ["netstat", "-an"],
        capture_output=True,
        text=True,
        shell=True 
    )
    # Regex LISTENING
    regex_tcp = re.compile(r"^ *TCP +[\d\.\[\]]+:(\d+) +[\d\.\[\]]+:[\d\*]+ +LISTENING", re.IGNORECASE)
    # (no tienen “LISTENING”)
    regex_udp = re.compile(r"^ *UDP +[\d\.\[\]]+:(\d+)", re.IGNORECASE)

    for linea in resultado.stdout.splitlines():
        coincidencia_tcp = regex_tcp.match(linea)
        if coincidencia_tcp:
            puerto = int(coincidencia_tcp.group(1))
            try:
                servicio = socket.getservbyport(puerto, "tcp")
            except OSError:
                servicio = "Desconocido"
            puertos_abiertos.append(("TCP", puerto, servicio))
            continue

        coincidencia_udp = regex_udp.match(linea)
        if coincidencia_udp:
            puerto = int(coincidencia_udp.group(1))
            try:
                servicio = socket.getservbyport(puerto, "udp")
            except OSError:
                servicio = "Desconocido"
            puertos_abiertos.append(("UDP", puerto, servicio))

    return sorted(puertos_abiertos, key=lambda x: (x[0], x[1]))



