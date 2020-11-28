from flasgger import Swagger
from flask_admin import Admin
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

admin = Admin(name='Kyiv data', template_mode='bootstrap3', endpoint='/admin')
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
swagger = Swagger()
