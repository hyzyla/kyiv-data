import logging

import sentry_sdk
from flask import Flask, jsonify
from sentry_sdk.integrations.flask import FlaskIntegration
from app import tickets, users

from app.extensions import admin, db, ma, migrate, swagger
from app.lib.config import settings
from app.lib.errors import BaseError


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

    register_extensions(app)
    register_admins(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    configure_logger(app)
    configure_sentry()
    return app


def register_extensions(app):
    """Register Flask extensions."""
    admin.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    swagger.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(tickets.views.blueprint)
    app.register_blueprint(users.views.blueprint)
    return None


def register_admins(app):
    admin.add_views(tickets.admin.ticket_view)
    admin.add_views(tickets.admin.subject_view)
    admin.add_views(tickets.admin.district_view)


def register_errorhandlers(app):
    """Register error handlers."""

    @app.errorhandler(BaseError)
    def handle_base_error(error: BaseError):
        app.logger.info(f'Base error {error.to_dict()}')
        response = jsonify(error.to_dict())
        response.status_code = error.code
        return response

    return None


def register_shellcontext(app):
    """Register shell context objects."""
    pass


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(tickets.commands.group)


def configure_logger(app):
    """Configure loggers."""
    logging.basicConfig(level=logging.INFO)


def configure_sentry():
    sentry_sdk.init(dsn=settings.SENTRY_DSN, integrations=[FlaskIntegration()], traces_sample_rate=1.0)
