import pytest

from ..data import tests, events

from failurebase.adapters.models import Event, Test


class TestGetManyEvents:

    def test_get_events(self, client, database_session, config):

        response = client.get('/api/events')

        assert response.status_code == 200

        content = response.json()

        events_per_page = config['EVENTS_PER_PAGE']

        base_query = database_session.query(Event).order_by(Event.server_timestamp.desc())
        number_of_events_on_first_page = base_query.limit(events_per_page).count()

        assert content['items'] is not None
        assert len(content['items']) == number_of_events_on_first_page
        assert content['page_number'] == 0
        assert content['page_limit'] == events_per_page

    @pytest.mark.parametrize(
        'query_parameters,expected_results',
        [

            (f'message={events["event_1"]["message"]}', 1),
            (f'message=LoginError: password', 1),
            (f'message=non-existing-message-query', 0),

            (f'traceback={events["event_2"]["message"]}', 1),
            (f'traceback=user does not provide sms code', 1),
            (f'traceback=non-existing-traceback-query', 0),

            (f'start_client_timestamp=2023-06-03T13:20:19.1763&end_client_timestamp=2023-06-03T13:30:19.1763', 1),
            (f'start_client_timestamp=2023-06-03T18:20:19.1763', 0),

            (f'start_server_timestamp=2022-11-26T19:01:45.2341&end_server_timestamp=2022-11-28T19:01:45.2341', 1),
            (f'start_server_timestamp=2023-12-29T17:11:23.7832', 0),

            (f'test_uid={tests["test_1"]["uid"]}', 1),
            (f'test_uid=valid_login_BR89', 1),
            (f'test_uid=non-existing-test-uid-query', 0),

            (f'test_file={tests["test_2"]["file"]}', 1),
            (f'test_file=login/valid_login_AS63.robot', 1),
            (f'test_file=non-existing-test-file-query', 0),

            (f'test_marks={tests["test_3"]["marks"]}', 1),
            (f'test_marks=["LOGIN_SOCIAL_MEDIA"]', 1),
            (f'test_marks=["non-existing-test-marks-query"]', 0),
        ]
    )
    def test_get_events_with_query_parameters(self, query_parameters, expected_results, client, database_session):
        response = client.get('/api/events?' + query_parameters)

        assert response.status_code == 200

        content = response.json()

        assert len(content['items']) == expected_results

    @pytest.mark.parametrize(
        'query_parameters,expected_message',
        [

            ('start_client_timestamp=wrong-format', 'string does not match format: %Y-%m-%dT%H:%M:%S.%f'),
            ('end_client_timestamp=wrong-format', 'string does not match format: %Y-%m-%dT%H:%M:%S.%f'),
            ('start_server_timestamp=wrong-format', 'string does not match format: %Y-%m-%dT%H:%M:%S.%f'),
            ('end_server_timestamp=wrong-format', 'string does not match format: %Y-%m-%dT%H:%M:%S.%f'),
            ('test_marks=[CRT]', 'string does not match format: ["<tag>","<tag>",...]'),
            ('test_marks={"CRT":"CRT"}', 'string does not match format: ["<tag>","<tag>",...]'),
            ('test_marks=CRT', 'string does not match format: ["<tag>","<tag>",...]'),

        ]
    )
    def test_get_events_query_parameters_validation(self, query_parameters, expected_message, client, database_session):

        response = client.get('/api/events?' + query_parameters)

        assert response.status_code == 422

        content = response.json()

        assert expected_message in content['detail'][0]['msg']


class TestGetSingleEvent:

    def test_get_event(self, client, database_session):

        event = database_session.query(Event).first()

        response = client.get(f'/api/events/{event.id}')

        assert response.status_code == 200

        content = response.json()

        assert event.message == content['message']
        assert event.traceback == content['traceback']
        assert event.test.uid == content['test']['uid']


class TestCreateEvent:

    def test_create_event(self, client, database_session):

        number_of_events_before = database_session.query(Event).count()
        number_of_tests_before = database_session.query(Test).count()

        data = {
            'test': {
                'uid': 'main.2022_3.sg34.fr43915.call',
                'marks': ['regression', 'attach', 'tput', 'detach'],
                'file': '/home/test_env/repos/pytestws/2022_3/sg34/fr43915/call.py',
            },
            'message': 'TputError: level of tput is too low',
            'traceback': '... sth :) ...',
            'timestamp': '2023-04-02T09:45:21.2318'
        }

        response = client.post('/api/events', json=data)

        assert response.status_code == 201

        content = response.json()

        assert data['message'] == content['message']
        assert data['traceback'] == content['traceback']
        assert data['test']['uid'] == content['test']['uid']

        number_of_events_after = database_session.query(Event).count()
        number_of_tests_after = database_session.query(Test).count()

        assert number_of_events_after == number_of_events_before + 1
        assert number_of_tests_after == number_of_tests_before + 1

    @pytest.mark.parametrize(
        'data,errs',
        [

            (
                {
                    'test': {'uid': 1, 'marks': 1, 'file': 1},
                    'message': 1,
                    'traceback': 1,
                    'timestamp': 1
                },
                [
                    {'loc': ['body', 'test', 'marks'], 'msg': 'value is not a valid list'},
                    {'loc': ['body', 'timestamp'], 'msg': "time data '1' does not match format '%Y-%m-%dT%H:%M:%S.%f'"}
                ]
            ),

            (
                {
                    'test': {'uid': 1, 'marks': [], 'file': 1},
                    'message': 1,
                    'traceback': 1,
                    'timestamp': '2023-04-02-09:45:21.2318'
                },
                [
                    {'loc': ['body', 'timestamp'],
                     'msg': "time data '2023-04-02-09:45:21.2318' does not match format '%Y-%m-%dT%H:%M:%S.%f'"}
                ]
            )

        ]
    )
    def test_create_event_validation(self, data, errs, client, database_session):

        number_of_events_before = database_session.query(Event).count()
        number_of_tests_before = database_session.query(Test).count()

        response = client.post('/api/events', json=data)

        assert response.status_code == 422

        content = response.json()

        assert len(content['detail']) == len(errs)

        for exp_err in errs:
            test_marks_err = next((err for err in content['detail'] if err['loc'] == exp_err['loc']), None)
            assert exp_err['msg'] in test_marks_err['msg']

        number_of_events_after = database_session.query(Event).count()
        number_of_tests_after = database_session.query(Test).count()

        assert number_of_events_after == number_of_events_before
        assert number_of_tests_after == number_of_tests_before


class TestDeleteEvents:

    def test_delete(self, client, database_session):

        response = client.post(f'/api/events/delete', json={'ids': []})

        assert response.status_code == 207

        content = response.json()
        assert content['statuses'] == []

        events_objs = database_session.query(Event).all()
        events_ids = [event.id for event in events_objs]

        response = client.post(f'/api/events/delete', json={'ids': events_ids})

        assert response.status_code == 207

        content = response.json()

        assert len(content['statuses']) == len(events_ids)
        assert all(status['id'] in events_ids for status in content['statuses'])
        assert all(status['status'] == 200 for status in content['statuses'])

        tests_obj = database_session.query(Test).all()

        assert len(tests_obj) == len(events_ids)

        events_objs = database_session.query(Event).all()

        assert len(events_objs) == 0

        non_existing_id = 32131

        response = client.post(f'/api/events/delete', json={'ids': [non_existing_id]})

        assert response.status_code == 207

        content = response.json()

        assert len(content['statuses']) == 1
        assert content['statuses'][0]['id'] == non_existing_id
        assert content['statuses'][0]['status'] == 404
