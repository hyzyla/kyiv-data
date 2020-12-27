from http import HTTPStatus
from unittest import mock, TestCase

import pytest
from flask.testing import FlaskClient

from app.tests.test_utils import (
    prepare_ticket,
    prepare_city,
    prepare_subject,
    prepare_district, prepare_photo, prepare_ticket_tag,
)
from app.tickets.enums import TicketPriority

TEST_UUID_1 = '358eaec0-cb1d-4340-91da-3b0612cab6b5'
TEST_UUID_2 = '7617f8e0-a0ed-455e-a2e7-09fd7fc38be4'

TOKEN = (
    'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9vdC'
    '1yb3V0aW5nLnZvdm5lbmtvLm5hbWVcL3NpZ25pbiIsImlhdCI6MTYwNjMyMjIyOC'
    'wiZXhwIjoxNjA2MzI1ODI4LCJuYmYiOjE2MDYzMjIyMjgsImp0aSI6InVCVXZ4Ym'
    'ZRVklycHdLZlIiLCJzdWIiOjEsInBydiI6IjIzYmQ1Yzg5NDlmNjAwYWRiMzllNz'
    'AxYzQwMDg3MmRiN2E1OTc2ZjcifQ.62gFi0dSoW69RD1921JR1RH10j2Jur1Bvn5'
    'kEQg8CXc'
)
AUTH_HEADERS = {
    'Custom-Token': f'Bearer {TOKEN}',
    'Authorization': 'super-secret',
}

TEST_TEXT = (
    'На прорізній, біля Віртуаторія, після піщаної бурі перестав працювати Телепорт '
    'ДВЗ-12. Починіть, пліз! Дуже хочу потрапити до батьків на День інтернету.'
)

TEST_CREATE_TICKET = {
    'title': 'Не працює телепорт',
    'city_id': 100,
    'address': 'вул. Прорізна, буд. 13',
    'subject_id': 200,
    'text': TEST_TEXT,
}
TEST_CREATE_TICKET_EXPECTED = {
    'address': 'вул. Прорізна, буд. 13',
    'approx_done_date': None,
    'city_id': 100,
    'created_at': mock.ANY,
    'district_id': None,
    'external_id': None,
    'id': mock.ANY,
    'number': None,
    'source': 'api',
    'link': None,
    'location': None,
    'tags': [],
    'photos': [],
    'priority': None,
    'status': 'На модерації',
    'subject_id': 200,
    'text': TEST_TEXT,
    'title': 'Не працює телепорт',
    'user_id': '1',
    'work_taken_by': None,
}


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
    assert response.status_code == HTTPStatus.OK, response.json

    case = TestCase()
    case.maxDiff = None
    case.assertEqual(
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
                    'link': None,
                    'location': None,
                    'tags': [],
                    'photos': [],
                    'priority': None,
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
                    'link': None,
                    'location': None,
                    'tags': [],
                    'photos': [],
                    'priority': None,
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
    assert response.status_code == HTTPStatus.NOT_FOUND, response.json

    city = prepare_city()
    ticket = prepare_ticket(city_id=city.id)
    response = client.get(f'/api/tickets/{ticket.id}')
    assert response.status_code == HTTPStatus.OK, response.edatdatxtra


def test_delete_ticket(client: FlaskClient):
    response = client.delete('/api/tickets/1', headers=AUTH_HEADERS)
    assert response.status_code == HTTPStatus.NOT_FOUND, response.json

    city = prepare_city()
    ticket1 = prepare_ticket(city_id=city.id)
    ticket2 = prepare_ticket(city_id=city.id)
    response = client.delete(f'/api/tickets/{ticket2.id}')
    assert response.status_code == HTTPStatus.FORBIDDEN, response.json

    response = client.delete(f'/api/tickets/{ticket2.id}', headers=AUTH_HEADERS)
    assert response.status_code == HTTPStatus.OK, response.json

    response = client.delete(f'/api/tickets/{ticket2.id}', headers=AUTH_HEADERS)
    assert response.status_code == HTTPStatus.NOT_FOUND, response.json


@pytest.mark.parametrize(
    'headers, status, data, expected',
    [
        ({'Authorization': 'wrong'}, HTTPStatus.FORBIDDEN, {}, None),
        (None, HTTPStatus.FORBIDDEN, {}, None),
        # Create with small amount of data
        (
            AUTH_HEADERS,
            HTTPStatus.OK,
            {
                'address': 'вул. Прорізна, буд. 13',
                'text': TEST_TEXT,
            },
            {
                **TEST_CREATE_TICKET_EXPECTED,
                'city_id': None,
                'title': None,
                'subject_id': None,
            }
        ),
        # Simple create
        (
            AUTH_HEADERS,
            HTTPStatus.OK,
            TEST_CREATE_TICKET,
            TEST_CREATE_TICKET_EXPECTED,
        ),
        # With location
        (
            AUTH_HEADERS,
            HTTPStatus.OK,
            {
                **TEST_CREATE_TICKET,
                'location': {
                    'lat': 19.1,
                    'lng': 21.02,
                },
            },
            {
                **TEST_CREATE_TICKET_EXPECTED,
                'location': {
                    'lat': 19.1,
                    'lng': 21.02,
                },
            },
        ),
        # With priority, link
        (
            AUTH_HEADERS,
            HTTPStatus.OK,
            {
                **TEST_CREATE_TICKET,
                'priority': TicketPriority.damage.value,
                'link': 'https://youtube.com',
            },
            {
                **TEST_CREATE_TICKET_EXPECTED,
                'priority': TicketPriority.damage.value,
                'link': 'https://youtube.com',
            },
        ),
        # With tags
        (
            AUTH_HEADERS,
            HTTPStatus.OK,
            {
                **TEST_CREATE_TICKET,
                'tags': [
                    {'name': 'test tag 1'},
                    {'name': 'Test TAG   1  '},
                    {'name': 'Tag 2'},
                ],
            },
            {
                **TEST_CREATE_TICKET_EXPECTED,
                'tags': [
                    {'name': 'Test Tag 1'},
                    {'name': 'Tag 2'},
                ],
            },
        ),
        # With photos
        (
            AUTH_HEADERS,
            HTTPStatus.OK,
            {
                **TEST_CREATE_TICKET,
                'photos': [
                    {'id': TEST_UUID_1},  # photo is uploaded
                    {'id': TEST_UUID_2},  # photo is not uploaded
                ],
            },
            {
                **TEST_CREATE_TICKET_EXPECTED,
                'photos': [
                    {'id': TEST_UUID_1},  # only uploaded photo
                ],
            },
        ),
    ],
)
def test_create_ticket(client: FlaskClient, headers, status, data, expected):
    prepare_city(id_=100)
    prepare_subject(id_=200)
    prepare_photo(id_=TEST_UUID_1)

    response = client.post('/api/tickets', json=data, headers=headers)
    assert response.status_code == status, response.json
    if response.status_code != HTTPStatus.OK:
        return

    data = response.json
    data['tags'] = list(sorted(data['tags'], key=lambda d: d['name']))
    data['photos'] = list(sorted(data['photos'], key=lambda d: d['id']))

    expected['tags'] = list(sorted(expected['tags'], key=lambda d: d['name']))
    expected['photos'] = list(sorted(expected['photos'], key=lambda d: d['id']))
    assert data == expected


def test_get_tickets_tags(client):
    city = prepare_city()
    district1 = prepare_district()

    ticket1 = prepare_ticket(city_id=city.id, district_id=district1.id)
    ticket2 = prepare_ticket(city_id=city.id, district_id=district1.id)
    prepare_ticket_tag(ticket_id=ticket1.id, name='test1')
    prepare_ticket_tag(ticket_id=ticket1.id, name='test2')
    prepare_ticket_tag(ticket_id=ticket2.id, name='test1')
    prepare_ticket_tag(ticket_id=ticket2.id, name='test3')

    response = client.get('/api/tickets/tags')
    assert response.status_code == HTTPStatus.OK, response.json
    data = response.json
    assert len(data) == 3
    assert {item['name'] for item in data} == {'test1', 'test2', 'test3'}


def test_get_titles(client):
    city = prepare_city()

    prepare_ticket(title='Title1', city_id=city.id)
    prepare_ticket(title='Title2', city_id=city.id)
    prepare_ticket(title='Title2', city_id=city.id)
    prepare_ticket(title=None, city_id=city.id)

    response = client.get('/api/tickets/titles')
    assert response.status_code == HTTPStatus.OK, response.json
    data = response.json
    assert len(data) == 2
    assert {item['title'] for item in data} == {'Title1', 'Title2'}


def test_get_districts(client):
    district1 = prepare_district(name='District1')
    district2 = prepare_district(name='District2')
    district3 = prepare_district(name='District3')

    response = client.get('/api/tickets/districts')
    assert response.status_code == HTTPStatus.OK, response.json
    assert response.json == [
        {'id': district1.id, 'name': 'District1'},
        {'id': district2.id, 'name': 'District2'},
        {'id': district3.id, 'name': 'District3'},
    ]


def test_get_subjects(client):
    subject1 = prepare_subject(id_=1, name='Subject1')
    subject2 = prepare_subject(id_=2, name='Subject2')
    subject3 = prepare_subject(id_=3, name='Subject3')
    response = client.get('/api/tickets/subjects')
    assert response.status_code == HTTPStatus.OK, response.json
    assert response.json == [
        {'id': subject1.id, 'name': 'Subject1'},
        {'id': subject2.id, 'name': 'Subject2'},
        {'id': subject3.id, 'name': 'Subject3'},
    ]

