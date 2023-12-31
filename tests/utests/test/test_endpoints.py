import pytest

from failurebase.adapters.models import Test

from ..data import tests


class TestGetManyTests:

    def test_get_tests(self, client, database_session, config):

        response = client.get('/api/tests')

        assert response.status_code == 200

        content = response.json()

        tests_per_page = config['TESTS_PER_PAGE']

        number_of_tests_on_first_page = database_session.query(Test).limit(tests_per_page).count()

        assert content['items'] is not None
        assert len(content['items']) == number_of_tests_on_first_page
        assert content['page_number'] == 0
        assert content['page_limit'] == tests_per_page

    @pytest.mark.parametrize(
        'query_parameters,expected_results',
        [
            (f'uid=webui/tests/atests/login/valid_login_DS18', 1),
            (f'uid=atests', 3),
            (f'uid=non-existing-uid-query', 0),

            (f'file=/home/test_user/repositories/atests/login/valid_login_DS18.robot', 1),
            (f'file=repositories/', 3),
            (f'file=non-existing-file-query', 0),

            (f'test_marks={tests["test_2"]["marks"]}', 1),
            (f'test_marks=["LOGIN_NO_MFA", "CRT"]', 1),
            (f'test_marks=["non-existing-marks-query"]', 0),
        ]
    )
    def test_get_tests_with_query_parameters(self, query_parameters, expected_results, client, database_session):
        response = client.get('/api/tests?' + query_parameters)

        assert response.status_code == 200

        content = response.json()

        assert len(content['items']) == expected_results

    @pytest.mark.parametrize(
        'query_parameters,expected_message',
        [

            ('test_marks=[CRT]', 'string does not match format: ["<tag>","<tag>",...]'),
            ('test_marks={"CRT":"CRT"}', 'string does not match format: ["<tag>","<tag>",...]'),
            ('test_marks=CRT', 'string does not match format: ["<tag>","<tag>",...]'),

        ]
    )
    def test_get_tests_query_parameters_validation(self, query_parameters, expected_message, client, database_session):
        response = client.get('/api/tests?' + query_parameters)

        assert response.status_code == 422

        content = response.json()

        assert expected_message in content['detail'][0]['msg']


class TestGetSingleTest:

    def test_get_test(self, client, database_session):

        test = database_session.query(Test).first()

        response = client.get(f'/api/tests/{test.id}')

        # assert response.status_code == 200
        number_of_tests_on_first_page = database_session.query(Test).limit(5).count()

        content = response.json()

        assert test.uid == content['uid']
        assert test.file == content['file']
