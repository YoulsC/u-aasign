# appinst.py

import subprocess
import json
import pyfiglet
from rich.table import Table
from rich.console import Console

def apps():
    
    comando = [
        "powershell",
        "-NoProfile",
        "-Command",
        """
        $ErrorActionPreference = 'SilentlyContinue';
        $apps = Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*,
                                 HKLM:\\Software\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* |
                Select-Object DisplayName, DisplayVersion |
                Where-Object { $_.DisplayName -and $_.DisplayVersion } ;
        $apps | ConvertTo-Json -Compress -Depth 2
        """
    ]
    try:
        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )
        salida = resultado.stdout.strip()
        if not salida:
            print("No se obtuvo salida de PowerShell.")
            return []
        try:
            datos = json.loads(salida)
        except Exception as e:
            print("Error al leer JSON:", e)
            print("Salida recibida:", salida[:500])
            return []
        if isinstance(datos, dict):
            datos = [datos]
        lista_apps = [
            (app.get("DisplayName", "Desconocido"), app.get("DisplayVersion", "Desconocido"))
            for app in datos
        ]
       
        console = Console()
        table = Table(title="Aplicaciones Instaladas")
        table.add_column("Nombre", style="cyan")
        table.add_column("Versión", style="yellow")

        for nombre, version in lista_apps:
            table.add_row(nombre, version)
        console.print(table)
       
        print("\nBuscando aplicaciones con actualización disponible...\n")
        apps_con_actualizacion(lista_apps)
        return lista_apps
    except Exception as e:
        print(f"Error al obtener aplicaciones: {e}")
        return []

def apps_con_actualizacion(lista_apps):
   
    try:
        resultado = subprocess.run(
            ["winget", "upgrade", "--source", "winget"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )
        salida = resultado.stdout
        if not salida:
            print("No se pudo obtener información de actualizaciones.")
            return []
        lineas = salida.splitlines()
        actualizables = []
        encabezado = False
        for linea in lineas:
            if not encabezado:
                if linea.strip().startswith("Nombre") or "----" in linea:
                    encabezado = True
                continue
            if not linea.strip():
                continue
            partes = linea.split()
            if len(partes) >= 4:
                nombre = " ".join(partes[:-3])
                version_actual = partes[-3]
                version_nueva = partes[-2]
                origen = partes[-1]
                actualizables.append((nombre, version_actual, version_nueva))
        if actualizables:
            console = Console()
            table = Table(title="Aplicaciones con Actualización Disponible")
            table.add_column("Nombre", style="cyan")
            table.add_column("Versión Actual", style="yellow")
            table.add_column("Nueva Versión", style="green")

            for nombre, version_actual, version_nueva in actualizables:
                table.add_row(nombre, version_actual, version_nueva)

            console.print(table)

        else:
            print("No se encontraron aplicaciones con actualización disponible.")
        return actualizables
    except Exception as e:
        print(f"Error al buscar actualizaciones: {e}")
        return []
