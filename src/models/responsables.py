from src.utils.db import db
from uuid import uuid4

def getDefaultID() -> str:
    return uuid4().hex

class Participante(db.Model):
    __tablename__ = 'Participantes'
    idResponsable = db.Column(db.String(32), primary_key=True, default=getDefaultID)
    nombre = db.Column(db.String(100), nullable=False)
    departamento = db.Column(db.String(100), nullable=False)
    telefono= db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    idProyecto = db.Column(db.String(32), db.ForeignKey('Proyectos.idProyecto', ondelete='CASCADE'), nullable=False)
    activos = db.relationship('Activo', backref='dueño_responsable', passive_deletes=True)

    def __init__(self, nombre, departamento, telefono, correo, idProyecto) -> None:
        self.nombre = nombre
        self.departamento = departamento
        self.telefono = telefono
        self.correo = correo
        self.idProyecto = idProyecto