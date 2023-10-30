from flask import Blueprint, session, redirect, url_for, render_template, request, flash
from src.models.usuarios import Usuario
from src.utils.db import db

login = Blueprint('login', __name__)

@login.route('/')
def vistaLogin():
    if not 'user_id' in session:
        return render_template('login/login.html')
    else:
        return redirect(url_for('proyectos.vistaListaProyectos'))

@login.route('/register')
def vistaSignUp():
    if not 'user_id' in session:
        return render_template('login/signUp.html')
    else:
        return redirect(url_for('proyectos.vistaListaProyectos'))

@login.route('/login', methods=['POST'])
def loginUser():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        usuario = Usuario.query.filter_by(correo=email).first()

        if not usuario or not usuario.verificarContrasena(password):
            flash('danger')
            flash('Correo o contraseña incorrectas')
            return redirect(url_for('login.vistaLogin'))

        session['user_id'] = usuario.idUsuario
        return redirect(url_for('proyectos.vistaListaProyectos'))

@login.route('/signup', methods=['POST'])
def signUpUser():
    if request.method == 'POST':
        nombre = request.form['nombre']
        aPaterno = request.form['aPaterno']
        aMaterno = request.form['aMaterno']
        email = request.form['email']
        password = request.form['password']
        
        emailExiste = Usuario.query.filter_by(correo=email).first()

        if emailExiste:
            flash('danger')
            flash('El correo que ingreso ya existe en el sistema')
            return redirect(url_for('login.vistaSignUp'))

        u = Usuario(
            nombre=nombre,
            apellidoPaterno=aPaterno,
            apelidoMaterno=aMaterno,
            correo=email,
            contrasena=password
        )
        db.session.add(u)
        db.session.commit()
        flash('success')
        flash('Se ha registrado exitosamente')
        return redirect(url_for('login.vistaLogin'))

@login.route('/logout')
def logoutUser():
    session.clear()
    return redirect(url_for('login.vistaLogin'))