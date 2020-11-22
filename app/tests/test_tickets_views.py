from datetime import datetime
from http import HTTPStatus

from flask.testing import FlaskClient

from app.tests.test_utils import prepare_ticket, prepare_city


def test_base_search(client):
    response = client.get('/api/search')
    assert response.status_code == 200


def test_get_ticket(client: FlaskClient):
    response = client.get('/api/tickets/1')
    assert response.status_code == HTTPStatus.NOT_FOUND, response.data

    city = prepare_city()
    ticket = prepare_ticket(city_id=city.id)
    response = client.get(f'/api/tickets/{ticket.id}')
    assert response.status_code == HTTPStatus.OK, response.data


def test_delete_ticket(client: FlaskClient):
    response = client.delete('/api/tickets/1')
    assert response.status_code == HTTPStatus.NOT_FOUND, response.data

    city = prepare_city()
    ticket = prepare_ticket(city_id=city.id)
    response = client.delete(f'/api/tickets/{ticket.id}')
    assert response.status_code == HTTPStatus.NO_CONTENT, response.data


def test_create_ticket(client: FlaskClient):
    city = prepare_city()
    response = client.post(
        '/api/tickets',
        json={
            'title': 'Test Title 1',
            'city_id': city.id,
            'external_id': 1123,
            'approx_done_date': '1968-12-06',
            'created_at': '2014-12-22T03:12:58.019077+00:00',
            'number': '23',
            'status': 'asdf',
            'source': 'cc1551',
            'user_id': '1',
            'work_taken_by': '1',
            'subject_id': '1',
            'text': 'asdf',
        }
    )
    assert response.status_code == HTTPStatus.CREATED, response.json
