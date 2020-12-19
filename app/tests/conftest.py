import pytest

from app.extensions import db
from app.main import create_app


@pytest.fixture(scope='session')
def app():
    _app = create_app()
    with _app.app_context():
        yield _app


@pytest.fixture
def client(app):
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

    tables = ', '.join(db.metadata.tables)
    db.session.rollback()
    db.session.execute(f'TRUNCATE {tables} CASCADE;')
    db.session.commit()
