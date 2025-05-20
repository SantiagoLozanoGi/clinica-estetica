from flask import Blueprint

bp = Blueprint('main', __name__)  # este será el ÚNICO objeto bp

# importa después de definir `bp`, para evitar bucles de importación
from app.routes import main, auth, citas, procedimientos

