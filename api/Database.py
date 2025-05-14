from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from .Config import DATABASE_URL

# Crear el motor de conexión
engine = create_engine(DATABASE_URL, echo=True)

try:
    with engine.connect() as connection:
        print("✅ Conexión exitosa a MariaDB")
except OperationalError as e:
    print("❌ Error al conectar:", e)

# Crear la base para los modelos
Base = declarative_base()


# Crear la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
