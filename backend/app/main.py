from fastapi import FastAPI, HTTPException
import requests
import json
from datetime import date
from pydantic import BaseModel

app = FastAPI()

# URL y token de acceso
url = "https://demo.netbox.dev/api/dcim/devices/"
token = "46423cbdccb1b82b0a51eca17e57306d286e8846"


def obtener_datos_dispositivos():
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Error al obtener los datos")

def procesar_datos(dispositivos):
    resultados = []

    for dispositivo in dispositivos.get('results', []):
        dispositivo_info = {
            'id': dispositivo.get('id'),
            'name': dispositivo.get('name'),
            'manufacturer': dispositivo.get('device_type', {}).get('manufacturer', {}).get('name')
        }

        ipv4 = dispositivo.get('primary_ip4', {})
        dispositivo_info['primary_ip4'] = ipv4 if ipv4 else '0.0.0.0'

        resultados.append(dispositivo_info)

    return resultados

@app.get("/procesar-consulta-y-generar-json")
def procesar_consulta_y_generar_json():
    try:
        datos_dispositivos = obtener_datos_dispositivos()
        resultados = procesar_datos(datos_dispositivos)
        
        with open('resultados_dispositivos.json', 'w') as file:
            json.dump(resultados, file, indent=4)

        return {"message": "Datos procesados y guardados en resultados_dispositivos.json"}
    except HTTPException as e:
        return e.detail




""" segundo punto"""
class Payload(BaseModel):
    nombre: str


@app.post("/generar_payload")
async def generar_payload(payload: Payload):
    fecha_hoy = date.today()

    contenido = f"Nombre: {payload.nombre}\nFecha: {fecha_hoy}"
    with open("payload.txt", "w") as archivo:
        archivo.write(contenido)

    return {"mensaje": "Archivo generado correctamente"}
