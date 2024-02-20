from src.utils.db import db
from src.models.usuarios import Usuario
from src.models.proyectos import Proyecto


Participante = db.Table('Participantes',
    db.Column('idUsuario', db.String(32), db.ForeignKey('Usuarios.idUsuario'), primary_key=True),
    db.Column('idProyecto', db.String(32), db.ForeignKey('Proyectos.idProyecto'), primary_key=True)
)