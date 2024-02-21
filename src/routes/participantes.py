from flask import Blueprint, session, redirect, url_for, render_template, request, flash
from src.models.usuarios import Usuario
from src.models.proyectos import Proyecto
from src.utils.db import db

participantes = Blueprint('participantes', __name__)

@participantes.route('/listar-participantes')
def vistaListaParticipantes():
    if not 'user_id' in session:
        return redirect(url_for('login.vistaLogin'))
    usuario = Usuario.query.filter_by(idUsuario = session['user_id']).first()
    if usuario.rol == 1:
        return redirect(url_for('login.logout'))
    if not 'proyecto_id' in session:
        return redirect(url_for('proyectos.vistaListaProyectos'))
    proyecto = Proyecto.query.filter_by(idProyecto = session['proyecto_id']).first()
    participantes_jefe = Usuario.query.filter_by(idJefe = usuario.idUsuario).all()
    participantes_listado = []
    for participante in participantes_jefe:
        if not participante in proyecto.usuarios:
            participantes_listado.append(participante)
    participantes_proyecto = proyecto.usuarios
    return render_template('participantes/listaParticipantes.html', usuario=usuario, participantes_listado=participantes_listado, participantes_proyecto=participantes_proyecto)

@participantes.route('/anadir-participante', methods=['POST'])
def añadirParticipante():
    if request.method == 'POST':
        idParticipante = request.form['idParticipante']
        participante = Usuario.query.filter_by(idUsuario = idParticipante).first()
        proyecto = Proyecto.query.filter_by(idProyecto = session['proyecto_id']).first()
        proyecto.usuarios.append(participante)
        db.session.commit()
        flash("success")
        flash("El participante ha sido añadido al proyecto")
        return redirect(url_for('participantes.vistaListaParticipantes'))

@participantes.route('/expulsar-participante/<string:idParticipante>')
def expulsarParticipante(idParticipante):
    participante = Usuario.query.filter_by(idUsuario = idParticipante).first()
    proyecto = Proyecto.query.filter_by(idProyecto = session['proyecto_id']).first()
    proyecto.usuarios.remove(participante)
    db.session.commit()
    flash("success")
    flash("El participante ha sido expulsado del proyecto")
    return redirect(url_for('participantes.vistaListaParticipantes'))
