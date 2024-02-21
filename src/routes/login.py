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
        if usuario.rol == 0:
            return redirect(url_for('proyectos.vistaListaProyectos'))
        else:
            return redirect(url_for('proyectosP.vistaListaProyectos'))

@login.route('/logout')
def logoutUser():
    session.clear()
    return redirect(url_for('login.vistaLogin'))