import os
from flask import Flask, request, render_template
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

# Connects our Flask App to our Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Add on migration capabilities in order to run terminal commands
Migrate(app, db)

# Secret Key setup
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# S3 Upload setup
S3_BUCKET = os.environ['S3_BUCKET_NAME']
S3_LOCATION = f'http://{S3_BUCKET}.s3.amazonaws.com/'
S3_KEY = os.environ['S3_ACCESS_KEY']
S3_SECRET = os.environ['S3_SECRET_ACCESS_KEY']

app.config['S3_BUCKET'] = S3_BUCKET
app.config['S3_KEY'] = S3_KEY
app.config['S3_SECRET'] = S3_SECRET

# CSRF setup
app.config['CSRF_ENABLED'] = True
csrf = CsrfProtect(app)

# Login manager setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "basic"
login_manager.login_message = "Please login to Ahmed's Instagram first."
login_manager.login_view = "sessions.login"

# App Environment Conditions


class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


app.config.from_object(DevelopmentConfig)

from instagram.images.views import images_blueprint
from instagram.sessions.views import sessions_blueprint
from instagram.users.views import users_blueprint

# Blue Print
app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/")
app.register_blueprint(images_blueprint, url_prefix="/images")


# Home Page
@app.route("/")
def home():
    user_full_name = request.args.get('user_full_name')
    return render_template('home.html', user_full_name=user_full_name)
