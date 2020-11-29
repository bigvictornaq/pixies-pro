import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

import cloudinary as Cloud
import cloudinary.uploader
import cloudinary.api


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Cloud.config(
        cloud_name = "pixies",
        api_key = "325945932269836",
        api_secret =  "7sVtJrQrKypYez-2Jch0hrJeXAY"
)

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'index'
login_manager.login_message_category = 'warning'
app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')
mail = Mail(app)

from pixies import routes
