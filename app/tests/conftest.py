import pytest

from app.main import app, db


@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

    tables = ', '.join(db.metadata.tables)
    db.session.execute(f'TRUNCATE {tables} CASCADE;')
    db.session.commit()
