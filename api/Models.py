from sqlalchemy import Column, Integer, String, ForeignKey, Date, text, Time
from sqlalchemy.orm import relationship
from datetime import datetime
from .Database import Base


class Enfermeros(Base):
    __tablename__ = 'enfermeros'

    # Autogenerado por la BBDD
    id = Column(Integer, primary_key=True, index=True)
    fecha_de_alta = Column(Date, server_default=text("CURRENT_DATE"))
    fecha_de_baja = Column(Date, default=None)

    # Datos necesasrios
    nombre = Column(String(100), index=True)
    apellido = Column(String(100), index=True)
    codigo = Column(String(100), unique=True, index=True)
    contrasena = Column(String(100), index=True)


class Dispositivos(Base):
    __tablename__ = 'dispositivos'

    # Autogenerado por la BBDD
    id = Column(Integer, primary_key=True, index=True)

    # Datos necesarios
    nombre = Column(String(100), index=True)


class Habitaciones(Base):
    __tablename__ = 'habitaciones'

    # Autogenerado por la BBDD
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)

    # Datos necesarios
    numero = Column(Integer, index=True)


class Camas(Base):
    __tablename__ = 'camas'

    # Autogenerado por la BBDD
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)

    # Datos necesarios
    letra = Column(String(50), index=True)
    habitacion_id = Column(ForeignKey('habitaciones.id'))

    # Relaciones
    habitacion = relationship("Habitaciones")


class Asistencias(Base):
    __tablename__ = 'asistencias'

    # Autogenerado por la BBDD
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)

    # Datos necesarios
    fecha = Column(Date, server_default=text("CURRENT_DATE"))
    hora = Column(Time, index=True)

    habitacion_id = Column(ForeignKey('habitaciones.id'), index=True)
    cama_id = Column(ForeignKey('camas.id'), index=True)
    enfermeros_id = Column(ForeignKey('enfermeros.id'))

    # Relaciones
    habitacion = relationship("Habitaciones")
    cama = relationship("Camas")
    enfermero = relationship("Enfermeros")


class Presencias(Base):
    __tablename__ = 'presencias'

    # Autogenerado por la BBDD
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    fecha = Column(Date, server_default=text("CURRENT_DATE"))
    hora_llamada = Column(Time, default=datetime.now().time)
    hora_presencia = Column(Time, default=datetime.now().time)

    # Datos necesarios
    habitacion_id = Column(ForeignKey('habitaciones.id'), index=True)
    cama_id = Column(ForeignKey('camas.id'), index=True)
    enfermeros_id = Column(ForeignKey('enfermeros.id'))

    # Relaciones
    habitacion = relationship("Habitaciones")
    cama = relationship("Camas")
    enfermero = relationship("Enfermeros")


class Cookies(Base):
    __tablename__ = 'cookies'

    # Autogenerado por la BBDD
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    hora_creada = Column(Time, default=datetime.now().time)

    # Datos necesarios
    cookie_valor = Column(Integer, index=True)
    enfermeros_id = Column(ForeignKey('enfermeros.id'))

    # Relaciones
    enfermero = relationship("Enfermeros")


class LlamadasTemporales(Base):
    __tablename__ = 'llamadas_temporales'

    # Autogenerado por la BBDD
    llamada_id = Column(Integer, autoincrement=True, primary_key=True, index=True)

    # Datos necesarios
    habitacion_id = Column(ForeignKey('habitaciones.id'), index=True)
    cama_id = Column(ForeignKey('camas.id'), index=True)

    # Relaciones
    habitacion = relationship("Habitaciones")
    cama = relationship("Camas")
