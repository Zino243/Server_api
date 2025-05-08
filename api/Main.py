from flask import Flask, request, jsonify
from pydantic import ValidationError
from . import Crud, Database
from .BaseModels import Enfermero, Dispositivo, Habitacion, Cama, Asistencia, Presencia, Cookie, LlamadaTemporal
from . import DataControlService

# Inicializar la aplicación Flask
app = Flask(__name__)

# Crear tablas
Database.Base.metadata.create_all(bind=Database.engine)

# Dependencia que proporciona la sesión de la base de datos
def get_db():
    db = Database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear usuario
@app.route("/user/create", methods=["POST"])
def create_usuario():
    db = next(get_db())
    try:
        enfermero = Enfermero(**request.json)
        Crud.create_enfermeros(
            nombre=enfermero.nombre,
            apellido=enfermero.apellido,
            codigo=enfermero.codigo,
            contrasena=enfermero.contrasena,
            fecha_de_alta=enfermero.fecha_de_alta,
            fecha_de_baja=enfermero.fecha_de_baja,
            db=db
        )
        return jsonify({"message": "Enfermero creado correctamente"}), 201

    except ValidationError as e:
        return jsonify(e.errors()), 402

# /llamada/numero/letra → GET
# esto se manda cuando el enfermo pulsa el boton para llamar al enfermero
# guardar en tabla llamadas_temp: habitacion, cama,hora

@app.route("/llamada/<int:numero_habitacion>/<string:letra_cama>", methods=["GET"])
def llamar_enfermo(numero_habitacion, letra_cama):
    db = next(get_db())
    return {"value": DataControlService.save_call_in_bbdd(numero_habitacion =numero_habitacion, letra_cama = letra_cama, db= db)}




# # Ruta para obtener un usuario por ID
# @app.route("/usuarios/<int:usuario_id>", methods=["GET"])
# def read_usuario(usuario_id):
#     db = next(get_db())
#     db_usuario = crud.get_usuario(db=db, usuario_id=usuario_id)
#     if db_usuario is None:
#         return jsonify({"detail": "Usuario no encontrado"}), 404
#     return jsonify(db_usuario.to_dict())
#
# # Ruta para obtener todos los usuarios
# @app.route("/usuarios/", methods=["GET"])
# def read_usuarios():
#     skip = int(request.args.get("skip", 0))
#     limit = int(request.args.get("limit", 100))
#     db = next(get_db())
#     usuarios = crud.get_usuarios(db=db, skip=skip, limit=limit)
#     return jsonify([usuario.to_dict() for usuario in usuarios])
