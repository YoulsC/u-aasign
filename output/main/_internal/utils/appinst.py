# appinst.py

import subprocess
import json

def apps():
    try:
        script = """
        Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* |
        Select-Object DisplayName, DisplayVersion |
        Where-Object { $_.DisplayName -ne $null } |
        ConvertTo-Json
        """
        result = subprocess.run(
            ["powershell", "-Command", script],
            capture_output=True,
            text=True,
            shell=True
        )

        apps = []
        if result.stdout:
            parsed = json.loads(result.stdout)
            if isinstance(parsed, list):
                for entry in parsed:
                    apps.append((
                        entry.get("DisplayName", "Desconocido"),
                        entry.get("DisplayVersion", "N/A")
                    ))
            elif isinstance(parsed, dict):
                apps.append((
                    parsed.get("DisplayName", "Desconocido"),
                    parsed.get("DisplayVersion", "N/A")
                ))
        return apps

    except Exception as e:
        print(f"Error al obtener aplicaciones: {e}")
        return []
