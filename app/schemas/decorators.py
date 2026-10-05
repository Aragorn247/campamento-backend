from functools import wraps
from flask import request, jsonify

def validate_json(validation_func):
    """
    Decorador reutilizable para validar la entrada JSON de un endpoint.
    Si hay errores de validación, responde inmediatamente con estado 400.
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = request.get_json(silent=True)
            errors = validation_func(data)
            
            if errors:
                return jsonify({
                    "error": "Bad Request",
                    "message": "Error de validación en los datos enviados.",
                    "details": errors,
                    "status_code": 400
                }), 400
                
            return f(*args, **kwargs)
        return wrapper
    return decorator