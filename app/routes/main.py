from flask import render_template
from app.routes import bp  # IMPORTA el blueprint definido en __init__.py
import logging

logger = logging.getLogger(__name__)

@bp.route('/')
def index():
    try:
        logger.info("Intentando renderizar index.html")
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error al renderizar template: {str(e)}")
        return f"Error: {str(e)}", 500
