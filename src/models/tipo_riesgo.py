from src.utils.db import db
from src.models.riesgo import Riesgo

class TipoRiesgo(db.Model):
    __tablename__ = 'TiposRiesgo'
    idTipoRiesgo = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(32), nullable=False)
    riesgos = db.relationship('Riesgo', backref='tipoRiesgo', cascade='all, delete-orphan')

    def __init__(self, nombre) -> None:
        self.nombre = nombre