import json

ruta_config = 'config.json'

def cargar_configuracion():
    with open(ruta_config, "r") as f:
        return json.load(f)