from . import ConfigService
from ipaddress import ip_address
from sqlalchemy.orm import Session
from . import Crud


def obtener_ultima_ip(db: Session):
    # Supón que Crud.ultima_ip_asignada devuelve la última IP como string
    return Crud.ultima_ip_asignada(db)

def siguiente_ip(db:Session):
    c = ConfigService.cargar_configuracion()
    ip = ip_address(obtener_ultima_ip(db))
    ip_fin = ip_address(c["ip_fin"])
    if ip < ip_fin:
        return str(ip + 1)
    else:
        raise ValueError("No hay más IPs disponibles en el rango.")

def asignar_ip(db: Session):
    config = ConfigService.cargar_configuracion()
    tipo = config["tipo"]  # A, B o C
    ip_inicio = config["ip_inicio"]
    ip_fin = config["ip_fin"]

    ultima_ip = obtener_ultima_ip(db)
    if ultima_ip:
        nueva_ip = siguiente_ip('config.json', db)
    else:
        nueva_ip = ip_inicio

    # Aquí podrías guardar la nueva IP en la base de datos si es necesario
    return {"tipo": tipo, "ip": nueva_ip}