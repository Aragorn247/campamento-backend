from flask import Flask, jsonify
from app.config import config_by_name
from app.extensions import db, jwt, swagger, migrate
from app.errors import register_error_handlers
from app.routes.auth import auth_bp
from app.routes.activities import activities_bp
from app.routes.bookings import bookings_bp

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Inicializar extensiones
    db.init_app(app)
    jwt.init_app(app)
    swagger.init_app(app)
    migrate.init_app(app, db)

    # Registrar manejadores globales de errores
    register_error_handlers(app)

    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(activities_bp)
    app.register_blueprint(bookings_bp)

    # Importar modelos para que Alembic/Flask-Migrate detecte las tablas
    with app.app_context():
        from app.models import User, Activity, Booking

    # Endpoint de Healthcheck
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'Campamento API',
            'version': '1.0.0'
        }), 200

    return app