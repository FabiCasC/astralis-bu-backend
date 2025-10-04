from flask import Flask
from app.config import Config
from app.extensions import db, migrate
from app.api.auth import auth_bp
from app.api.users import users_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)

    @app.route('/')
    def index():
        return {'message': 'Backend Astralis listo 🚀'}

    return app
