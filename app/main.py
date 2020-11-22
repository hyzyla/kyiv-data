import logging

import sentry_sdk
from flask import Flask
from flask_admin import Admin
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sentry_sdk.integrations.flask import FlaskIntegration

from app.config import settings

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

sentry_sdk.init(dsn=settings.SENTRY_DSN, integrations=[FlaskIntegration()], traces_sample_rate=1.0)

admin = Admin(app, name='Kyiv data', template_mode='bootstrap3')
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

from . import views
from . import commands
from . import models
from . import admin
