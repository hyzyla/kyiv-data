import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_admin import Admin

from app.config import settings

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app, name='Kyiv data', template_mode='bootstrap3')
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

from . import views
from . import commands
from . import models
from . import admin
