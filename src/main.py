# src/main.py

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.status import Status
from pyfiglet import figlet_format

import os
import time
import psutil

from utils.os_info import get_os_version
from utils.process_info import procesos
from utils.puertoscan import Scan_puertos
from utils.usorecursos import usorecursos
from utils.evaluacion import evaluacion
from utils.appinst import apps

console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_banner():
    # Banner original
    banner = figlet_format("U-AASIGN", font="slant")
    console.print(f"[bold cyan]{banner}[/bold cyan]")


def show_menu():
    clear_screen()
    show_banner()
    console.print(Panel("[bold]Sistema de Evaluación de Seguridad[/bold]",
                        title="🐓 Menú Principal", width=50))
    console.print("[yellow]1.[/yellow] Ver versión del sistema operativo")
    console.print("[yellow]2.[/yellow] Ver procesos activos")
    console.print("[yellow]3.[/yellow] Escanear puertos abiertos")
    console.print("[yellow]4.[/yellow] Ver uso de recursos")
    console.print("[yellow]5.[/yellow] Evaluar seguridad del sistema")
    console.print("[yellow]6.[/yellow] Ver aplicaciones instaladas")
    console.print("[yellow]0.[/yellow] Salir")


def main():
    while True:
        show_menu()
        choice = Prompt.ask(
            "\n[bold white]Selecciona una opción[/bold white]",
            choices=["1", "2", "3", "4", "5", "6", "0"]
        )

        if choice == "1":
            clear_screen()
            show_banner()
            with console.status("[green]Obteniendo versión del sistema..."):
                os_version = get_os_version()
                time.sleep(0.5)
            console.print(Panel(f"[cyan]{os_version}[/cyan]", title="Versión del sistema"))
            input("\nPresiona Enter para volver al menú...")

        elif choice == "2":
            clear_screen()
            show_banner()
            with console.status("[green]Obteniendo procesos activos..."):
                processes = procesos()
                time.sleep(0.5)

            if processes:
                # Pedir filtro de sistema
                if Prompt.ask("[bold yellow]¿Omitir procesos de sistema? (s/n)[/bold yellow]", choices=["s","n"], default="s") == "s":
                    system_users = ("root", "SYSTEM", "LocalService", "NetworkService")
                    processes = [
                        p for p in processes
                        if p.user not in system_users
                        and not (p.name.startswith("[") and p.name.endswith("]"))
                        and p.pid > 100
                    ]

                # Ahora ordenas e imprimes esos procesos filtrados
                processes.sort(key=lambda p: p.cpu_percent, reverse=True)
                console.print("[yellow]🔍 Listado de todos los procesos activos con métricas detalladas:[/yellow]\n")
                # Ordenar descendente por uso de CPU
                processes.sort(key=lambda p: p.cpu_percent, reverse=True)

                table = Table(title="[bold cyan]Procesos Activos[/bold cyan]")
                # Columnas con colores
                table.add_column("#", style="bold yellow", justify="right")
                table.add_column("PID", style="bold magenta", justify="right")
                table.add_column("Usuario", style="bold green")
                table.add_column("Nombre", style="bold white")
                table.add_column("% CPU", style="bold red", justify="right")
                table.add_column("% RAM", style="bold blue", justify="right")
                table.add_column("Hilos", style="bold cyan", justify="right")
                table.add_column("I/O KiB L/E", style="bold green", justify="right")
                table.add_column("Conexiones", style="bold magenta", justify="right")
                table.add_column("Inicio", style="bold white")

                for idx, p in enumerate(processes, 1):
                    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(p.create_time))
                    io_vals = f"{p.io_read_bytes//1024}/{p.io_write_bytes//1024}"
                    table.add_row(
                        str(idx),
                        str(p.pid),
                        p.user,
                        p.name,
                        f"{p.cpu_percent:.1f}",
                        f"{p.memory_percent:.1f}",
                        str(p.num_threads),
                        io_vals,
                        str(p.net_connections),
                        start_time
                    )
                console.print(table)

                if Prompt.ask("[bold yellow]¿Terminar algún proceso sospechoso? (s/n)[/bold yellow]", choices=["s","n"], default="n") == "s":
                    sel = IntPrompt.ask(
                        "[bold magenta]Selecciona # de proceso para terminar[/bold magenta]"
                    )
                    target = processes[int(sel)-1]
                    try:
                        psutil.Process(target.pid).terminate()
                        console.print(f"[bold green]✔ Proceso PID {target.pid} ('{target.name}') terminado correctamente.[/bold green]")
                    except psutil.NoSuchProcess:
                        console.print(f"[bold red]✖ El proceso {target.pid} ya no existe.[/bold red]")
                    except psutil.AccessDenied:
                        console.print(f"[bold red]✖ Permiso denegado al terminar proceso {target.pid}.[/bold red]")
            else:
                console.print("[bold red]No se encontraron procesos activos.[/bold red]")

            input("\nPresiona Enter para volver al menú...")

        elif choice == "3":
            clear_screen()
            show_banner()
            with console.status("[green]Escaneando puertos abiertos..."):
                ports = Scan_puertos()
                time.sleep(0.5)
            if ports:
                table = Table(title="Puertos Abiertos")
                table.add_column("Protocolo", style="bold cyan", justify="center")
                table.add_column("Puerto", style="bold yellow", justify="right")
                table.add_column("Servicio", style="bold white")
                for proto, port, serv in ports:
                    table.add_row(proto, str(port), serv)
                console.print(table)
            else:
                console.print("[bold red]No se encontraron puertos abiertos.[/bold red]")
            input("\nPresiona Enter para volver al menú...")

        elif choice == "4":
            clear_screen()
            show_banner()
            with console.status("[green]Obteniendo uso de recursos..."):
                usage = usorecursos()
                time.sleep(0.5)
            console.print(f"[bold green]CPU:[/bold green] {usage['cpu_usage']}%")
            console.print(f"[bold green]RAM:[/bold green] {usage['ram_usage']}%")
            input("\nPresiona Enter para volver al menú...")

        elif choice == "5":
            clear_screen()
            show_banner()
            with console.status("[green]Evaluando seguridad..."):
                report = evaluacion()
                time.sleep(0.5)
            console.print(Panel(report, title="Evaluación del sistema", subtitle="🏁"))
            input("\nPresiona Enter para volver al menú...")

        elif choice == "6":
            clear_screen()
            show_banner()
            with console.status("[green]Obteniendo aplicaciones instaladas..."):
                aplicaciones = apps()
                time.sleep(0.5)
            table = Table(title="Aplicaciones Instaladas")
            table.add_column("#", style="bold yellow", justify="right")
            table.add_column("Nombre", style="bold white")
            table.add_column("Versión", style="bold green")
            for idx, (name, ver) in enumerate(aplicaciones,1):
                table.add_row(str(idx), name, ver)
            console.print(table)
            if len(aplicaciones) > 30:
                console.print(f"[bold yellow]Mostrando 30 de {len(aplicaciones)} aplicaciones...[/bold yellow]")
            input("\nPresiona Enter para volver al menú...")

        elif choice == "0":
            console.print("[bold red]Saliendo... Hasta luego![/bold red]")
            break


if __name__ == "__main__":
    main()
