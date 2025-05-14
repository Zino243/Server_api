from flask import Flask
from flask import jsonify
from flask_cors import CORS

from . import DataControlService
from . import Database

app = Flask(__name__)
CORS(app)
# Database.Base.metadata.drop_all(bind=Database.engine) # este es para eliminar la base de datos
Database.Base.metadata.create_all(bind=Database.engine)

def get_db():
    db = Database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify("pong"), 200

@app.route("/llamada/<string:numero_habitacion>/<string:letra_cama>", methods=["GET"])
def llamar_enfermo(numero_habitacion, letra_cama):
    db = next(get_db())
    DataControlService.save_call_in_bbdd(numero_habitacion =numero_habitacion, letra_cama= letra_cama, db= db)

    return "correct"

@app.route("/atender_asistencia/<string:numero_habitacion>/<string:letra_cama>/<string:cookie>", methods=["GET"])
def atender_asistencia(numero_habitacion, letra_cama, cookie:str):
    db = next(get_db())

    DataControlService.send_led_on(db, numero_habitacion, letra_cama)
    DataControlService.save_asistencias(db, numero_habitacion, letra_cama, cookie)
    return f"asistencia atendida por el usuario con la galleta {cookie}"

@app.route("/ultimas_asistencias", methods=["GET"])
def ultimas_asistencias():
    db = next(get_db())
    return jsonify(DataControlService.last_llamadas_temporales(db=db)), 200