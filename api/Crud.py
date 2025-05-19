# app/Crud.py

from sqlalchemy.orm import Session
from . import Models
from .BaseModels import Asistencia
from .Models import Camas, Habitaciones, Cookies, Asistencias


# # Función para crear un usuario
# def create_usuario(db: Session, nombre: str, correo: str):
#     db_usuario = models.Usuario(nombre=nombre, correo=correo)
#     db.add(db_usuario)
#     db.commit()
#     db.refresh(db_usuario)
#     return db_usuario
#
# # Función para obtener un usuario por ID
# def get_usuario(db: Session, usuario_id: int):
#     return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
#
# # Función para obtener todos los usuarios
# def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Usuario).offset(skip).limit(limit).all()
#
# enfermeros

def create_enfermeros(nombre: str, apellido: str, codigo: str, contrasena: str, fecha_de_alta, fecha_de_baja,
                      db: Session):
    enfermero = Models.Enfermeros(
        nombre=nombre,
        apellido=apellido,
        codigo=codigo,
        fecha_de_alta=fecha_de_alta,
        fecha_de_baja=fecha_de_baja,
        contrasena=contrasena,
    )
    db.add(enfermero)
    db.commit()
    db.refresh(enfermero)


def update_enfermeros():
    return


def read_enfermeros():
    return


def delete_enfermeros(codigo: str):
    return

def id_for_cookie(db:Session, cookie:int):
    query_cookie = db.query(Cookies)

    try:
        query_cookie = query_cookie.filter(Cookies.cookie_valor == cookie).first()
        return query_cookie.enfermeros_id
    except Exception as e:
        return {"error": str(e)}
# dispositivos

def create_dispositivos():
    return


def update_dispositivos():
    return


def read_dispositivos():
    return


def delete_dispositivos():
    return


# habitaciones

def create_habitaciones():
    return


def update_habitaciones():
    return

def read_habitaciones(db:Session, numero_habitacion):
    return
def habitacionID(db:Session, numero_habitacion):
    '''return habitacion ID'''
    query_habitaciones = db.query(Habitaciones)

    if int(numero_habitacion) is not None:
        try:
            habitacion = query_habitaciones.filter(Habitaciones.numero == numero_habitacion).first()
            return habitacion.id
        except Exception as e:
            return {"error", str(e)}
    return
def habitacion_num(db:Session, habitacion_id:int):
    '''return habitacion ID'''
    query_habitaciones = db.query(Habitaciones)

    if int(habitacion_id) is not None:
        try:
            habitacion = query_habitaciones.filter(Habitaciones.id == habitacion_id).first()
            return habitacion.numero
        except Exception as e:
            return {"error", str(e)}
    return

def delete_habitaciones():
    return


# camas

def create_camas():
    return


def update_camas():
    return


def camas_id(db: Session, habitacion:int = None, letra_cama: str = None, ) -> int:
    query_camas = db.query(Camas)

    if letra_cama is not None or habitacion is not None:
        try:
            cama = query_camas.filter(Camas.letra == letra_cama).all()
            if cama:
                for i in cama:
                    if i.habitacion_id == habitacion:
                        return i.id
            else:
                return 0
        except Exception as e:
            print(f"cama error {e}")
            return 0
    else:
        return 0

def cama_letra(db:Session, cama_id:int) -> str:
    query_camas = db.query(Camas)

    if cama_id != 0:
        try:
            cama = query_camas.filter(Camas.id == cama_id).first()
            return cama.letra
        except Exception as e:
            print(f"cama error {e}")
    else:
        return "0"

def ip_cama(db:Session, cama_id:int) -> str:
    query_camas = db.query(Camas)

    if cama_id != 0:
        try:
            ip = query_camas.filter(Camas.id == cama_id).first()
            return ip.ip
        except Exception as e:
            print(f"cama error for ip {e}")
    else:
        return "0"
def delete_camas():
    return


# asistencias

def create_asistencias(db:Session, habitacion_id, cama_id, enfemero_id):

    asistencia = Models.Asistencias(
        habitacion_id = habitacion_id,
        cama_id = cama_id,
        enfermeros_id = enfemero_id,
    )
    db.add(asistencia)
    db.commit()
    db.refresh(asistencia)


def update_asistencias():
    return


def read_asistencias():
    return


def delete_asistencias():
    return


# presencias

def create_presencias():
    return


def update_presencias():
    return


def read_presencias():
    return


def delete_presencias():
    return


# cookies

def create_cookies():
    return


def update_cookies():
    return


def read_cookies():
    return


def delete_cookies():
    return


# llamadas_temp

def create_llamadas_temporales(db, numero_habitacion, letra_cama):
    llamada_temporal = Models.LlamadasTemporales(
        habitacion_id=int(numero_habitacion),
        cama_id=int(letra_cama),
    )
    db.add(llamada_temporal)
    db.commit()
    db.refresh(llamada_temporal)
    return

def last_llamadas_temporales(db: Session):
    return (
        db.query(Models.LlamadasTemporales)
        .order_by(Models.LlamadasTemporales.hora.desc())
        .limit(24)
        .all()
    )

def update_llamadas_temporales():
    return


def read_llamadas_temporales():
    return


def delete_llamadas_temporales():
    return
