from http import HTTPStatus
from unittest import mock, TestCase

import pytest
from flask.testing import FlaskClient

from app.tests.test_utils import (
    prepare_ticket,
    prepare_city,
    prepare_subject,
    prepare_district,
)

AUTH_HEADERS = {'Authorization': 'super-secret'}


def test_base_search(client):
    response = client.get('/api/search')
    assert response.status_code == HTTPStatus.OK, response.json
    page = {'page': 1, 'pages': 0, 'per_page': 20, 'total': 0}
    assert response.json == {'items': [], **page}

    city = prepare_city()
    city_id = city.id
    ticket1 = prepare_ticket(city_id=city.id)
    ticket2 = prepare_ticket(city_id=city.id)
    ticket1_id = ticket1.id
    ticket2_id = ticket2.id

    response = client.get('/api/search')
    assert response.status_code == HTTPStatus.OK, response.data

    TestCase().assertEqual(
        response.json,
        {
            **page,
            'pages': 1,
            'total': 2,
            'items': [
                {
                    'address': 'Test address',
                    'approx_done_date': '2020-11-22',
                    'city_id': city_id,
                    'created_at': mock.ANY,
                    'district_id': 1,
                    'external_id': 1,
                    'id': ticket2_id,
                    'number': 'N-100',
                    'source': 'cc1551',
                    'status': 'Test status',
                    'subject_id': 1,
                    'text': 'Test text',
                    'title': 'Test title',
                    'user_id': '1',
                    'work_taken_by': 'Test executor',
                },
                {
                    'address': 'Test address',
                    'approx_done_date': '2020-11-22',
                    'city_id': city_id,
                    'created_at': mock.ANY,
                    'district_id': 1,
                    'external_id': 1,
                    'id': ticket1_id,
                    'number': 'N-100',
                    'source': 'cc1551',
                    'status': 'Test status',
                    'subject_id': 1,
                    'text': 'Test text',
                    'title': 'Test title',
                    'user_id': '1',
                    'work_taken_by': 'Test executor',
                },
            ],
        },
    )


def test_get_ticket(client: FlaskClient):
    response = client.get('/api/tickets/1')
    assert response.status_code == HTTPStatus.NOT_FOUND, response.data

    city = prepare_city()
    ticket = prepare_ticket(city_id=city.id)
    response = client.get(f'/api/tickets/{ticket.id}')
    assert response.status_code == HTTPStatus.OK, response.data


def test_delete_ticket(client: FlaskClient):
    response = client.delete('/api/tickets/1', headers=AUTH_HEADERS)
    assert response.status_code == HTTPStatus.NOT_FOUND, response.data

    city = prepare_city()
    ticket = prepare_ticket(city_id=city.id)
    response = client.delete(f'/api/tickets/{ticket.id}')
    assert response.status_code == HTTPStatus.FORBIDDEN, response.data

    response = client.delete(f'/api/tickets/{ticket.id}', headers=AUTH_HEADERS)
    assert response.status_code == HTTPStatus.NO_CONTENT, response.data


@pytest.mark.parametrize(
    'headers, status',
    [
        (AUTH_HEADERS, HTTPStatus.CREATED),
        ({'Authorization': 'wrong'}, HTTPStatus.FORBIDDEN),
        (None, HTTPStatus.FORBIDDEN),
    ],
)
def test_create_ticket(client: FlaskClient, headers, status):
    city = prepare_city()
    response = client.post(
        '/api/tickets',
        json={
            'title': 'Не працює телепорт',
            'city_id': city.id,
            'external_id': 1123,
            'approx_done_date': '2077-12-06',
            'address': 'вул. Прорізна, буд. 13',
            'number': '23',
            'status': 'В роботі',
            'user_id': 100,
            'work_taken_by': '1',
            'subject_id': 1,
            'text': (
                'На прорізній, після піщаної бурі перестав працювати Телепорт ДВЗ-12.'
                'Починіть, пліз! Дуже хочу потрапити до батьків на День Інтернету'
            ),
        },
        headers=headers,
    )
    assert response.status_code == status, response.json
    if response.status_code != HTTPStatus.CREATED:
        return

    assert response.json == {
        'address': 'вул. Прорізна, буд. 13',
        'approx_done_date': '2077-12-06',
        'city_id': city.id,
        'created_at': mock.ANY,
        'district_id': None,
        'external_id': 1123,
        'id': mock.ANY,
        'number': '23',
        'source': 'api',
        'status': 'В роботі',
        'subject_id': 1,
        'text': 'На прорізній, після піщаної бурі перестав працювати Телепорт '
        'ДВЗ-12.Починіть, пліз! Дуже хочу потрапити до батьків на День '
        'Інтернету',
        'title': 'Не працює телепорт',
        'user_id': '100',
        'work_taken_by': '1',
    }


def test_get_cities(client: FlaskClient):
    city1 = prepare_city(name='Київ')
    city2 = prepare_city(name='Полтава')
    city3 = prepare_city(name='Одеса')
    response = client.get('/api/cities')
    assert response.status_code == HTTPStatus.OK, response.json
    data = response.json

    TestCase().assertEqual(
        data, [{'id': city1.id, 'name': 'Київ'}, {'id': city2.id, 'name': 'Полтава'}, {'id': city3.id, 'name': 'Одеса'}]
    )


def test_get_titles(client):
    city = prepare_city()
    prepare_ticket(city_id=city.id, title='Test 1')
    prepare_ticket(city_id=city.id, title='Test 1')
    prepare_ticket(city_id=city.id, title='Test 1')
    prepare_ticket(city_id=city.id, title='Test 2')
    response = client.get('/api/titles')
    assert response.status_code == HTTPStatus.OK, response.json
    data = response.json

    TestCase().assertEqual(
        data,
        [{'tickets_count': 3, 'title': 'Test 1'}, {'tickets_count': 1, 'title': 'Test 2'}],
    )


def test_get_subjects(client):
    city = prepare_city()

    subject1 = prepare_subject(name='Subject 1')
    subject2 = prepare_subject(name='Subject 2')
    subject3 = prepare_subject(name='Subject 3')

    prepare_ticket(city_id=city.id, subject_id=subject1.id)
    prepare_ticket(city_id=city.id, subject_id=subject1.id)
    prepare_ticket(city_id=city.id, subject_id=subject2.id)
    prepare_ticket(city_id=city.id, subject_id=0)

    response = client.get('/api/subjects')
    assert response.status_code == HTTPStatus.OK, response.json
    data = response.json

    TestCase().assertEqual(
        data,
        [
            {'tickets_count': 2, 'name': 'Subject 1', 'id': subject1.id},
            {'tickets_count': 1, 'name': 'Subject 2', 'id': subject2.id},
            {'tickets_count': 0, 'name': 'Subject 3', 'id': subject3.id},
        ],
    )


def test_get_districts(client):
    city = prepare_city()

    district1 = prepare_district(name='District 1')
    district2 = prepare_district(name='District 2')
    district3 = prepare_district(name='District 3')

    prepare_ticket(city_id=city.id, district_id=district1.id)
    prepare_ticket(city_id=city.id, district_id=district1.id)
    prepare_ticket(city_id=city.id, district_id=district2.id)
    prepare_ticket(city_id=city.id, district_id=0)

    response = client.get('/api/districts')
    assert response.status_code == HTTPStatus.OK, response.json
    data = response.json

    TestCase().assertEqual(
        data,
        [
            {'tickets_count': 2, 'name': 'District 1', 'id': district1.id},
            {'tickets_count': 1, 'name': 'District 2', 'id': district2.id},
            {'tickets_count': 0, 'name': 'District 3', 'id': district3.id},
        ],
    )
