# app/Crud.py

from sqlalchemy.orm import Session
from . import Models
from .Models import Camas


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

def create_enfermeros(nombre: str, apellido: str, codigo: str, contrasena: str, fecha_de_alta, fecha_de_baja, db: Session):
    enfermero = Models.Enfermeros(
        nombre = nombre,
        apellido = apellido,
        codigo = codigo,
        fecha_de_alta = fecha_de_alta,
        fecha_de_baja = fecha_de_baja,
        contrasena = contrasena,
    )
    db.add(enfermero)
    db.commit()
    db.refresh(enfermero)
    
def update_enfermeros():
    return
def read_enfermeros():
    return
def delete_enfermeros(codigo:str):
    return
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
def read_habitaciones():
    return
def delete_habitaciones():
    return

# camas

def create_camas():
    return
def update_camas():
    return
def read_camas(db: Session, letra_cama: str = None):
    query = db.query(Camas)

    if letra_cama is not None:
        try:
            query = query.filter(Camas.letra == letra_cama)
            return 300
        except:
            return 400

def delete_camas():
    return

# asistencias

def create_asistencias():
    return
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

def create_llamadas_temporales():
    return
def update_llamadas_temporales():
    return
def read_llamadas_temporales():
    return
def delete_llamadas_temporales():
    return
