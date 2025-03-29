from flask import Flask
from .config.config import Config
from .utils.logger import setup_logger
from .routes import auth, email, generator

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Setup logger
    app.logger = setup_logger('app')
    app.logger.info("Application starting up")
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(email.bp)
    app.register_blueprint(generator.bp)
    
    return app