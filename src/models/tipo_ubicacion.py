from src.utils.db import db
from src.models.activos import Activo

class TipoUbicacion(db.Model):
    __tablename__ = 'TiposUbicacion'
    idTipoUbicacion = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(32), nullable=False)
    activos = db.relationship('Activo', backref='tipoUbicacion', cascade='all, delete-orphan')

    def __init__(self, nombre) -> None:
        self.nombre = nombre