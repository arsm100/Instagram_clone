import os
import braintree
import sendgrid
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import login_manager, LoginManager, current_user
from flask_wtf import CSRFProtect
from authlib.flask.client import OAuth


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

# App Environment Conditions


class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']
    GOOGLE_CLIENT_SECRET = os.environ['GOOGLE_CLIENT_SECRET']
    # SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    TESTING = True


app.config.from_object(eval(os.environ['APP_SETTINGS']))

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
csrf = CSRFProtect(app)

# Login manager setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "basic"
login_manager.login_message = "Please login to Aragram first"
login_manager.login_view = "sessions.login"

# Braintree Setup & Environment Conditions (Sandbox)
BRAINTREE_MERCHANT_ID = os.environ['BRAINTREE_MERCHANT_ID']
BRAINTREE_PUBLIC_KEY = os.environ['BRAINTREE_PUBLIC_KEY']
BRAINTREE_PRIVATE_KEY = os.environ['BRAINTREE_PRIVATE_KEY']

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=BRAINTREE_MERCHANT_ID,
        public_key=BRAINTREE_PUBLIC_KEY,
        private_key=BRAINTREE_PRIVATE_KEY
    )
)


def generate_client_token():
    return gateway.client_token.generate()


# sendgrid mailing service setup
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)

# google oauth setup
config = eval((os.environ['APP_SETTINGS']))
oauth = OAuth()
REDIRECT_URI = os.environ['REDIRECT_URI']
REDIRECT_URI_NEW = os.environ['REDIRECT_URI_NEW']

google = oauth.register('google',
                        client_id=config.GOOGLE_CLIENT_ID,
                        client_secret=config.GOOGLE_CLIENT_SECRET,
                        access_token_url='https://accounts.google.com/o/oauth2/token',
                        access_token_params=None,
                        refresh_token_url=None,
                        authorize_url='https://accounts.google.com/o/oauth2/auth',
                        api_base_url='https://www.googleapis.com/oauth2/v1/',
                        client_kwargs={
                            'scope': 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile',
                            'token_endpoint_auth_method': 'client_secret_basic',
                            'token_placement': 'header',
                            'prompt': 'consent'
                        }
                        )

oauth.init_app(app)


# SuperAdmins
super_admins = {'ahmedramzy160', 'josh777'}

# Blue Print
from instagram.sessions.views import sessions_blueprint
from instagram.images.views import images_blueprint
from instagram.donations.views import donations_blueprint
from instagram.users.views import users_blueprint
from instagram.followings.views import followings_blueprint
app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/")
app.register_blueprint(images_blueprint, url_prefix="/images")
app.register_blueprint(donations_blueprint, url_prefix="/donations")
app.register_blueprint(followings_blueprint, url_prefix="/")


# Home Page
@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('users.profile', id=current_user.id))
    else:
        return render_template('home.html')
