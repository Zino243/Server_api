from sqlalchemy.orm import Session
import requests
from . import Crud


def save_call_in_bbdd(numero_habitacion, letra_cama:str, db: Session):

    habitacion = Crud.habitacionID(db=db, numero_habitacion = numero_habitacion)
    letra = Crud.camas_id(db=db, habitacion = habitacion, letra_cama= letra_cama)
    print(letra)
    Crud.create_llamadas_temporales(db = db,
                                    letra_cama = letra,
                                    numero_habitacion=habitacion
                                    # hora autogenerada i guess#
                                    )

def save_asistencias(db:Session, numero_habitacion, letra_cama, cookie):
    habitacion_id = Crud.habitacionID(db = db, numero_habitacion = numero_habitacion)
    cama_id = Crud.camas_id(db=db, habitacion = habitacion_id, letra_cama= letra_cama)
    enfemero_id = Crud.id_for_cookie(db=db, cookie=cookie)
    Crud.create_asistencias(db = db ,habitacion_id = habitacion_id, cama_id = cama_id, enfemero_id = enfemero_id)

def send_led_on(db: Session, numero_habitacion: str, letra_cama: str) -> None:

    habitacion = Crud.habitacionID(db = db, numero_habitacion = numero_habitacion)
    cama_id = Crud.camas_id(db=db, habitacion = habitacion, letra_cama= letra_cama)
    ip = Crud.ip_cama(db=db, cama_id= cama_id)
    if ip == 0:
        raise ValueError(f"ip incorrecta {ip}")
    else:
        response = requests.get(f"http://{ip}/relay/0?turn=on")
        response.raise_for_status()

def last_llamadas_temporales(db: Session):
    llamadas = Crud.last_llamadas_temporales(db)
    resultado = [
        {
            "habitacion_id": Crud.habitacion_num(db, l.habitacion_id),
            "cama_id": Crud.cama_letra(db, l.cama_id),
            "hora": l.hora.strftime('%H:%M:%S')  # convertimos time a string
        }
        for l in llamadas
    ]

    print(resultado)
    return resultado