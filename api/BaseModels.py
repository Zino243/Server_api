from datetime import date, time
from pydantic import BaseModel, Field

class Enfermero(BaseModel):
    fecha_de_alta: date = Field(default_factory=date.today)
    fecha_de_baja: date | None = None
    nombre: str
    apellido: str
    codigo: str
    contrasena: str

class Dispositivo(BaseModel):
    nombre: str

class Habitacion(BaseModel):
    numero: int  # no 'letra' aquí, era 'numero' según tu modelo SQLAlchemy

class Cama(BaseModel):
    letra: str
    habitacion_id: int  # FK necesaria para saber a qué habitación pertenece

class Asistencia(BaseModel):
    fecha: date = Field(default_factory=date.today)
    hora: time
    habitacion_id: int
    cama_id: int
    enfermeros_id: int

class Presencia(BaseModel):
    fecha: date = Field(default_factory=date.today)
    hora_llamada: time
    hora_presencia: time
    habitacion_id: int
    cama_id: int
    enfermeros_id: int

class Cookie(BaseModel):
    hora_creada: time
    cookie_valor: int
    enfermeros_id: int

class LlamadaTemporal(BaseModel):
    habitacion_id: int
    cama_id: int
