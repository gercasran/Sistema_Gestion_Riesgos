from flask import Blueprint, session, redirect, url_for, render_template, request, flash
from src.models.usuarios import Usuario
from src.models.proyectos import Proyecto
from src.utils.db import db

responsables = Blueprint('responsables', __name__)

@responsables.route('/listar-responsables')
def vistaListaResponsables():
    if not 'user_id' in session:
        return redirect(url_for('login.vistaLogin'))
    usuario = Usuario.query.filter_by(idUsuario = session['user_id']).first()
    if usuario.rol == 1:
        return redirect(url_for('login.logout'))
    if not 'proyecto_id' in session:
        return redirect(url_for('proyectos.vistaListaProyectos'))
    proyecto = Proyecto.query.filter_by(idProyecto = session['proyecto_id']).first()
    responsables = proyecto.usuarios.filter_by(rol=1).all()
    return render_template('responsables/listaResponsables.html', usuario=usuario, responsables=responsables)

@responsables.route('/edicion-responsable/<string:idResponsable>')
def vistaEdicionResponsables(idResponsable):
    if not 'user_id' in session:
        return redirect(url_for('login.vistaLogin'))
    usuario = Usuario.query.filter_by(idUsuario = session['user_id']).first()
    if usuario.rol == 1:
        return redirect(url_for('login.logout'))
    if not 'proyecto_id' in session:
        return redirect(url_for('proyectos.vistaListaProyectos'))
    proyecto = Proyecto.query.filter_by(idProyecto = session['proyecto_id']).first()
    responsable = proyecto.usuarios.filter_by(idResponsable=idResponsable).first()
    return render_template('responsables/modificarResponsables.html', usuario=usuario, responsable=responsable)

@responsables.route('/anadir-responsable', methods=['POST'])
def añadirResponsable():
    if request.method == 'POST':
        nombre = request.form['nombre']
        aPaterno = request.form['aPaterno']
        aMaterno = request.form['aMaterno']
        email = request.form['email']
        telefono = request.form['tel']
        password = request.form['password']
        
        emailExiste = Usuario.query.filter_by(correo=email).first()

        if emailExiste:
            flash('danger')
            flash('El correo que ingreso ya existe en el sistema')
            return redirect(url_for('responsables.vistaListaResponsables'))

        u = Usuario(
            nombre=nombre,
            apellidoPaterno=aPaterno,
            apelidoMaterno=aMaterno,
            correo=email,
            telefono=telefono,
            contrasena=password,
            rol=1
        )
        db.session.add(u)

        proyecto = Proyecto.query.filter_by(idProyecto = session['proyecto_id']).first()
        proyecto.usuarios.append(u)

        db.session.commit()
        flash('success')
        flash('El participante fue añadido correctamente')
        return redirect(url_for('responsables.vistaListaResponsables'))

@responsables.route('/actualizar-responsable', methods=['POST'])
def modificarResponsable():
    if request.method == 'POST':
        idResponsable = request.form['idResponsable']
        nombre = request.form['nombre']
        aPaterno = request.form['aPaterno']
        aMaterno = request.form['aMaterno']
        email = request.form['email']
        telefono = request.form['tel']
        password = request.form['password']
        responsable = Usuario.query.filter_by(idUsuario=idResponsable).first()
        responsable.nombre = nombre
        responsable.aPaterno = aPaterno
        responsable.aMaterno = aMaterno
        responsable.telefono = telefono
        responsable.correo = email
        responsable.password = password
        db.session.commit()
        flash('success')
        flash('El participante fue modificado correctamente')
        return redirect(url_for('responsables.vistaListaResponsables'))

@responsables.route('/eliminar-responsable/<string:idResponsable>')
def eliminarResponsable(idResponsable):
    responsable = Usuario.query.filter_by(idUsuario=idResponsable).first()
    proyecto = Proyecto.query.filter_by(idProyecto = session['proyecto_id']).first()
    proyecto.usuarios.remove(responsable)
    db.session.delete(responsable)
    db.session.commit()
    flash('danger')
    flash('El participante fue eliminado correctamente')
    return redirect(url_for('responsables.vistaListaResponsables'))