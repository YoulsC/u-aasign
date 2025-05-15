# src/main.py

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.status import Status
from pyfiglet import figlet_format

import os
import time
import subprocess

from utils.os_info import get_os_version
from utils.process_info import procesos
from utils.puertoscan import Scan_puertos
from utils.usorecursos import usorecursos
from utils.evaluacion import evaluacion
from utils.appinst import apps
from utils.actividad import procssact

console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
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
                table = Table(title="Procesos Activos")
                table.add_column("PID", justify="right")
                table.add_column("Nombre", justify="left")
                table.add_column("Estado", justify="center")
                table.add_column("% CPU", justify="right")
                table.add_column("% RAM", justify="right")
                for proc in processes:
                    table.add_row(
                        str(proc.pid),
                        proc.name,
                        proc.status,
                        f"{proc.cpu_percent:.1f}",
                        f"{proc.memory_percent:.1f}"
                    )
                console.print(table)
            else:
                console.print("[bold yellow]No se pudieron obtener procesos activos.[/bold yellow]")

            input("\nPresiona Enter para volver al menú...")


        elif choice == "3":
            clear_screen()
            show_banner()
            with console.status("[green]Escaneando puertos abiertos..."):
                ports = Scan_puertos()
                time.sleep(0.5)

            if ports:
                table = Table(title="Puertos abiertos")
                table.add_column("Protocolo", justify="center")
                table.add_column("Puerto", justify="right")
                table.add_column("Servicio")
                for proto, port, service in ports:
                    table.add_row(proto, str(port), service)
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
            with console.status("[green]Evaluando seguridad del sistema..."):
                os_version = get_os_version()
                active_processes = procesos()
                raw_ports = Scan_puertos()
                resource_usage = usorecursos()

                # Preparamos la lista de puertos para la función:
                open_ports_for_score = [(port, service) for _, port, service in raw_ports]

                score, recommendations = evaluacion({
                    'os_version': os_version,
                    'active_processes': active_processes,
                    'open_ports': open_ports_for_score,
                    'cpu_usage': resource_usage['cpu_usage'],
                    'ram_usage': resource_usage['ram_usage']
                })
                time.sleep(0.5)

            console.print(f"\n[bold magenta] Puntuación de seguridad: {score}/100[/bold magenta]")
            if recommendations:
                console.print("\n Recomendaciones:")
                for r in recommendations:
                    console.print(f" - {r}")
            else:
                console.print("[green]¡Todo se ve bien![/green]")

            input("\nPresiona Enter para volver al menú...")
 
        elif choice == "6":
            clear_screen()
            show_banner()
            aplicaciones = apps()
            table = Table(title="Aplicaciones Instaladas")
            table.add_column("Nombre", style="cyan")
            table.add_column("Version", style="green")
            for name, version in aplicaciones[:30]:
                table.add_row(name, version)
            if len(aplicaciones) > 30:
                console.print(f"\n[bold yellow]Mostrando 30 de {len(aplicaciones)} aplicaciones...[/bold yellow]")
            

            input("\nPresiona Enter para volver al menú...")
            

        elif choice == "0":
            console.print("[red]Saliendo del programa...[/red]")
            break

if __name__ == "__main__":
    main()
