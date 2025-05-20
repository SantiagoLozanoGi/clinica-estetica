from flask import Blueprint

bp = Blueprint('main', __name__)

# Aquí debes importar todos los módulos que usan el `bp`
# para que se registren sus rutas
from app.routes import auth, citas, procedimientos
