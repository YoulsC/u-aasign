# U-AASIGN - Sistema de Analisis de Seguridad

U-AAsign es una herramienta de evaluación de seguridad del sistema para Windows . Analiza puertos abiertos, uso de recursos, procesos y da recomendaciones.


## Features

- Recupera la version del sistema operativo.
- Lista los procesos activos.
- Escanea los puertos abiertos en localhost.
- Mide el uso de CPU y RAM.
- Evalua una puntuacion de seguridad y genera recomendaciones.

## Estructura del proyecto

```
u-aasign
├── src
│   ├── main.py                 # Punto de entrada para la app
│   ├── utils
│   │   ├── os_info.py          # Funciones para obtener el OS del sistema
│   │   ├── process_info.py     # Funciones para obtener los procesos del sistema
│   │   ├── appinst.py          # Funciones para obtener las apps del sistema y ver cuales podrian actualizarse
│   │   ├── puertoscan.py       # Funciones para obtener los puertos abiertos 
│   │   ├── usorecursos.py      # Funciones para monitorear CPU y uso de RAM 
│   │   ├── virustotal_api.py   # Api para detectar codigo malicioso
│   │   └── evaluaciones.py     # Funciones para evaluar las funciones anteriores con una calificacion
├── requirements.txt            # Dependencias usadas
└── README.md                   # Documentacion
```

## Instalacion


1. Haz double clic en  'uaasign.exe'


## Link Github
https://github.com/YoulsC/u-aasign.git


## Como usarlo

⠀
1. Descarga `uaasign.exe`
2. Ejecuta el archivo (doble clic o desde terminal)
3. Navega por el menú escribiendo el número de la opción
4. Presiona Enter para volver al menú


## Recomendaciones 
Usar Windows :p


## Autores
Sergio Armando Valdivia Padilla
Julio Cesar Gutierrez Martin
-Proyecto academico no comercial -2025