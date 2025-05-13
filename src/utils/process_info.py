import psutil
from dataclasses import dataclass
from typing import List

@dataclass
class ProcessInfo:
    pid: int
    name: str
    status: str
    cpu_percent: float
    memory_percent: float

def get_active_processes() -> List[ProcessInfo]:
    """
    Recupera información de los procesos activos.

    Devuelve una lista de ProcessInfo, ordenada de mayor a menor uso de CPU.
    Captura procesos que desaparecen o a los que no tiene acceso.
    """
    processes: List[ProcessInfo] = []
    # Primer paso: psutil.cache_cpu_percent() al inicio del programa para mediciones más fiables
    psutil.cpu_percent(interval=None)

    for proc in psutil.process_iter(['pid', 'name', 'status']):
        try:
            info = proc.info
            # Medimos CPU y RAM
            cpu = proc.cpu_percent(interval=0.1)
            mem = proc.memory_percent()
            processes.append(ProcessInfo(
                pid=info['pid'],
                name=info['name'] or '',
                status=info['status'],
                cpu_percent=cpu,
                memory_percent=mem
            ))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            # El proceso finalizó o no tenemos permisos; lo ignoramos
            continue

    # Ordenar de mayor a menor uso de CPU
    processes.sort(key=lambda p: p.cpu_percent, reverse=True)
    return processes
