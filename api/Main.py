from flask import Flask, request, jsonify
from pydantic import ValidationError
from . import Crud, Database
from .BaseModels import Enfermero, Dispositivo, Habitacion, Cama, Asistencia, Presencia, Cookie, LlamadaTemporal
from . import DataControlService

app = Flask(__name__)

# Database.Base.metadata.drop_all(bind=Database.engine)
Database.Base.metadata.create_all(bind=Database.engine)

# Dependencia que proporciona la sesión de la base de datos
def get_db():
    db = Database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# # Crear usuario
# @app.route("/user/create", methods=["POST"])
# def create_usuario():
#     db = next(get_db())
#     try:
#         enfermero = Enfermero(**request.json)
#         Crud.create_enfermeros(
#             nombre=enfermero.nombre,
#             apellido=enfermero.apellido,
#             codigo=enfermero.codigo,
#             contrasena=enfermero.contrasena,
#             fecha_de_alta=enfermero.fecha_de_alta,
#             fecha_de_baja=enfermero.fecha_de_baja,
#             db=db
#         )
#         return jsonify({"message": "Enfermero creado correctamente"}), 201
#
#     except ValidationError as e:
#         return jsonify(e.errors()), 402

@app.route("/ping", methods=["GET"])
def ping():
    return "pong"

@app.route("/llamada/<string:numero_habitacion>/<string:letra_cama>", methods=["GET"])
def llamar_enfermo(numero_habitacion, letra_cama):
    db = next(get_db())
    DataControlService.save_call_in_bbdd(numero_habitacion =numero_habitacion, letra_cama= letra_cama, db= db)

    return "correct"

@app.route("/atender_asistencia/<string:numero_habitacion>/<string:letra_cama>/<string:cookie>", methods=["GET"])
def atender_asistencia(numero_habitacion, letra_cama, cookie:str):
    #cuando desde el dispositivo se de a atender
    # [ - ] GET -> http://IP_del_rele/relay/0?turn=on
    # SAVE -> asistencias -> habitacion_id, cama_id, enfermero_id
    db = next(get_db())

    DataControlService.send_led_on(db, numero_habitacion, letra_cama)
    DataControlService.save_asistencias(db, numero_habitacion, letra_cama, cookie)
    return f"asistencia atendida por el usuario con la galleta {cookie}"