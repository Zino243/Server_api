from sqlalchemy import Column, Integer, String, ForeignKey, Date, text, Time
from sqlalchemy.orm import relationship
from datetime import datetime
from api.Database import Base


class Enfermeros(Base):
    __tablename__ = 'enfermeros'

    id = Column(Integer, primary_key=True, index=True)
    fecha_de_alta = Column(Date, server_default=text("CURRENT_DATE"))
    fecha_de_baja = Column(Date, default=None)

    nombre = Column(String(100), index=True)
    apellido = Column(String(100), index=True)
    codigo = Column(String(100), unique=True, index=True)
    contrasena = Column(String(100), index=True)

    # Relaciones con cascada
    asistencias = relationship("Asistencias", cascade="all, delete", back_populates="enfermero")
    presencias = relationship("Presencias", cascade="all, delete", back_populates="enfermero")
    cookies = relationship("Cookies", cascade="all, delete", back_populates="enfermero")


class Dispositivos(Base):
    __tablename__ = 'dispositivos'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), index=True)


class Habitaciones(Base):
    __tablename__ = 'habitaciones'

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(Integer, index=True)


class Camas(Base):
    __tablename__ = 'camas'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    letra = Column(String(50), index=True)
    habitacion_id = Column(ForeignKey('habitaciones.id'))
    ip = Column(String(45), nullable=False)

    habitacion = relationship("Habitaciones")


class Asistencias(Base):
    __tablename__ = 'asistencias'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    fecha = Column(Time, default=datetime.now().time)
    hora = Column(Time, index=True)

    habitacion_id = Column(ForeignKey('habitaciones.id'), index=True)
    cama_id = Column(ForeignKey('camas.id'), index=True)
    enfermeros_id = Column(ForeignKey('enfermeros.id'))

    habitacion = relationship("Habitaciones")
    cama = relationship("Camas")
    enfermero = relationship("Enfermeros", back_populates="asistencias")


class Presencias(Base):
    __tablename__ = 'presencias'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    fecha = Column(Date, server_default=text("CURRENT_DATE"))
    hora_llamada = Column(Time, default=datetime.now().time)
    hora_presencia = Column(Time, default=datetime.now().time)

    habitacion_id = Column(ForeignKey('habitaciones.id'), index=True)
    cama_id = Column(ForeignKey('camas.id'), index=True)
    enfermeros_id = Column(ForeignKey('enfermeros.id'))

    habitacion = relationship("Habitaciones")
    cama = relationship("Camas")
    enfermero = relationship("Enfermeros", back_populates="presencias")


class Cookies(Base):
    __tablename__ = 'cookies'  # Corregido de 'cookies.json' a 'cookies'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    hora_creada = Column(Time, default=datetime.now().time)
    cookie_valor = Column(Integer, index=True)
    enfermeros_id = Column(ForeignKey('enfermeros.id'))

    enfermero = relationship("Enfermeros", back_populates="cookies")

class LlamadasTemporales(Base):
    __tablename__ = 'llamadas_temporales'

    llamada_id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    habitacion_id = Column(ForeignKey('habitaciones.id'), index=True)
    cama_id = Column(ForeignKey('camas.id'), index=True)
    enfermero_id = Column(ForeignKey('enfermeros.id'), nullable=True, index=True)  # Nuevo campo

    hora = Column(Time, default=datetime.now().time)
    estado = Column(String(20), default='pendiente')

    habitacion = relationship("Habitaciones")
    cama = relationship("Camas")
    enfermero = relationship("Enfermeros")

