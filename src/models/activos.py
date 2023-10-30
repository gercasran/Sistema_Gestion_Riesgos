from src.utils.db import db
from src.models.riesgo import Riesgo
from uuid import uuid4

def getDefaultID() -> str:
    return uuid4().hex

class Activo(db.Model):
    __tablename__ = 'Activos'
    idActivo = db.Column(db.String(32), primary_key=True, default=getDefaultID)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(250), nullable=False)
    confidencialidad = db.Column(db.Integer, nullable=False)
    disponibilidad = db.Column(db.Integer, nullable=False)
    integridad = db.Column(db.Integer, nullable=False)
    sensibilidad = db.Column(db.Integer, nullable=False)
    idParticipante = db.Column(db.String(32), db.ForeignKey('Participantes.idResponsable', ondelete='SET NULL'), nullable=True)
    idProyecto = db.Column(db.String(32), db.ForeignKey('Proyectos.idProyecto', ondelete='CASCADE'), nullable=False)
    idTipoActivo = db.Column(db.Integer, db.ForeignKey('TiposActivos.idTipoActivo', ondelete='CASCADE'), nullable=False)
    idTipoUbicacion = db.Column(db.Integer, db.ForeignKey('TiposUbicacion.idTipoUbicacion', ondelete='CASCADE'), nullable=False)
    riesgos = db.relationship('Riesgo', backref='activo', cascade='all, delete-orphan')


    def __init__(self, nombre, descripcion, confidencialidad, disponibilidad, integridad, idParticipante, idProyecto, idTipoActivo, idTipoUbicacion) -> None:
        self.nombre = nombre
        self.descripcion = descripcion
        self.confidencialidad = confidencialidad
        self.disponibilidad = disponibilidad
        self.integridad = integridad
        self.sensibilidad = 0
        self.idParticipante = idParticipante
        self.idProyecto = idProyecto
        self.idTipoActivo = idTipoActivo
        self.idTipoUbicacion = idTipoUbicacion

    def calcularSensibilidad(self) -> None:
        self.sensibilidad = self.confidencialidad + self.disponibilidad + self.integridad