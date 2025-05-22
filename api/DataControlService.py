from sqlalchemy.orm import Session
import requests
from . import Crud
from . import IPControlService
from . import ConfigService
url = "https://api.pushover.net/1/messages.json"

def save_call_in_bbdd(numero_habitacion, letra_cama:str, db: Session):

    habitacion = Crud.habitacionID(db=db, numero_habitacion = numero_habitacion)
    letra = Crud.camas_id(db=db, habitacion = habitacion, letra_cama= letra_cama)
    print(letra)
    id_llamada = Crud.create_llamadas_temporales(db = db,
                                    letra_cama = letra,
                                    numero_habitacion=habitacion
                                    # hora autogenerada i guess#
                                    )
    send_pushover(numero_habitacion=numero_habitacion, letra_cama=letra_cama, id_llamada=id_llamada)
def send_pushover(numero_habitacion, letra_cama, id_llamada):
    config = ConfigService.cargar_configuracion()
    requests.post(url, data= {
        "token": "ankvim4u8c554keqni3h6f3oymms7a",
        "user": "g6qd86iinmyd2i4gvrrtzgt9849aa5",
        "message": f"ve a la habitacion {numero_habitacion} cama {letra_cama}",
        "url" : f"http://{config["ip_server"]}:{config["puerto_server"]}/atender_asistencia/{numero_habitacion}/{letra_cama}/{id_llamada}",
        "url_title" : "confirmar",
    })

def save_asistencias(db:Session, numero_habitacion, letra_cama, codigo):
    """esto es atender asistencia"""
    try:
        habitacion_id = Crud.habitacionID(db = db, numero_habitacion = numero_habitacion)
        cama_id = Crud.camas_id(db=db, habitacion = habitacion_id, letra_cama= letra_cama)
        enfemero_id = Crud.enfermero_ID_by_code(db=db, codigo=codigo)
        print(f"enfermero id {enfemero_id}")
        Crud.create_asistencias(db = db ,habitacion_id = habitacion_id, cama_id = cama_id, enfemero_id = enfemero_id)
        return True
    except Exception as e:
        print(f"Error al guardar asistencia: {e}")

def send_led_on(db: Session, numero_habitacion: str, letra_cama: str) -> None:

    habitacion = Crud.habitacionID(db = db, numero_habitacion = numero_habitacion)
    cama_id = Crud.camas_id(db=db, habitacion = habitacion, letra_cama= letra_cama)
    ip = Crud.ip_cama(db=db, cama_id= cama_id)
    if ip == 0:
        raise ValueError(f"ip incorrecta {ip}")
    else:
        #-> response = requests.get(f"http://{ip}/relay/0?turn=on")
        #-> response.raise_for_status()
        print("[ x ] led off")

def send_led_off(db: Session, numero_habitacion: str, letra_cama: str) -> None:

    habitacion = Crud.habitacionID(db = db, numero_habitacion = numero_habitacion)
    cama_id = Crud.camas_id(db=db, habitacion = habitacion, letra_cama= letra_cama)
    ip = Crud.ip_cama(db=db, cama_id= cama_id)
    if ip == 0:
        raise ValueError(f"ip incorrecta {ip}")
    else:
        #-> response = requests.get(f"http://{ip}/relay/0?turn=off")
        #-> response.raise_for_status()
        print("[ 0 ] led off")

def last_llamadas_temporales(db: Session):

    llamadas = Crud.last_llamadas_temporales(db)
    resultado = [
        {
            "habitacion_id": Crud.habitacion_num(db, l.habitacion_id),
            "cama_id": Crud.cama_letra(db, l.cama_id),
            "hora": l.hora.strftime('%H:%M:%S'),
            "estado": l.estado
        }
        for l in llamadas
    ]

    print(resultado)
    return resultado

def create_enfermero(db: Session, enfermero: dict) -> None:
    """Crea un nuevo enfermero en la base de datos."""
    try:
        Crud.create_enfermero(db=db, enfermero=enfermero)
    except Exception as e:
        print(f"Error al crear enfermero: {e}")

def all_enfermeros(db:Session):
    """devuelve todos los enfermeros"""
    return Crud.all_enfermeros(db=db)

def delete_enfermeros(db:Session, id: str):
    """elimina un enfermero de la base de datos"""
    return Crud.delete_enfermeros(db=db, id=id)

def exist_enfemero(db:Session, codigo: str):
    """verifica si existe un enfermero"""
    return Crud.exist_enfermero(db=db, codigo=codigo)

def enfermero_by_code(db:Session, codigo: str):
    """devuelve un enfermero por su codigo"""
    return Crud.enfermero_by_code(db=db, codigo=codigo)

def save_presencias(db:Session, numero_habitacion, letra_cama):
    """esto es atender asistencia"""
    try:
        habitacion_id = Crud.habitacionID(db = db, numero_habitacion = numero_habitacion)
        cama_id = Crud.camas_id(db=db, habitacion = habitacion_id, letra_cama= letra_cama)
        Crud.create_presencias(db = db ,habitacion_id = habitacion_id, cama_id = cama_id)
    except Exception as e:
        print(f"Error al guardar asistencia: {e}")

def marcar_llamada_espera(db:Session, id_llamada):
    """marca la llamada como en espera"""
    try:
        Crud.marcar_llamada_espera(db=db, llamada_id=int(id_llamada))
    except Exception as e:
        print(f"Error al marcar llamada en espera: {e}")

def marcar_llamada_en_cogida(db:Session, numero_habitacion, letra_cama):
    """marca la llamada como en espera"""
    try:
        Crud.marcar_llamada_cogida(db=db, numero_habitacion=numero_habitacion, letra_cama=letra_cama)
    except Exception as e:
        print(f"Error al marcar llamada en espera: {e}")