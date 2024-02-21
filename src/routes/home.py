from flask import Blueprint, session, redirect, url_for, render_template, request, flash
from src.utils.db import db
from src.models.usuarios import Usuario
from src.models.proyectos import Proyecto

home = Blueprint('home', __name__)

@home.route('/home')
def vistaHome():
    if not 'user_id' in session:
        return redirect(url_for('login.vistaLogin'))
    usuario = Usuario.query.filter_by(idUsuario = session['user_id']).first()
    if usuario.rol == 1:
        return redirect(url_for('login.logout'))
    if not 'proyecto_id' in session:
        return redirect(url_for('proyectos.vistaListaProyectos'))
    proyecto = Proyecto.query.filter_by(idProyecto = session['proyecto_id']).first()
    return render_template('home/home.html', usuario=usuario, proyecto=proyecto)

@home.route('/regresar-proyectos')
def regresarProyectos():
    session.pop('proyecto_id')
    return redirect(url_for('proyectos.vistaListaProyectos'))