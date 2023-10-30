from src.utils.db import db
from src.models.activos import Activo

class TipoActivo(db.Model):
    __tablename__ = 'TiposActivos'
    idTipoActivo = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(32), nullable=False)
    activos = db.relationship('Activo', backref='tipoActivo', cascade='all, delete-orphan')

    def __init__(self, nombre) -> None:
        self.nombre = nombre