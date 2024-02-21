from src.models.usuarios import Usuario
from src.utils.db import db
from app import app

with app.app_context():
    nombre = input("Ingrese el nombre: ")
    aPaterno = input("Ingrese el apellido paterno: ")
    aMaterno = input("Ingrese el apellido materno: ")
    email = input("Ingrese el correo electronico: ")
    telefono = input("Ingrese el telefono: ")
    password = input("Ingrese el contraseña: ")

    u = Usuario(
        nombre=nombre,
        apellidoPaterno=aPaterno,
        apelidoMaterno=aMaterno,
        correo=email,
        telefono=telefono,
        contrasena=password,
        rol=0
    )

    db.session.add(u)
    db.session.commit()