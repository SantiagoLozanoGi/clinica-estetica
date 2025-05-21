
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from datetime import datetime
from app import db # Asegúrate de que 'db' se ha inicializado correctamente (Flask-SQLAlchemy)
from app.routes import bp
from app.models import Cita, Procedimiento, Medico, Paciente, CitaProcedimiento, Persona
from app.forms import CitaForm
import logging
from app.forms import CitaForm

logger = logging.getLogger(__name__)

@bp.route('/agendar', methods=['GET', 'POST'])
@login_required
def agendar():
    form = CitaForm()

    # Obtener datos para los select
    procedimientos = Procedimiento.query.filter_by(activo=True).all()
    medicos = Medico.query.all()

    form.procedimiento_id.choices = [(p.id, p.nombre) for p in procedimientos]
    form.medico_id.choices = [(m.id, f"{m.persona.nombres} {m.persona.apellidos}") for m in medicos]

    # Cargar los datos del paciente si ya existe para precargar el formulario (solo en GET o si la validación falla)
    paciente_existente = None
    if current_user.is_authenticated and current_user.persona:
        paciente_existente = Paciente.query.filter_by(persona_id=current_user.persona.id).first()
    
    # Pre-llenar el formulario solo si es un GET request o si la validación falló (para no perder datos ingresados)
    if request.method == 'GET' and paciente_existente:
        logger.info(f"Precargando datos del paciente ID: {paciente_existente.id} en el formulario.")
        form.tipo_sangre.data = paciente_existente.tipo_sangre
        form.alergias.data = paciente_existente.alergias
        form.medicamentos_actuales.data = paciente_existente.medicamentos_actuales
        form.historial_estetica_previo.data = paciente_existente.historial_estetica_previo
        form.motivo_consulta.data = paciente_existente.motivo_consulta
        form.referido_por.data = paciente_existente.referido_por

    if form.validate_on_submit():
        logger.info("Formulario validado correctamente. Intentando guardar cita y/o actualizar paciente...")
        logger.info(f"Datos del formulario recibidos: {form.data}") # Útil para depuración

        paciente = paciente_existente # Usamos el paciente_existente si ya lo obtuvimos

        try:
            # Si el paciente no existe, lo creamos
            if not paciente:
                logger.info("Paciente no encontrado, creando un nuevo registro de Paciente.")
                # Asegúrate de que current_user.persona exista. Si no, esto fallaría.
                # Tu RegistrationForm ya crea Persona asociada, lo cual es bueno.
                if not current_user.persona:
                    flash('Error: Su perfil de usuario no tiene información personal asociada. Por favor, complete su perfil primero.', 'danger')
                    logger.error("current_user.persona es None. No se puede crear Paciente sin Persona.")
                    return redirect(url_for('main.index')) # O a una página de perfil para que lo complete

                paciente = Paciente(persona_id=current_user.persona.id)
                db.session.add(paciente)
                db.session.flush() # Necesario para que paciente.id esté disponible antes de la cita
                logger.info(f"Nuevo paciente creado con ID: {paciente.id}")
            else:
                logger.info(f"Paciente existente encontrado con ID: {paciente.id}. Procediendo a actualizar datos.")

            # Actualizar o asignar los datos del paciente con la información del formulario
            # Asignamos directamente, si el campo está vacío en el formulario, se guardará como None/vacío en DB
            # si la columna lo permite. Si una columna es NOT NULL y el campo está vacío, puede dar error.
            paciente.tipo_sangre = form.tipo_sangre.data if form.tipo_sangre.data else None
            paciente.alergias = form.alergias.data if form.alergias.data else None
            paciente.medicamentos_actuales = form.medicamentos_actuales.data if form.medicamentos_actuales.data else None
            paciente.historial_estetica_previo = form.historial_estetica_previo.data if form.historial_estetica_previo.data else None
            paciente.motivo_consulta = form.motivo_consulta.data if form.motivo_consulta.data else None
            paciente.referido_por = form.referido_por.data if form.referido_por.data else None
            
            # Nota: No necesitas db.session.add(paciente) de nuevo si ya lo obtuviste o lo creaste en esta sesión
            # SQLAlchemy ya lo está rastreando.

            # Crear la cita
            cita = Cita(
                paciente_id=paciente.id, # Usamos el ID del paciente (ya sea nuevo o existente)
                medico_id=form.medico_id.data,
                fecha_hora=form.fecha_hora.data,
                duracion_estimada=form.duracion_estimada.data,
                notas=form.notas.data,
                sala="Clínica Medicadiz Torre Especialistas"
            )
            db.session.add(cita)
            db.session.flush() # Asegura que cita.id esté disponible

            # Asociar procedimiento a la cita
            cita_procedimiento = CitaProcedimiento(
                cita_id=cita.id,
                procedimiento_id=form.procedimiento_id.data
            )
            db.session.add(cita_procedimiento)

            db.session.commit() # Guarda todos los cambios: paciente (si actualizado) y cita, cita_procedimiento

            flash('¡Cita agendada con éxito!', 'success')
            logger.info("Cita, procedimientos y datos del paciente guardados/actualizados en DB.")
            return redirect(url_for('main.listar'))

        except Exception as e:
            db.session.rollback() # Deshace cualquier cambio en la base de datos si ocurre un error
            logger.error(f"Error al procesar la cita o actualizar paciente: {e}", exc_info=True) # exc_info=True para el traceback
            flash(f'Ocurrió un error al agendar la cita. Por favor, inténtelo de nuevo. Detalles: {e}', 'danger')
            # Renderiza el formulario con los errores de validación si los hubiera
            return render_template('citas/agendar.html', form=form)

    else:
        # Si el formulario no es válido (GET request o POST con errores de validación)
        logger.warning(f"Formulario de cita NO validado. Errores: {form.errors}")
        # Los errores del formulario se mostrarán en el template gracias a las modificaciones que te di para agendar.html

    return render_template('citas/agendar.html', form=form)


@bp.route('/mis_citas', methods=['GET'])
@login_required
def listar():
    paciente = Paciente.query.filter_by(persona_id=current_user.persona.id).first()
    citas = Cita.query.filter_by(paciente_id=paciente.id).order_by(Cita.fecha_hora.desc()).all()
    return render_template('citas/listar.html', citas=citas)

@bp.route('/mis_citas/<int:id>')
@login_required
def detalle(id):
    cita = Cita.query.get_or_404(id)
    return render_template('citas/detalle.html', cita=cita)

@bp.route('/cancelar/<int:id>', methods=['POST'])
@login_required
def cancelar(id):
    cita = Cita.query.get_or_404(id)
    cita.estado = 'cancelada'
    db.session.commit()
    flash('Cita cancelada exitosamente', 'success')
    return redirect(url_for('main.listar'))
