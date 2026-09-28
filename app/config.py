import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Especificamos explícitamente el driver psycopg2
    db_url = os.getenv('DATABASE_URL', 'postgresql://camp_user:camp_password@db:5432/campamento_db')
    if db_url and db_url.startswith('postgresql://'):
        db_url = db_url.replace('postgresql://', 'postgresql+psycopg2://', 1)
        
    SQLALCHEMY_DATABASE_URI = db_url

    SWAGGER = {
        'title': 'API Campamento - Sprint 8',
        'uiversion': 3,
        'version': '1.0.0',
        'description': 'Documentación interactiva de la API Backend del Campamento'
    }

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}