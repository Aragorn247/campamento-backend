from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from flask_migrate import Migrate

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "API Campamento - Sprint 8",
        "description": "Documentación interactiva de la API Backend del Campamento",
        "version": "1.0.0"
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Formato: Bearer <JWT_TOKEN>"
        }
    }
}

swagger = Swagger(template=swagger_template)