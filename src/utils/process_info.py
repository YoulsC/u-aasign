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

def procesos() -> List[ProcessInfo]:
   
    processes: List[ProcessInfo] = []
   
    psutil.cpu_percent(interval=None)

    for proc in psutil.process_iter(['pid', 'name', 'status']):
        try:
            info = proc.info
          
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
           
            continue


    processes.sort(key=lambda p: p.cpu_percent, reverse=True)
    return processes
