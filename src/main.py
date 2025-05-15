# src/main.py

from math import prod
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.status import Status
from pyfiglet import figlet_format

import os
import time
import psutil

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

            processes = [p for p in processes if p.pid != 0]

            if processes:
                console.print(
                    "[yellow]⚠️  Revisar primero los procesos que más CPU consumen ayuda a detectar rápida y eficientemente posibles amenazas.[/yellow]\n"
                )

                # Normalizamos uso de CPU a 0–100%
                n_cpus = psutil.cpu_count()
                top_procs = sorted(
                    processes,
                    key=lambda p: p.cpu_percent / n_cpus,
                    reverse=True
                )[:10]

                # Mostrar la tabla de Top 10
                table = Table(title="Top 10 Procesos por CPU")
                table.add_column("PID", justify="right")
                table.add_column("Nombre", justify="left")
                table.add_column("% CPU", justify="right")
                table.add_column("% RAM", justify="right")

                for proc in top_procs:
                    table.add_row(
                        str(proc.pid),
                        proc.name,
                        f"{(proc.cpu_percent / n_cpus):.1f}",
                        f"{proc.memory_percent:.1f}"
                    )
                console.print(table)

                # Preguntar y analizar en VirusTotal
                if Prompt.ask("\n¿Quieres analizar alguno de estos procesos en VirusTotal? (s/n)", choices=["s", "n"]) == "s":
                    pid_choices = [str(p.pid) for p in top_procs]
                    pid = Prompt.ask("Selecciona el PID a analizar", choices=pid_choices)
                    try:
                        p = psutil.Process(int(pid))
                        exe_path = p.exe()
                        from utils.virustotal_api import analizar_archivo_virustotal
                        console.print(f"[cyan]Analizando archivo: {exe_path}[/cyan]")
                        result = analizar_archivo_virustotal(exe_path)

                        if "error" in result:
                            console.print(f"[red]{result['error']}[/red]")
                        else:
                            stats = result['data']['attributes']['stats']
                            console.print("\n[bold]VirusTotal:[/bold]")
                            console.print(f" - Malicioso: [red]{stats['malicious']}[/red]")
                            console.print(f" - Sospechoso: [yellow]{stats['suspicious']}[/yellow]")
                            console.print(f" - No detectado: [green]{stats['undetected']}[/green]")
                            sha256 = result['meta'].get('file_info', {}).get('sha256')
                            if sha256:
                                console.print(f"\n[cyan]Más info:[/cyan] https://www.virustotal.com/gui/file/{sha256}")
                    except psutil.AccessDenied:
                        console.print(f"[red]Acceso denegado al proceso {pid}[/red]")
                    except psutil.NoSuchProcess:
                        console.print(f"[red]El proceso {pid} ya no existe[/red]")
                    except Exception as e:
                        console.print(f"[red]Error analizando el proceso: {e}[/red]")

            else:
                console.print("[bold yellow]No se pudieron obtener procesos activos válidos.[/bold yellow]")

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
                raw_ports = scan_open_ports()
                resource_usage = get_resource_usage()

                # Preparamos la lista de puertos para la función:
                open_ports_for_score = [(port, service) for _, port, service in raw_ports]

                score, recommendations = evaluate_security_score({
                    'os_version': os_version,
                    'active_processes': active_processes,
                    'open_ports': open_ports_for_score,
                    'cpu_usage': resource_usage['cpu_usage'],
                    'ram_usage': resource_usage['ram_usage']
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
