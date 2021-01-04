from http import HTTPStatus
from unittest.case import TestCase

import pytest

from app.tests.test_utils import prepare_city, prepare_ticket, prepare_subject, prepare_district
from app.tickets.enums import TicketSource


@pytest.mark.parametrize('url', ['/api/titles', '/api/stats/titles/tickets'])
def test_get_titles_tickets_stat(client, url):
    city = prepare_city()
    prepare_ticket(city_id=city.id, title='Test 1')
    prepare_ticket(city_id=city.id, title='Test 1')
    prepare_ticket(city_id=city.id, title='Test 1')
    prepare_ticket(city_id=city.id, title='Test 2')
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK, response.json
    data = response.json

    TestCase().assertEqual(
        data,
        [{'tickets_count': 3, 'title': 'Test 1'}, {'tickets_count': 1, 'title': 'Test 2'}],
    )


@pytest.mark.parametrize('url', ['/api/subjects', '/api/stats/subjects/tickets'])
def test_get_subjects_tickets_stat(client, url):
    city = prepare_city()

    subject1 = prepare_subject(id_=1, name='Subject 1')
    subject2 = prepare_subject(id_=2, name='Subject 2')
    subject3 = prepare_subject(id_=3, name='Subject 3')

    prepare_ticket(city_id=city.id, subject_id=subject1.id)
    prepare_ticket(city_id=city.id, subject_id=subject1.id)
    prepare_ticket(city_id=city.id, subject_id=subject2.id)
    prepare_ticket(city_id=city.id, subject_id=0)

    response = client.get(url)
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


@pytest.mark.parametrize('url', ['/api/districts', '/api/stats/districts/tickets'])
def test_get_districts_tickets_stat(client, url):
    city = prepare_city()

    district1 = prepare_district(name='District 1')
    district2 = prepare_district(name='District 2')
    district3 = prepare_district(name='District 3')

    prepare_ticket(city_id=city.id, district_id=district1.id)
    prepare_ticket(city_id=city.id, district_id=district1.id)
    prepare_ticket(city_id=city.id, district_id=district2.id)
    prepare_ticket(city_id=city.id, district_id=0)

    response = client.get(url)
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


def test_get_subject_stat_with_source_filter(client):
    city = prepare_city()

    subject1 = prepare_subject(id_=1, name='Subject 1')
    subject2 = prepare_subject(id_=2, name='Subject 2')
    subject3 = prepare_subject(id_=3, name='Subject 3')
    subject4 = prepare_subject(id_=4, name='Subject 4')

    prepare_ticket(city_id=city.id, subject_id=subject1.id, source=TicketSource.cc1551)
    prepare_ticket(city_id=city.id, subject_id=subject1.id, source=TicketSource.api)
    prepare_ticket(city_id=city.id, subject_id=subject2.id, source=TicketSource.api)
    prepare_ticket(city_id=city.id, subject_id=subject2.id, source=TicketSource.api)
    prepare_ticket(city_id=city.id, subject_id=subject3.id, source=TicketSource.cc1551)
    prepare_ticket(city_id=city.id, subject_id=0)

    response = client.get('/api/stats/subjects/tickets', query_string={'source': 'api'})
    assert response.status_code == HTTPStatus.OK, response.json
    data = response.json
    data = sorted(data, key=lambda item: item['id'])
    TestCase().assertEqual(
        data,
        [
            {'id': subject1.id, 'name': subject1.name, 'tickets_count': 1},
            {'id': subject2.id, 'name': subject2.name, 'tickets_count': 2},
            {'id': subject3.id, 'name': subject3.name, 'tickets_count': 0},
            {'id': subject4.id, 'name': subject4.name, 'tickets_count': 0},
        ],
    )
