from flask import Blueprint, session, redirect, url_for, render_template, request, flash
from src.models.usuarios import Usuario
from src.models.proyectos import Proyecto
from src.utils.db import db

proyectos = Blueprint('proyectos', __name__)

@proyectos.route('/proyectos')
def vistaListaProyectos():
    if not 'user_id' in session:
        return redirect(url_for('login.vistaLogin'))
    elif 'proyecto_id' in session:
        return redirect(url_for('home.vistaHome'))
    else:
        usuario = Usuario.query.filter_by(idUsuario = session['user_id']).first()
        proyectos = usuario.proyectos
        return render_template('proyectos/listaProyectos.html', usuario=usuario, proyectos=proyectos)

@proyectos.route('/editar-proyecto/<string:idProyecto>')
def vistaEditarProyecto(idProyecto):
    if not 'user_id' in session:
        return redirect(url_for('login.vistaLogin'))
    elif 'proyecto_id' in session:
        return redirect(url_for('home.vistaHome'))
    else:
        usuario = Usuario.query.filter_by(idUsuario = session['user_id']).first()
        proyecto = Proyecto.query.filter_by(idProyecto=idProyecto).first()
        return render_template('proyectos/editarProyecto.html', usuario=usuario, proyecto=proyecto)

@proyectos.route('/anadir-proyecto', methods=['POST'])
def añadirProyecto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        p = Proyecto(nombre=nombre, descripcion=descripcion, idUsuario=session['user_id'])
        db.session.add(p)
        db.session.commit()
        flash('success')
        flash('Proyecto creado correctamente')
        return redirect(url_for('proyectos.vistaListaProyectos'))

@proyectos.route('/modificar-proyecto', methods=['POST'])
def modificarProyecto():
    if request.method == 'POST':
        idProyecto = request.form['idproyecto']
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        p = Proyecto.query.filter_by(idProyecto=idProyecto).first()
        p.nombre = nombre
        p.descripcion = descripcion
        db.session.commit()
        flash('success')
        flash('Proyecto modificado correctamente')
        return redirect(url_for('proyectos.vistaListaProyectos'))

@proyectos.route('/eliminar-proyecto/<string:idProyecto>')
def eliminarProyecto(idProyecto):
    p = Proyecto.query.filter_by(idProyecto=idProyecto).first()
    db.session.delete(p)
    db.session.commit()
    flash('danger')
    flash('Proyecto eliminado correctamente')
    return redirect(url_for('proyectos.vistaListaProyectos'))

@proyectos.route('/seleccionar-proyecto/<string:idProyecto>')
def seleccionarProyecto(idProyecto):
    session['proyecto_id'] = idProyecto
    return redirect(url_for('home.vistaHome'))