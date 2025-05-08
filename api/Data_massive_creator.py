import random
from datetime import datetime, timedelta, time

from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import Config
from Models import Enfermeros, Habitaciones, Camas, Asistencias, Presencias, Cookies, LlamadasTemporales

DB_URL = Config.DATABASE_URL

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
session = Session()
faker = Faker('es_ES')

# Crear habitaciones
habitaciones = []
for i in range(5):
    h = Habitaciones(numero=100 + i)
    session.add(h)
    habitaciones.append(h)

session.commit()

# Crear camas (3 por habitación)
camas = []
letras = ['A', 'B', 'C']
for hab in habitaciones:
    for letra in letras:
        c = Camas(letra=letra, habitacion_id=hab.id)
        session.add(c)
        camas.append(c)

session.commit()

# Crear enfermeros
enfermeros = []
for i in range(10):
    nombre = faker.first_name()
    apellido = faker.last_name()
    codigo = f"ENF{1000 + i}"
    contrasena = faker.password()
    e = Enfermeros(nombre=nombre, apellido=apellido, codigo=codigo, contrasena=contrasena)
    session.add(e)
    enfermeros.append(e)

session.commit()

# Crear asistencias
for _ in range(100):
    a = Asistencias(
        fecha=faker.date_between(start_date='-30d', end_date='today'),
        hora=time(hour=random.randint(6, 22), minute=random.randint(0, 59)),
        habitacion_id=random.choice(habitaciones).id,
        cama_id=random.choice(camas).id,
        enfermeros_id=random.choice(enfermeros).id
    )
    session.add(a)

# Crear presencias
for _ in range(80):
    hora_llamada = time(hour=random.randint(6, 22), minute=random.randint(0, 59))
    delta_min = random.randint(1, 5)
    hora_presencia = (datetime.combine(datetime.today(), hora_llamada) + timedelta(minutes=delta_min)).time()

    p = Presencias(
        fecha=faker.date_between(start_date='-30d', end_date='today'),
        hora_llamada=hora_llamada,
        hora_presencia=hora_presencia,
        habitacion_id=random.choice(habitaciones).id,
        cama_id=random.choice(camas).id,
        enfermeros_id=random.choice(enfermeros).id
    )
    session.add(p)

# Crear cookies
for _ in range(20):
    c = Cookies(
        hora_creada=time(hour=random.randint(6, 23), minute=random.randint(0, 59)),
        cookie_valor=random.randint(100000, 999999),
        enfermeros_id=random.choice(enfermeros).id
    )
    session.add(c)

# Crear llamadas temporales
for _ in range(30):
    lt = LlamadasTemporales(
        habitacion_id=random.choice(habitaciones).id,
        cama_id=random.choice(camas).id
    )
    session.add(lt)

session.commit()
print("Datos generados correctamente.")
