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
from utils.process_info import get_active_processes
from utils.port_scanner import scan_open_ports
from utils.resource_usage import get_resource_usage
from utils.security_rules import evaluate_security_score

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
    console.print("[yellow]0.[/yellow] Salir")

def main():
    while True:
        show_menu()
        choice = Prompt.ask(
            "\n[bold white]Selecciona una opción[/bold white]",
            choices=["1", "2", "3", "4", "5", "0"]
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
                processes = get_active_processes()
                time.sleep(0.5)
            # Aquí podrías formatear y mostrar `processes`
            input("\nPresiona Enter para volver al menú...")

        elif choice == "3":
            clear_screen()
            show_banner()
            with console.status("[green]Escaneando puertos abiertos..."):
                ports = scan_open_ports()
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
                usage = get_resource_usage()
                time.sleep(0.5)
            console.print(f"[bold green]CPU:[/bold green] {usage['cpu_usage']}%")
            console.print(f"[bold green]RAM:[/bold green] {usage['ram_usage']}%")
            input("\nPresiona Enter para volver al menú...")

        elif choice == "5":
            clear_screen()
            show_banner()
            with console.status("[green]Evaluando seguridad del sistema..."):
                os_version = get_os_version()
                active_processes = get_active_processes()
                open_ports = scan_open_ports()
                resource_usage = get_resource_usage()
                score, recommendations = evaluate_security_score({
                    'os_version': os_version,
                    'active_processes': active_processes,
                    'open_ports': open_ports,
                    'resource_usage': resource_usage
                })
                time.sleep(0.5)

            console.print(f"\n[bold magenta]🎯 Puntuación de seguridad: {score}/100[/bold magenta]")
            if recommendations:
                console.print("\n📌 Recomendaciones:")
                for r in recommendations:
                    console.print(f" - {r}")
            else:
                console.print("[green]¡Todo se ve bien![/green]")

            input("\nPresiona Enter para volver al menú...")

        elif choice == "0":
            console.print("[red]Saliendo del programa...[/red]")
            break

if __name__ == "__main__":
    main()
