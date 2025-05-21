from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from app.routes import bp # IMPORTA el blueprint definido en __init__.py
from app.models import Procedimiento, Tratamiento

# Ruta para listar procedimientos
# CAMBIO: Ahora la URL es '/procedimientos' en lugar de '/'
@bp.route('/procedimientos', endpoint='procedimientos')
@login_required
def listar():
    procedimientos = Procedimiento.query.filter_by(activo=True).all()
    tratamientos = Tratamiento.query.all() # Asumiendo que necesitas tratamientos también aquí
    return render_template('procedimientos/listar.html', 
                            procedimientos=procedimientos, 
                            tratamientos=tratamientos)

# Ruta para ver el detalle de un procedimiento específico
# CAMBIO: La URL ahora es '/procedimientos/<int:id>'
@bp.route('/procedimientos/<int:id>', endpoint='detalleprocedimiento')
@login_required
def detalle(id):
    procedimiento = Procedimiento.query.get_or_404(id)
    return render_template('procedimientos/detalle.html', procedimiento=procedimiento)

