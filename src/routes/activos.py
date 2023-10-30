from flask import Blueprint, session, redirect, url_for, render_template, request, flash
from src.utils.db import db
from src.models.usuarios import Usuario
from src.models.proyectos import Proyecto
from src.models.activos import Activo
from src.models.tipo_activo import TipoActivo
from src.models.tipo_ubicacion import TipoUbicacion
from src.models.responsables import Participante

activos = Blueprint('activos', __name__)

cdi = {
    'confidencialidad': {
        1: "El activo no posee información confidencial y puede ser compartido públicamente sin preocupaciones.",
        2: "El activo tiene información de baja confidencialidad y puede ser compartido con personas de confianza.",
        3: "El activo presenta cierto grado de confidencialidad en la información que posee y debe ser compartido únicamente con personas autorizadas.",
        4: "El activo cuenta con un alto nivel de confidencialidad en la información que posee y solo debe ser compartido con un grupo selecto de personas o departamentos.",
        5: "El activo es sumamente confidencial en la información que tiene y solo puede ser accesible por un número muy limitado de personas con necesidad de saber.",
        6: "El activo requiere una confidencialidad muy alta y solo debe compartirse con individuos altamente autorizados.",
        7: "La información en el activo es altamente sensible y solo puede ser compartida con un pequeño grupo de personas clave.",
        8: "El activo alberga información de máxima importancia y su confidencialidad es crítica, solo permitiendo el acceso a un puñado de individuos de confianza.",
        9: "El activo contiene información extremadamente confidencial y solo puede ser accesible por una persona o entidad absolutamente autorizada."
    },
    'disponibilidad': {
        1: "La información que maneja el activo está prácticamente siempre inaccesible o inutilizable para la mayoría del personal.",
        2: "La información que maneja el activo posee una disponibilidad limitada y puede volverse inaccesible en momentos críticos.",
        3: "La información que maneja el activo generalmente se encuentra disponible, pero pueden surgir interrupciones ocasionales.",
        4: "La información que maneja el activo cuenta con una alta disponibilidad y se puede acceder en la mayoría de los casos.",
        5: "La información que maneja el activo está siempre disponible sin experimentar interrupciones significativas.",
        6: "La disponibilidad del activo es crítica y debe mantenerse constantemente para respaldar las operaciones.",
        7: "El activo debe estar siempre disponible para garantizar la continuidad de las operaciones y evitar interrupciones críticas.",
        8: "La disponibilidad del activo es esencial y se requieren medidas excepcionales para garantizar un acceso continuo.",
        9: "La disponibilidad del activo es de suprema importancia, y cualquier interrupción puede tener consecuencias graves en las operaciones."
    },
    'integridad': {
        1: "La información del activo es altamente propensa a la corrupción y a modificaciones no autorizadas.",
        2: "La información del activo tiene un nivel limitado de integridad y puede ser susceptible a cambios no autorizados en ciertas circunstancias.",
        3: "La información del activo es generalmente íntegro, pero pueden ocurrir cambios no autorizados en circunstancias excepcionales.",
        4: "La información del activo es altamente íntegro y es poco probable que se modifique no autorizadamente.",
        5: "La información del activo es extremadamente íntegro y se protege rigurosamente contra cualquier modificación no autorizada.",
        6: "La integridad de la información es crítica y cualquier modificación no autorizada debe ser prevenida a toda costa.",
        7: "El activo alberga información esencial y su integridad es de máxima importancia, asegurando que no se produzcan cambios no autorizados.",
        8: "La integridad de la información en el activo es esencial y debe protegerse con medidas de seguridad rigurosas.",
        9: "La integridad del activo es de suprema importancia y cualquier modificación no autorizada es inaceptable."
    },
    'sensibilidad': {
        3: "Los activos son relativamente menos críticos en términos de seguridad de la información. La pérdida de confidencialidad, integridad o disponibilidad de estos activos tendría un impacto negativo moderado en el proyecto.",
        4: "Los activos con esta sensibilidad son críticos para la organización. La pérdida de confidencialidad, integridad o disponibilidad de estos activos tendría un impacto negativo severo y puede ser necesaria una protección muy rigurosa.",
        5: "Los activos son de importancia moderada en términos de seguridad de la información. La pérdida de confidencialidad, integridad o disponibilidad de estos activos tendría un impacto negativo considerable en el proyecto.",
        6: "Los activos con esta sensibilidad son críticos para la organización y la pérdida de confidencialidad, integridad o disponibilidad tendría un impacto desastroso.",
        7: "Los activos con esta sensibilidad son de máxima importancia y la pérdida de confidencialidad, integridad o disponibilidad sería catastrófica.",
        8: "Los activos con esta sensibilidad son críticos para la organización. La pérdida de confidencialidad, integridad o disponibilidad de estos activos tendría un impacto negativo severo y puede requerir medidas de seguridad más estrictas.",
        9: "Los activos son de importancia moderada en términos de seguridad de la información. La pérdida de confidencialidad, integridad o disponibilidad de estos activos tendría un impacto negativo considerable en el proyecto.",
        10: "Los activos con esta sensibilidad son críticos para la organización. La pérdida de confidencialidad, integridad o disponibilidad de estos activos tendría un impacto negativo severo y puede ser necesaria una protección muy rigurosa.",
        11: "Los activos con esta sensibilidad son críticos para la organización y la pérdida de confidencialidad, integridad o disponibilidad tendría un impacto desastroso.",
        12: "Los activos con esta sensibilidad son de máxima importancia y la pérdida de confidencialidad, integridad o disponibilidad sería catastrófica.",
        13: "Los activos con esta sensibilidad son críticos para la organización y la pérdida de confidencialidad, integridad o disponibilidad tendría un impacto desastroso.",
        14: "Los activos con esta sensibilidad son de máxima importancia y la pérdida de confidencialidad, integridad o disponibilidad sería catastrófica.",
        15: "Los activos con esta sensibilidad son críticos para la organización y la pérdida de confidencialidad, integridad o disponibilidad tendría un impacto desastroso.",
        16: "Los activos con esta sensibilidad son de máxima importancia y la pérdida de confidencialidad, integridad o disponibilidad sería catastrófica.",
        17: "Los activos con esta sensibilidad son críticos para la organización y la pérdida de confidencialidad, integridad o disponibilidad tendría un impacto desastroso.",
        18: "Los activos con esta sensibilidad son de máxima importancia y la pérdida de confidencialidad, integridad o disponibilidad sería catastrófica.",
        19: "Los activos con esta sensibilidad son críticos para la organización y la pérdida de confidencialidad, integridad o disponibilidad tendría un impacto desastroso.",
        20: "Los activos con esta sensibilidad son de máxima importancia y la pérdida de confidencialidad, integridad o disponibilidad sería catastrófica.",
        21: "Los activos con esta sensibilidad son críticos para la organización y la pérdida de confidencialidad, integridad o disponibilidad tendría un impacto desastroso.",
        22: "Los activos con esta sensibilidad son de máxima importancia y la pérdida de confidencialidad, integridad o disponibilidad sería catastrófica.",
        23: "Los activos con esta sensibilidad son críticos para la organización y la pérdida de confidencialidad, integridad o disponibilidad tendría un impacto desastroso.",
        24: "Los activos con esta sensibilidad son de máxima importancia y la pérdida de confidencialidad, integridad o disponibilidad sería catastrófica.",
        25: "Los activos con esta sensibilidad son críticos para la organización y la pérdida de confidencialidad, integridad o disponibilidad tendría un impacto desastroso.",
        26: "Los activos con esta sensibilidad son de máxima importancia y la pérdida de confidencialidad, integridad o disponibilidad sería catastrófica.",
        27: "Los activos con esta sensibilidad son críticos para la organización y la pérdida de confidencialidad, integridad o disponibilidad tendría un impacto desastroso."
    }
}

@activos.route('/listar-inventario')
def vistaListaActivos():
    if not 'user_id' in session:
        return redirect(url_for('login.vistaLogin'))
    elif not 'proyecto_id' in session:
        return redirect(url_for('proyectos.vistaListaProyectos'))
    else:
        usuario = Usuario.query.filter_by(idUsuario = session['user_id']).first()
        proyecto = Proyecto.query.filter_by(idProyecto = session['proyecto_id']).first()
        activos = proyecto.activos
        return render_template('activos/listaActivos.html', usuario=usuario, activos=activos, cdi=cdi)

@activos.route('/crear-activo')
def vistaCrearActivos():
    if not 'user_id' in session:
        return redirect(url_for('login.vistaLogin'))
    elif not 'proyecto_id' in session:
        return redirect(url_for('proyectos.vistaListaProyectos'))
    else:
        usuario = Usuario.query.filter_by(idUsuario = session['user_id']).first()
        proyecto = Proyecto.query.filter_by(idProyecto = session['proyecto_id']).first()
        return render_template('activos/altaActivos.html', usuario=usuario, cdi=cdi, tiposActivo=TipoActivo.query.all(), tiposUbicacion=TipoUbicacion.query.all(), participantes=proyecto.responsables)

@activos.route('/borrar-activo')
def vistaBorrarActivos():
    if not 'user_id' in session:
        return redirect(url_for('login.vistaLogin'))
    elif not 'proyecto_id' in session:
        return redirect(url_for('proyectos.vistaListaProyectos'))
    else:
        usuario = Usuario.query.filter_by(idUsuario = session['user_id']).first()
        proyecto = Proyecto.query.filter_by(idProyecto = session['proyecto_id']).first()
        activos = proyecto.activos
        return render_template('activos/listaBorrarActivos.html', usuario=usuario, activos=activos, cdi=cdi)

@activos.route('/editar-activo')
def vistaEditarActivos():
    if not 'user_id' in session:
        return redirect(url_for('login.vistaLogin'))
    elif not 'proyecto_id' in session:
        return redirect(url_for('proyectos.vistaListaProyectos'))
    else:
        usuario = Usuario.query.filter_by(idUsuario = session['user_id']).first()
        proyecto = Proyecto.query.filter_by(idProyecto = session['proyecto_id']).first()
        activos = proyecto.activos
        return render_template('activos/listaEdicionActivos.html', usuario=usuario, activos=activos, cdi=cdi)

@activos.route('/modificar-activo/<string:idActivo>')
def vistaModificacionActivos(idActivo):
    if not 'user_id' in session:
        return redirect(url_for('login.vistaLogin'))
    elif not 'proyecto_id' in session:
        return redirect(url_for('proyectos.vistaListaProyectos'))
    else:
        usuario = Usuario.query.filter_by(idUsuario = session['user_id']).first()
        activo = Activo.query.filter_by(idActivo=idActivo).first()
        return render_template('activos/edicionActivos.html', usuario=usuario, activo=activo, cdi=cdi, tiposActivo=TipoActivo.query.all(), tiposUbicacion=TipoUbicacion.query.all(), participantes=Participante.query.all())

@activos.route('/anadir-activos', methods=['POST'])
def añadirActivos():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        confidencialidad = request.form['confidencialidad']
        disponibilidad = request.form['disponibilidad']
        integridad = request.form['integridad']
        idParticipante = request.form['idParticipante']
        idTipoActivo = request.form['idTipoActivo']
        idTipoUbicacion = request.form['idTipoUbicacion']
        a = Activo(
            nombre=nombre,
            descripcion=descripcion,
            confidencialidad=int(confidencialidad),
            disponibilidad=int(disponibilidad),
            integridad=int(integridad),
            idParticipante=idParticipante,
            idTipoActivo=int(idTipoActivo),
            idTipoUbicacion=int(idTipoUbicacion),
            idProyecto=session['proyecto_id']
        )
        a.calcularSensibilidad()
        db.session.add(a)
        db.session.commit()
        flash('success')
        flash('El activo ha sido añadido correctamente')
        return redirect(url_for('activos.vistaListaActivos'))

@activos.route('/actualizar-activos', methods=['POST'])
def modificarActivos():
    if request.method == 'POST':
        idActivo = request.form['idactivo']
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        confidencialidad = request.form['confidencialidad']
        disponibilidad = request.form['disponibilidad']
        integridad = request.form['integridad']
        idParticipante = request.form['idParticipante']
        idTipoActivo = request.form['idTipoActivo']
        idTipoUbicacion = request.form['idTipoUbicacion']
        a = Activo.query.filter_by(idActivo=idActivo).first()
        a.nombre=nombre
        a.descripcion=descripcion
        a.confidencialidad=int(confidencialidad)
        a.disponibilidad=int(disponibilidad)
        a.integridad=int(integridad)
        a.idParticipante = idParticipante
        a.idTipoActivo=int(idTipoActivo)
        a.idTipoUbicacion=int(idTipoUbicacion)
        a.calcularSensibilidad()
        db.session.commit()
        flash('success')
        flash('El activo ha sido modificado correctamente')
        return redirect(url_for('activos.vistaListaActivos'))


@activos.route('/eliminar-activo/<string:idActivo>')
def eliminarActivo(idActivo):
    a = Activo.query.filter_by(idActivo=idActivo).first()
    db.session.delete(a)
    db.session.commit()
    flash('danger')
    flash('El activo ha sido eliminado correctamente')
    return redirect(url_for('activos.vistaListaActivos'))