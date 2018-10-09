from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_mail import Mail
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from config import config
from flask_login import LoginManager
from flask_pagedown import PageDown


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
pagedown = PageDown()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    pagedown.init_app(app)
#    with app.app_context():
#        db.drop_all()
#        db.create_all()
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api_1_0 import api
    app.register_blueprint(api, url_prefix='/api')

    return app