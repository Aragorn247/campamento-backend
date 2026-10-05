from flask import jsonify
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        """Captura errores HTTP estándar (404, 400, 403, etc.)"""
        response = {
            "error": e.name,
            "message": e.description,
            "status_code": e.code
        }
        return jsonify(response), e.code

    @app.errorhandler(Exception)
    def handle_generic_exception(e):
        """Captura cualquier error no controlado (500)"""
        # En entorno de producción se loguea la excepción
        response = {
            "error": "Internal Server Error",
            "message": "Ha ocurrido un error inesperado en el servidor.",
            "status_code": 500
        }
        return jsonify(response), 500