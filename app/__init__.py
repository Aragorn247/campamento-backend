from flask import Flask, jsonify
from app.config import config_by_name
from app.extensions import db, jwt, swagger, migrate  # <--- Agregado migrate
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
    migrate.init_app(app, db)  # <--- Inicializado Migrate

    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(activities_bp)
    app.register_blueprint(bookings_bp)

    # Importar modelos para que Alembic (Migrate) detecte las tablas
    with app.app_context():
        from app.models import User, Activity, Booking
        # Se elimina db.create_all() para dar paso al flujo profesional con Alembic

    # Healthcheck
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'Campamento API',
            'version': '1.0.0'
        }), 200

    return app