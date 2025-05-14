import random
from datetime import datetime, time, timedelta
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import Config  # Este módulo debe definir DATABASE_URL
from api.Database import Base
from api.Models import (
    Enfermeros,
    Dispositivos,
    Habitaciones,
    Camas,
    Asistencias,
    Presencias,
    Cookies,
    LlamadasTemporales
)

# Configuración de la base de datos
DB_URL = Config.DATABASE_URL
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
session = Session()

faker = Faker('es_ES')

# Función para generar un valor de tiempo aleatorio entre una hora de inicio y fin
def random_time(start_hour=6, end_hour=22):
    hour = random.randint(start_hour, end_hour)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return time(hour, minute, second)

# -----------------------------
# 1. Crear Habitaciones (mínimo 7)
# -----------------------------
habitaciones = []
for i in range(7):
    hab = Habitaciones(numero=100 + i)
    session.add(hab)
    habitaciones.append(hab)
session.commit()

# -----------------------------
# 2. Crear Camas (3 por cada habitación → mínimo 21 camas)
# -----------------------------
camas = []
letras = ['A', 'B', 'C']
for hab in habitaciones:
    for letra in letras:
        # Generamos una IP aleatoria en el rango de clase B
        ip = f"172.16.{random.randint(0, 255)}.{random.randint(0, 255)}"

        # Creamos la cama y le asignamos la IP
        cama = Camas(letra=letra, habitacion_id=hab.id, ip=ip)

        # Añadimos la cama a la sesión y a la lista de camas
        session.add(cama)
        camas.append(cama)

# Confirmamos los cambios en la base de datos
session.commit()

# -----------------------------
# 3. Crear Enfermeros (mínimo 7)
# -----------------------------
enfermeros = []
for i in range(7):
    nombre = faker.first_name()
    apellido = faker.last_name()
    codigo = f"ENF{1000 + i}"
    contrasena = faker.password()
    enf = Enfermeros(nombre=nombre, apellido=apellido, codigo=codigo, contrasena=contrasena)
    session.add(enf)
    enfermeros.append(enf)
session.commit()

# -----------------------------
# 4. Crear Dispositivos (mínimo 7)
# -----------------------------
dispositivos = []
for i in range(7):
    disp = Dispositivos(nombre=f"Dispositivo {i+1}")
    session.add(disp)
    dispositivos.append(disp)
session.commit()

# -----------------------------
# 5. Crear Asistencias (mínimo 7)
# Nota: En el modelo, 'fecha' es de tipo Time, por lo que generamos una hora aleatoria.
# -----------------------------
for _ in range(7):
    asistencia = Asistencias(
        fecha=random_time(),       # Valor de tiempo (por ejemplo, '14:30:15')
        hora=random_time(),        # Valor de hora adicional
        habitacion_id=random.choice(habitaciones).id,
        cama_id=random.choice(camas).id,
        enfermeros_id=random.choice(enfermeros).id
    )
    session.add(asistencia)
session.commit()

# -----------------------------
# 6. Crear Presencias (mínimo 7)
# Aquí 'fecha' es de tipo Date y se generan horas para las llamadas y presencia.
# -----------------------------
for _ in range(7):
    hora_llamada = random_time()
    delta = random.randint(1, 5)
    dt_llamada = datetime.combine(datetime.today(), hora_llamada)
    dt_presencia = dt_llamada + timedelta(minutes=delta)
    presencia = Presencias(
        fecha=faker.date_object(),  # Un objeto date válido
        hora_llamada=hora_llamada,
        hora_presencia=dt_presencia.time(),
        habitacion_id=random.choice(habitaciones).id,
        cama_id=random.choice(camas).id,
        enfermeros_id=random.choice(enfermeros).id
    )
    session.add(presencia)
session.commit()

# -----------------------------
# 7. Crear Cookies (mínimo 7)
# -----------------------------
for _ in range(7):
    cookie = Cookies(
        hora_creada=random_time(),
        cookie_valor=random.randint(100000, 999999),
        enfermeros_id=random.choice(enfermeros).id
    )
    session.add(cookie)
session.commit()

# -----------------------------
# 8. Crear LlamadasTemporales (mínimo 7)
# -----------------------------
for _ in range(7):
    lt = LlamadasTemporales(
        habitacion_id=random.choice(habitaciones).id,
        cama_id=random.choice(camas).id,
        hora=random_time()
    )
    session.add(lt)
session.commit()

print("Datos generados correctamente.")
