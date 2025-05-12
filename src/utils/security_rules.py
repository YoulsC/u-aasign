def evaluate_security_score(system_info):
    score = 100
    recommendations = []

    # Check OS version
    os_version = system_info.get('os_version')
    if os_version:
        if 'Windows' in os_version:
            if '10' not in os_version:
                score -= 20
                recommendations.append("Consider upgrading to Windows 10 or later.")
        elif 'Linux' in os_version:
            if 'Ubuntu 18.04' not in os_version and 'Ubuntu 20.04' not in os_version:
                score -= 15
                recommendations.append("Consider using a supported version of Ubuntu.")

    # Check active processes
    active_processes = system_info.get('active_processes', [])
    if len(active_processes) > 50:
        score -= 10
        recommendations.append("Reduce the number of active processes to improve security.")

    # Check open ports
    open_ports = system_info.get('open_ports', [])
    if len(open_ports) > 10:
        score -= 15
        recommendations.append("Close unnecessary open ports.")

    #Penalizar los puertos inseguros especificos
    insecure_ports = [21, 23, 445, 3389]
    found_insecure = [port for port, _ in open_ports if port in insecure_ports]
    if found_insecure:
        score -= 20
        recommendations.append(f"Close insecure ports: {', '.join(map(str, found_insecure))}.")

    # Check CPU usage
    cpu_usage = system_info.get('cpu_usage', 0)
    if cpu_usage > 80:
        score -= 10
        recommendations.append("High CPU usage detected. Investigate running processes.")

    # Check RAM usage
    ram_usage = system_info.get('ram_usage', 0)
    if ram_usage > 80:
        score -= 10
        recommendations.append("High RAM usage detected. Consider closing unused applications.")

    return score, recommendations