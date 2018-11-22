import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import login_manager, LoginManager
from flask_wtf.csrf import CsrfProtect

######################################
# SET UP OUR POSTGRESQL DATABASE #####
####################################

# # This grabs our directory
# basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
# Connects our Flask App to our Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CSRF_ENABLED'] = True
app.config['USER_ENABLE_EMAIL'] = False

db = SQLAlchemy(app)

# Add on migration capabilities in order to run terminal commands
Migrate(app, db)


login_manager = LoginManager()
login_manager.init_app(app)
csrf = CsrfProtect(app)
login_manager.session_protection = "basic"
login_manager.login_message = "Please login to Ahmed's Instagram first."
login_manager.login_view = "login"

from instagram.users.views import users_blueprint
from instagram.sessions.views import sessions_blueprint

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
# app.register_blueprint(images_blueprint, url_prefix="/images")
