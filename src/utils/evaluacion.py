def evaluacion(info_sistema):
    puntaje = 100
    recomendaciones = []

    # Comprobar versión del SO
    version_so = info_sistema.get('version_so')
    if version_so:
        if 'Windows' in version_so:
            if '10' not in version_so:
                puntaje -= 20
                recomendaciones.append("Considere actualizar a Windows 10 o posterior.")
        elif 'Linux' in version_so:
            if 'Ubuntu 18.04' not in version_so and 'Ubuntu 20.04' not in version_so:
                puntaje -= 15
                recomendaciones.append("Considere usar una versión de Ubuntu con soporte.")

    # Comprobar procesos activos
    procesos_activos = info_sistema.get('procesos_activos', [])
    if len(procesos_activos) > 50:
        puntaje -= 10
        recomendaciones.append("Reduzca el número de procesos activos para mejorar la seguridad.")

    # Comprobar puertos abiertos
    puertos_abiertos = info_sistema.get('puertos_abiertos', [])
    if len(puertos_abiertos) > 10:
        puntaje -= 15
        recomendaciones.append("Cierre los puertos abiertos innecesarios.")

    # Penalizar puertos inseguros específicos
    puertos_inseguros = [21, 23, 445, 3389]
    encontrados_inseguros = [puerto for puerto, _ in puertos_abiertos if puerto in puertos_inseguros]
    if encontrados_inseguros:
        puntaje -= 20
        recomendaciones.append(f"Cierre los puertos inseguros: {', '.join(map(str, encontrados_inseguros))}.")

    # Comprobar uso de CPU
    uso_cpu = info_sistema.get('uso_cpu', 0)
    if uso_cpu > 80:
        puntaje -= 10
        recomendaciones.append("Uso de CPU elevado detectado. Investigue los procesos en ejecución.")

    # Comprobar uso de RAM
    uso_ram = info_sistema.get('uso_ram', 0)
    if uso_ram > 80:
        puntaje -= 10
        recomendaciones.append("Uso de RAM elevado detectado. Considere cerrar aplicaciones no utilizadas.")

    return puntaje, recomendaciones
