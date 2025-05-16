
import psutil
import time
from dataclasses import dataclass
from typing import List

@dataclass
class ProcessInfo:
    pid: int
    name: str
    user: str
    status: str
    cpu_percent: float
    memory_percent: float
    create_time: float
    num_threads: int
    io_read_bytes: int
    io_write_bytes: int
    net_connections: int
    cmdline: str

def procesos() -> List[ProcessInfo]:
    interval = 0.1
    for proc in psutil.process_iter(['pid']):
        try: proc.cpu_percent(None)
        except (psutil.NoSuchProcess, psutil.AccessDenied): pass

    time.sleep(interval)
    resultados: List[ProcessInfo] = []

    for proc in psutil.process_iter([
            'pid', 'name', 'username', 'status',
            'cpu_percent', 'memory_percent',
            'create_time', 'num_threads', 'io_counters', 'cmdline'
        ]):
        try:
            info = proc.info
            io = info.get('io_counters')
            # Contamos conexiones de red (inet)
            try:
                conns = proc.connections(kind='inet')
                net_count = len(conns)
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                net_count = 0

            resultados.append(ProcessInfo(
                pid=info['pid'],
                name=info['name'] or '',
                user=info['username'] or '',
                status=info['status'],
                cpu_percent=info['cpu_percent'],
                memory_percent=info['memory_percent'],
                create_time=info['create_time'],
                num_threads=info['num_threads'],
                io_read_bytes=io.read_bytes if io else 0,
                io_write_bytes=io.write_bytes if io else 0,
                net_connections=net_count,
                cmdline=' '.join(info.get('cmdline') or [])
            ))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    resultados.sort(key=lambda p: p.cpu_percent, reverse=True)
    return resultados
