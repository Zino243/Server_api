from sqlalchemy.orm import Session

from . import Crud


def save_call_in_bbdd(numero_habitacion,letra_cama, db: Session):
    # comprobar primero que existe la cama y la habitacion
    return Crud.read_camas(db, letra_cama)