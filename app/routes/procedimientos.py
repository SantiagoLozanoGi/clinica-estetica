from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from app.routes import bp
from app.models import Procedimiento, Tratamiento

@bp.route('/', endpoint='procedimientos')
@login_required
def listar():
    procedimientos = Procedimiento.query.filter_by(activo=True).all()
    tratamientos = Tratamiento.query.all()
    return render_template('procedimientos/listar.html', 
                        procedimientos=procedimientos, 
                        tratamientos=tratamientos)

@bp.route('/<int:id>', endpoint='detalleprocedimiento')
@login_required
def detalle(id):
    procedimiento = Procedimiento.query.get_or_404(id)
    return render_template('procedimientos/detalle.html', procedimiento=procedimiento)