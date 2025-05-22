import requests
from flask import Flask, redirect, url_for
from flask import jsonify, request, make_response,  render_template
from flask_cors import CORS
import uuid
from . import IPControlService
from . import DataControlService
from . import Database
from . import CookiesService
from . import ConfigService

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

# Aquí vamos a simular una base de datos con diccionario
sesiones = {}
# Diccionario inverso: device_id -> session_id
usuarios = {}

@app.route("/enroll", methods=["GET"])
def mostrar_formulario():
    return render_template('enroll.html')

@app.route("/enroll", methods=["POST"])
def procesar_registro():
    username = request.form.get("username")
    if not username:
        return "Falta el nombre de usuario", 400

    db = next(get_db())
    # comprueba si el usuairo existe
    if DataControlService.exist_enfemero(db, username):
        # Si ya estaba registrado, eliminar cookie anterior
        if username in usuarios:
            old_session = usuarios[username]
            sesiones.pop(old_session, None)

        # Crear nueva sesión
        session_id = str(uuid.uuid4())
        sesiones[session_id] = username
        usuarios[username] = session_id

        #guardar la cookie
        CookiesService.crear_cookie(session_id, username)

        # Asignar cookie
        resp = make_response(f"✅ Bienvenido, {username}. Te has registrado.")
        resp.set_cookie("session_id", session_id, max_age=604800, httponly=True)
        return resp
    return "❌ Usuario no encontrado", 403

@app.route("/unenroll", methods=["GET"])
def cerrar_sesion():
    session_id = request.cookies.get("session_id")

    if session_id and session_id in sesiones:
        username = sesiones.pop(session_id)
        usuarios.pop(username, None)

    # Eliminar cookie del navegador
    resp = make_response("👋 Sesión cerrada correctamente.")
    resp.set_cookie("session_id", "", max_age=0)

    # eliminar cookie del json

    CookiesService.eliminar_cookie(session_id)
    return resp

@app.route("/confirmar", methods=["GET"])
def confirmar():
    session_id = request.cookies.get("session_id")

    cookie_local = CookiesService.leer_cookies()
    for i in cookie_local.keys():
        if session_id == i:
            db = next(get_db())
            return f"✅ Acción confirmada para {DataControlService.enfermero_by_code(db, cookie_local[i])}", 200
    else:
        return "❌ Sesión no válida. ¿Te registraste?", 403

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify("pong"), 200

@app.route("/llamada/<string:numero_habitacion>/<string:letra_cama>", methods=["GET"])
def llamar_enfermo(numero_habitacion, letra_cama):
    try:
        db = next(get_db())
        DataControlService.send_pushover(numero_habitacion = numero_habitacion, letra_cama = letra_cama)
        DataControlService.save_call_in_bbdd(numero_habitacion=numero_habitacion, letra_cama=letra_cama, db=db)
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/atender_asistencia/<string:numero_habitacion>/<string:letra_cama>", methods=["GET"])
def atender_asistencia(numero_habitacion, letra_cama):
    try:
        db = next(get_db())
        config = ConfigService.cargar_configuracion()

        session_id = request.cookies.get("session_id")
        cookies = {"session_id": session_id}

        # Mandamos esa cookie a /confirmar
        response = requests.get(f"http://{config['ip_server']}:{config['puerto_server']}/confirmar", cookies=cookies)
        response.raise_for_status()

        cookies_local = CookiesService.leer_cookies()
        #
        DataControlService.send_led_on(db, numero_habitacion, letra_cama)
        DataControlService.save_asistencias(db, numero_habitacion, letra_cama, cookies_local[session_id])
        return jsonify({"status": f"ok"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/presencia/<string:numero_habitacion>/<string:letra_cama>", methods=["GET"])
def presencia(numero_habitacion, letra_cama):
    try:
        db = next(get_db())
        DataControlService.send_led_off(db, numero_habitacion, letra_cama)
        DataControlService.save_presencias(db, numero_habitacion, letra_cama)
        # guardar la presencia en la bbdd
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/ultimas_asistencias", methods=["GET"])
def ultimas_asistencias():
    db = next(get_db())
    return jsonify(DataControlService.last_llamadas_temporales(db=db)), 200

@app.route("/admin", methods=["GET"])
def admin_web():
    return render_template('index.html')

@app.route("/admin/gestion_usuarios", methods=["GET", "POST"])
def gestion_usuarios():
    db = next(get_db())

    if request.method == "POST":
        DataControlService.create_enfermero(db, enfermero = {
            "nombre": request.form.get("nombre"),
            "apellido": request.form.get("apellido"),
            "codigo": request.form.get("codigo"),
            "contrasena": request.form.get("contrasena")
        })

    # GET: Mostrar enfermeros
    usuarios = DataControlService.all_enfermeros(db)
    return render_template('gestion_usuarios.html', usuarios=usuarios)


@app.route("/admin/gestion_usuarios/eliminar/<int:id_enfermero>", methods=["POST"])
def eliminar_enfermero(id_enfermero):
    db = next(get_db())
    return redirect(url_for("gestion_usuarios"))

@app.route("/gestion/ip/ultima", methods=["GET"])
def ultima():
    db = next(get_db())
    return jsonify(IPControlService.obtener_ultima_ip(db=db)), 200

@app.route("/gestion/ip/siguiente", methods=["GET"])
def siguiente():
    db = next(get_db())
    return jsonify(IPControlService.siguiente_ip(db=db)), 200

@app.route("/gestion/ip/asignar", methods=["GET"])
def asignar():
    db = next(get_db())
    return jsonify(IPControlService.asignar_ip(db=db)), 200