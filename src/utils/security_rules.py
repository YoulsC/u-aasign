def evaluate_security_score(system_info):
    score = 100
    recommendations = []

    # Comprobar versión del SO
    os_version = system_info.get('os_version')
    if os_version:
        if 'Windows' in os_version:
            if '10' not in os_version:
                score -= 20
                recommendations.append("Considere actualizar a Windows 10 o posterior.")
        elif 'Linux' in os_version:
            if 'Ubuntu 18.04' not in os_version and 'Ubuntu 20.04' not in os_version:
                score -= 15
                recommendations.append("Considere usar una versión de Ubuntu con soporte.")

    # Comprobar procesos activos
    active_processes = system_info.get('active_processes', [])
    if len(active_processes) > 50:
        score -= 10
        recommendations.append("Reduzca el número de procesos activos para mejorar la seguridad.")

    # Comprobar puertos abiertos
    open_ports = system_info.get('open_ports', [])
    if len(open_ports) > 10:
        score -= 15
        recommendations.append("Cierre los puertos abiertos innecesarios.")

    # Penalizar puertos inseguros específicos
    insecure_ports = [21, 23, 445, 3389]
    found_insecure = [port for port, _ in open_ports if port in insecure_ports]
    if found_insecure:
        score -= 20
        recommendations.append(f"Cierre los puertos inseguros: {', '.join(map(str, found_insecure))}.")

    # Comprobar uso de CPU
    cpu_usage = system_info.get('cpu_usage', 0)
    if cpu_usage > 80:
        score -= 10
        recommendations.append("Uso de CPU elevado detectado. Investigue los procesos en ejecución.")

    # Comprobar uso de RAM
    ram_usage = system_info.get('ram_usage', 0)
    if ram_usage > 80:
        score -= 10
        recommendations.append("Uso de RAM elevado detectado. Considere cerrar aplicaciones no utilizadas.")

    return score, recommendations
