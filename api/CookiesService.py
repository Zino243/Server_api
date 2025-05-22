import json
import os

file_path='source/cookies.json'

def ensure_file_exists():
    """Crea el archivo JSON y su carpeta si no existen."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump({}, f)

def leer_cookies():
    """Lee todas las cookies.json del archivo JSON."""
    ensure_file_exists()
    with open(file_path, 'r') as f:
        return json.load(f)

def crear_cookie(key, value):
    """Crea o actualiza una cookie en el archivo JSON."""
    cookies = leer_cookies()
    cookies[key] = value
    with open(file_path, 'w') as f:
        json.dump(cookies, f)

def eliminar_cookie(key):
    """Elimina una cookie del archivo JSON."""
    cookies = leer_cookies()
    if key in cookies:
        del cookies[key]
        with open(file_path, 'w') as f:
            json.dump(cookies, f)
    else:
        raise KeyError(f"La cookie con clave '{key}' no existe.")