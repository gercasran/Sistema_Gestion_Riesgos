from flask import Blueprint, session, redirect, url_for, render_template, request, flash
from src.models.usuarios import Usuario
from src.models.proyectos import Proyecto
from src.models.responsables import Participante
from src.models.activos import Activo
from src.utils.db import db

responsables = Blueprint('responsables', __name__)

@responsables.route('/listar-responsables')
def vistaListaResponsables():
    if not 'user_id' in session:
        return redirect(url_for('login.vistaLogin'))
    elif not 'proyecto_id' in session:
        return redirect(url_for('proyectos.vistaListaProyectos'))
    else:
        usuario = Usuario.query.filter_by(idUsuario = session['user_id']).first()
        proyecto = Proyecto.query.filter_by(idProyecto = session['proyecto_id']).first()
        responsables = proyecto.responsables
        return render_template('responsables/listaResponsables.html', usuario=usuario, responsables=responsables)

@responsables.route('/crear-responsable')
def vistaCrearResponsables():
    if not 'user_id' in session:
        return redirect(url_for('login.vistaLogin'))
    elif not 'proyecto_id' in session:
        return redirect(url_for('proyectos.vistaListaProyectos'))
    else:
        usuario = Usuario.query.filter_by(idUsuario = session['user_id']).first()
        return render_template('responsables/altaResponsables.html', usuario=usuario)

@responsables.route('/borrar-responsable')
def vistaBorrarResponsables():
    if not 'user_id' in session:
        return redirect(url_for('login.vistaLogin'))
    elif not 'proyecto_id' in session:
        return redirect(url_for('proyectos.vistaListaProyectos'))
    else:
        usuario = Usuario.query.filter_by(idUsuario = session['user_id']).first()
        proyecto = Proyecto.query.filter_by(idProyecto = session['proyecto_id']).first()
        responsables = proyecto.responsables
        return render_template('responsables/listaBorrarResponsables.html', usuario=usuario, responsables=responsables)

@responsables.route('/editar-responsable')
def vistaEditarResponsables():
    if not 'user_id' in session:
        return redirect(url_for('login.vistaLogin'))
    elif not 'proyecto_id' in session:
        return redirect(url_for('proyectos.vistaListaProyectos'))
    else:
        usuario = Usuario.query.filter_by(idUsuario = session['user_id']).first()
        proyecto = Proyecto.query.filter_by(idProyecto = session['proyecto_id']).first()
        responsables = proyecto.responsables
        return render_template('responsables/listaEdicionResponsables.html', usuario=usuario, responsables=responsables)

@responsables.route('/edicion-responsable/<string:idResponsable>')
def vistaEdicionResponsables(idResponsable):
    if not 'user_id' in session:
        return redirect(url_for('login.vistaLogin'))
    elif not 'proyecto_id' in session:
        return redirect(url_for('proyectos.vistaListaProyectos'))
    else:
        usuario = Usuario.query.filter_by(idUsuario = session['user_id']).first()
        responsable = Participante.query.filter_by(idResponsable=idResponsable).first()
        return render_template('responsables/modificarResponsables.html', usuario=usuario, responsable=responsable)

@responsables.route('/anadir-responsable', methods=['POST'])
def añadirResponsable():
    if request.method == 'POST':
        nombre = request.form['nombre']
        departamento = request.form['departamento']
        telefono = request.form['telefono']
        email = request.form['email']
        
        r = Participante(
            nombre=nombre,
            departamento=departamento,
            telefono=telefono,
            correo=email,
            idProyecto=session['proyecto_id']
        )
        db.session.add(r)
        db.session.commit()
        flash('success')
        flash('El participante fue añadido correctamente')
        return redirect(url_for('responsables.vistaListaResponsables'))

@responsables.route('/actualizar-responsable', methods=['POST'])
def modificarResponsable():
    if request.method == 'POST':
        idResponsable = request.form['idResponsable']
        nombre = request.form['nombre']
        departamento = request.form['departamento']
        telefono = request.form['telefono']
        email = request.form['email']
        responsable = Participante.query.filter_by(idResponsable=idResponsable).first()
        responsable.nombre = nombre
        responsable.departamento = departamento
        responsable.telefono = telefono
        responsable.correo = email
        db.session.commit()
        flash('success')
        flash('El participante fue modificado correctamente')
        return redirect(url_for('responsables.vistaListaResponsables'))

@responsables.route('/eliminar-responsable/<string:idResponsable>')
def eliminarResponsable(idResponsable):
    responsable = Participante.query.filter_by(idResponsable=idResponsable).first()
    for activo in responsable.activos:
        activo.idParticipante = None
    db.session.delete(responsable)
    db.session.commit()
    flash('danger')
    flash('El participante fue eliminado correctamente')
    return redirect(url_for('responsables.vistaListaResponsables'))