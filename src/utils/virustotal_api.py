import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")  

def analizar_archivo_virustotal(file_path, api_key=API_KEY):
    url = 'https://www.virustotal.com/api/v3/files'
    headers = {'x-apikey': api_key}

    with open(file_path, 'rb') as f:
        files = {'file': (file_path, f)}
        response = requests.post(url, files=files, headers=headers)
        if response.status_code == 200 or response.status_code == 202:
            analysis_id = response.json()['data']['id']
            # Ahora consultamos el resultado
            report_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
            report_response = requests.get(report_url, headers=headers)
            if report_response.status_code == 200:
                return report_response.json()
            else:
                return {"error": f"Error al obtener el informe: {report_response.status_code}"}
        else:
            return {"error": f"Error al enviar el archivo: {response.status_code}, {response.text}"}
