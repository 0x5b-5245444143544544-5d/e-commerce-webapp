from flask import Flask
from flask_login import LoginManager
from backend.config import config
import backend.database as db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = config['backend']['flask_secret']
    from backend.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from backend.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from backend.models import User

    @login_manager.user_loader
    def load_user(user_id):
        user = User()
        user = User.get_user_by_id(user, user_id)
        return user

    return app