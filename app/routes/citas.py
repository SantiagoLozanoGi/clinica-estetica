from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.routes import bp
from app.models import Cita, Procedimiento, Medico, Paciente
from app.forms import CitaForm

@bp.route('/agendar', methods=['GET', 'POST'])
@login_required
def agendar():
    form = CitaForm()
    
    # Obtener datos para los select
    procedimientos = Procedimiento.query.filter_by(activo=True).all()
    medicos = Medico.query.all()
    
    form.procedimiento_id.choices = [(p.id, p.nombre) for p in procedimientos]
    form.medico_id.choices = [(m.id, f"{m.persona.nombres} {m.persona.apellidos}") for m in medicos]
    
    if form.validate_on_submit():
        paciente = Paciente.query.filter_by(persona_id=current_user.persona.id).first()
        
        cita = Cita(
            paciente_id=paciente.id,
            medico_id=form.medico_id.data,
            fecha_hora=form.fecha_hora.data,
            duracion_estimada=form.duracion_estimada.data,
            notas=form.notas.data,
            sala="Clínica Medicadiz Torre Especialistas"
        )
        
        db.session.add(cita)
        
        # Agregar procedimiento a la cita
        cita_procedimiento = CitaProcedimiento(
            cita_id=cita.id,
            procedimiento_id=form.procedimiento_id.data
        )
        db.session.add(cita_procedimiento)
        
        db.session.commit()
        flash('¡Cita agendada con éxito!', 'success')
        return redirect(url_for('citas.listar'))
    
    return render_template('citas/agendar.html', form=form)

@bp.route('/')
@login_required
def listar():
    paciente = Paciente.query.filter_by(persona_id=current_user.persona.id).first()
    citas = Cita.query.filter_by(paciente_id=paciente.id).order_by(Cita.fecha_hora.desc()).all()
    return render_template('citas/listar.html', citas=citas)

@bp.route('/<int:id>')
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
    return redirect(url_for('citas.listar'))