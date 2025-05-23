# app/Crud.py

from sqlalchemy.orm import Session
from . import Models
from .Models import Camas, Habitaciones, Cookies, Asistencias
from datetime import datetime, timedelta

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

def create_enfermero(db: Session, enfermero: dict) -> None:
    """Crea un nuevo enfermero en la base de datos."""
    try:
        new_enfermero = Models.Enfermeros(
            nombre=enfermero["nombre"],
            apellido=enfermero["apellido"],
            codigo=enfermero["codigo"],
            contrasena=enfermero["contrasena"]
        )
        db.add(new_enfermero)
        db.commit()
        db.refresh(new_enfermero)
    except Exception as e:
        print(f"Error al crear enfermero: {e}")
        raise

def exist_enfermero(db:Session, codigo: str):
    """verifica si existe un enfermero"""
    query_enfermeros = db.query(Models.Enfermeros).filter(Models.Enfermeros.codigo == codigo).first()
    if query_enfermeros:
        return True
    else:
        return False
def enfermero_by_code(db:Session, codigo: str):
    """devuelve un enfermero por su codigo"""
    query_enfermeros = db.query(Models.Enfermeros).filter(Models.Enfermeros.codigo == codigo).first()
    if query_enfermeros:
        return query_enfermeros.nombre
    else:
        return False

def enfermero_ID_by_code(db:Session, codigo: str):
    """devuelve un enfermero por su codigo"""
    query_enfermeros = db.query(Models.Enfermeros).filter(Models.Enfermeros.codigo == codigo).first()
    if query_enfermeros:
        return query_enfermeros.id
    else:
        return False
def all_enfermeros(db: Session):
    """devuelve todos los enfermeros"""
    query_enfermeros = db.query(Models.Enfermeros).all()
    return query_enfermeros

def enfermero_by_id(db: Session, id: int):
    """devuelve un enfermero por su id"""
    query_enfermeros = db.query(Models.Enfermeros).filter(Models.Enfermeros.id == id).first()
    if query_enfermeros:
        return query_enfermeros.nombre
    else:
        return False

def delete_enfermeros(db: Session, id: str):
    # Buscar al enfermero por su id
    enfermero = db.query(Models.Enfermeros).filter(Models.Enfermeros.id == id).first()

    if enfermero:
        # Eliminar el enfermero (SQLAlchemy se encargará de borrar las relaciones por el cascade)
        db.delete(enfermero)
        db.commit()
        return True
    else:
        return False


def id_for_cookie(db:Session, cookie:int):
    query_cookie = db.query(Cookies)

    try:
        query_cookie = query_cookie.filter(Cookies.cookie_valor == cookie).first()
        return query_cookie.enfermeros_id
    except Exception as e:
        return {"error": str(e)}

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
    print("[+]asistencia guardada")
    try:
        asistencia = Models.Asistencias(
            habitacion_id = habitacion_id,
            cama_id = cama_id,
            enfermeros_id = enfemero_id,
        )
        db.add(asistencia)
        db.commit()
        db.refresh(asistencia)
    except Exception as e:
        print(f"Error al guardar asistencia: {e}")
# presencias
def create_presencias(db:Session, habitacion_id, cama_id):
    presencia = Models.Presencias(
        habitacion_id = habitacion_id,
        cama_id = cama_id,
    )
    db.add(presencia)
    db.commit()
    db.refresh(presencia)

# llamadas_temp

def create_llamadas_temporales(db, numero_habitacion, letra_cama):
    llamada_temporal = Models.LlamadasTemporales(
        habitacion_id=numero_habitacion,
        cama_id=letra_cama,
    )
    db.add(llamada_temporal)
    db.commit()
    db.refresh(llamada_temporal)
    return llamada_temporal.llamada_id


def last_llamadas_temporales(db: Session):
    return (
        db.query(Models.LlamadasTemporales)
        .order_by(Models.LlamadasTemporales.hora)
        .all()
    )
def llamada_enfermero(db: Session, llamada_id: int, enfermero_id):
    llamada = db.query(Models.LlamadasTemporales).filter(Models.LlamadasTemporales.llamada_id == llamada_id).first()
    if llamada:
        llamada.enfermero_id = enfermero_id
        db.commit()
        return True
    else:
        return False

def ultima_ip_asignada(db:Session):
    query_camas = db.query(Camas).order_by(Camas.id.desc()).first()
    if query_camas:
        return query_camas.ip
    else:
        return 0

def get_llamadas_temporales(db: Session):
    return db.query(Models.LlamadasTemporales).all()

def get_llamada_temporal(db: Session, llamada_id: int):
    return db.query(Models.LlamadasTemporales).filter(Models.LlamadasTemporales.llamada_id == llamada_id).first()

def update_estado_llamada_cogida(db: Session, numero_habitacion, letra_cama):
    """
    Actualiza el estado a 'cogida' para todas las llamadas pendientes de una cama y habitación.
    """
    try:
        llamadas = (
            db.query(Models.LlamadasTemporales)
            .filter(
                Models.LlamadasTemporales.habitacion_id == numero_habitacion,
                Models.LlamadasTemporales.cama_id == letra_cama,
                Models.LlamadasTemporales.estado.in_(['pendiente', 'en_espera'])
            )
            .all()
        )
        if llamadas:
            for llamada in llamadas:
                llamada.estado = 'cogida'
            db.commit()
            return True
        else:
            return False
    except Exception as e:
        print(f"Error al actualizar llamadas: {e}")
        db.rollback()
        return False
def update_estado_llamada_por_id(db: Session, llamada_id: int, nuevo_estado: str):
    """Actualiza el estado de una llamada temporal por su ID."""
    if nuevo_estado not in ['pendiente', 'cogida', 'en_espera']:
        raise ValueError("Estado no válido. Los valores permitidos son: 'pendiente', 'cogida', 'en_espera'.")
    llamada = db.query(Models.LlamadasTemporales).filter(Models.LlamadasTemporales.llamada_id == llamada_id).first()
    if llamada:
        llamada.estado = nuevo_estado
        db.commit()
        return True
    else:
        return False

def marcar_llamada_cogida(db: Session, numero_habitacion, letra_cama):
    return update_estado_llamada_cogida(db, numero_habitacion, letra_cama)

def marcar_llamada_espera(db: Session, llamada_id: int):
    return update_estado_llamada_por_id(db, llamada_id, 'en_espera')

def marcar_llamada_pendiente(db: Session, llamada_id: int):
    return update_estado_llamada_por_id(db, llamada_id, 'pendiente')
