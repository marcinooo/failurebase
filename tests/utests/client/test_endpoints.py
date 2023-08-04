import json
import pytest

from ..data import tests, events, clients, API_KEY

from failurebase.adapters.models import Client


class TestGetManyClients:

    def test_get_clients(self, client, database_session, config):

        response = client.get('/api/clients')

        assert response.status_code == 200

        content = response.json()

        clients_per_page = config['CLIENTS_PER_PAGE']

        base_query = database_session.query(Client).order_by(Client.created.desc())
        number_of_clients_on_first_page = base_query.limit(clients_per_page).count()

        assert content['items'] is not None
        assert len(content['items']) == number_of_clients_on_first_page
        assert content['page_number'] == 0
        assert content['page_limit'] == clients_per_page

    @pytest.mark.parametrize(
        'query_parameters,expected_results',
        [

            (f'uid={clients["client_1"]["uid"]}', 1),
            (f'uid={clients["client_1"]["uid"][10:20]}', 1),
            (f'uid=non-existing-uid-query', 0),

            (f'start_created=2023-03-03T10:45:56.397&end_created=2023-03-23T21:12:11.1923', 1),
            (f'start_created=2026-04-05T11:22:17.982', 0)

        ]
    )
    def test_get_clients_with_query_parameters(self, query_parameters, expected_results, client, database_session):
        response = client.get('/api/clients?' + query_parameters)

        assert response.status_code == 200

        content = response.json()

        assert len(content['items']) == expected_results

    @pytest.mark.parametrize(
        'query_parameters,expected_message',
        [

            ('start_created=wrong-format', 'string does not match format: %Y-%m-%dT%H:%M:%S.%f')

        ]
    )
    def test_get_clients_query_parameters_validation(self, query_parameters, expected_message, client, database_session):

        response = client.get('/api/clients?' + query_parameters)

        assert response.status_code == 422

        content = response.json()

        assert expected_message in content['detail'][0]['msg']


class TestGetSingleClient:

    def test_get_client(self, client, database_session):

        app_client = database_session.query(Client).first()

        response = client.get(f'/api/clients/{app_client.id}')

        assert response.status_code == 200

        content = response.json()

        assert app_client.uid == content['uid']


class TestCreateAppClient:

    def test_create_app_client(self, client, database_session):

        number_of_app_clients_before = database_session.query(Client).count()

        headers = {'Api-Key': API_KEY}

        response = client.post('/api/clients', headers=headers)

        assert response.status_code == 201

        content = response.json()

        assert 'uid' in content
        assert 'secret' in content

        number_of_app_clients_after = database_session.query(Client).count()

        assert number_of_app_clients_after == number_of_app_clients_before + 1


class TestDeleteAppClients:

    def test_delete_app_clients(self, client, database_session):

        headers = {'Api-Key': API_KEY}
        response = client.post(f'/api/clients/delete', headers=headers, json={'ids': []})

        assert response.status_code == 207

        content = response.json()
        assert content['statuses'] == []

        app_clients_objs = database_session.query(Client).all()
        app_clients_ids = [app_client.id for app_client in app_clients_objs]

        response = client.post(f'/api/clients/delete', headers=headers, json={'ids': app_clients_ids})

        assert response.status_code == 207

        content = response.json()

        assert len(content['statuses']) == len(app_clients_ids)
        assert all(status['id'] in app_clients_ids for status in content['statuses'])
        assert all(status['status'] == 200 for status in content['statuses'])

        app_clients_objs = database_session.query(Client).all()

        assert len(app_clients_objs) == 0

        non_existing_id = 32131

        response = client.post(f'/api/clients/delete', headers=headers, json={'ids': [non_existing_id]})

        assert response.status_code == 207

        content = response.json()

        assert len(content['statuses']) == 1
        assert content['statuses'][0]['id'] == non_existing_id
        assert content['statuses'][0]['status'] == 404
