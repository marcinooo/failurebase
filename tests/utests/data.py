import json
from datetime import datetime


tests = {
    'test_1': dict(
        uid='webui/tests/atests/login/valid_login_DS18',
        file='/home/test_user/repositories/atests/login/valid_login_DS18.robot',
        marks=json.dumps(['CRT', 'LOGIN_NO_MFA', 'LOGIN_NO_SOCIAL_MEDIA']),
        total_events_count=1
    ),
    'test_2': dict(
        uid='webui/tests/atests/login/valid_login_BR89',
        file='/home/test_user/repositories/atests/login/valid_login_BR89.robot',
        marks=json.dumps(['CRT', 'LOGIN_MFA', 'LOGIN_NO_SOCIAL_MEDIA']),
        total_events_count=1
    ),
    'test_3': dict(
        uid='webui/tests/atests/login/valid_login_AS63',
        file='/home/test_user/repositories/atests/login/valid_login_AS63.robot',
        marks=json.dumps(['CRT', 'CIT', 'LOGIN_MFA', 'LOGIN_SOCIAL_MEDIA']),
        total_events_count=1
    ),
    'test_4': dict(
        uid='main.2023_1.sg1.fr16012.peek_tput',
        file='/home/test_env/repos/pytestws/2023_1/sg1/fr16012/peek_tput.py',
        marks=json.dumps(['regression', 'tput']),
        total_events_count=1
    ),
    'test_5': dict(
        uid='main.2021_4.sg17.fr31912.attach',
        file='/home/test_env/repos/pytestws/2021_4/sg17/fr31912/attach.py',
        marks=json.dumps(['regression', 'attach']),
        total_events_count=1
    )
}


events = {
    'event_1': dict(
        message='LoginError: password should contain at least one digit',
        traceback='Traceback (most recent call last):\n'
                  ' File "/home/test_user/repositories/atests/login/valid_login_DS18.robot", line 321, in <module>\n'
                  'LoginError: password should contain at least one digit',
        client_timestamp=datetime(2023, 6, 3, 12, 15, 34, 738),
        server_timestamp=datetime(2023, 6, 3, 12, 15, 35, 128),
    ),
    'event_2': dict(
        message='MFAError: user does not provide sms code in given timeout',
        traceback='Traceback (most recent call last):\n'
                  ' File "/home/test_user/repositories/atests/login/valid_login_BR89.robot", line 239, in <module>\n'
                  'MFAError: user does not provide sms code in given timeout',
        client_timestamp=datetime(2023, 6, 3, 13, 23, 31, 345),
        server_timestamp=datetime(2023, 6, 3, 13, 23, 31, 541),
    ),
    'event_3': dict(
        message='SocialMediaLoginError: unknown issue',
        traceback='Traceback (most recent call last):\n'
                  ' File "/home/test_user/repositories/atests/login/valid_login_AS63.robot", line 128, in <module>\n'
                  'SocialMediaLoginError: unknown issue',
        client_timestamp=datetime(2023, 6, 3, 14, 45, 56, 8),
        server_timestamp=datetime(2023, 6, 3, 14, 45, 56, 218),
    ),
    'event_4': dict(
        message='ExecutionException: Moler caught some error messages during execution. '
                'Please check Moler logs for details.\n'
                'Moler caught some error messages during execution:\n'
                '  1) >>Not all cells are online<<\n',
        traceback='	Traceback (most recent call last):\n  File '
                  '"/opt/tester/python3/lib/python3.6/site-packages/moler/util/moler_test.py", line 280, in wrapped\n'
                  '    cls._check_exceptions_occured(caught_exception)\n'
                  '  File "/opt/tester/python3/lib/python3.6/site-packages/moler/util/moler_test.py", line 227, '
                  'in _check_exceptions_occured\n    raise ExecutionException(err_msg)',
        client_timestamp=datetime(2022, 11, 26, 19, 2, 7, 981),
        server_timestamp=datetime(2022, 11, 26, 19, 2, 8, 212),
    ),
    'event_5': dict(
        message='SocialMediaLoginError: unknown issue',
        traceback='Traceback (most recent call last):\n  File '
                  '"/home/tester/Paris/resources/pcap_verification/flow_verifier.py",'
                  ' line 104, in expect_messages_in_flow\n    self._verify_results(parsed_awaited_messages)\n  File '
                  '"/home/tester/Paris/resources/pcap_verification/flow_verifier.py",'
                  ' line 297, in _verify_results\n    self._verify_missing_message(message)\n  File '
                  '"/home/tester/Paris/resources/pcap_verification/flow_verifier.py",'
                  ' line 311, in _verify_missing_message\n    raise MissingMessage(err_msg)\n',
        client_timestamp=datetime(2022, 12, 21, 18, 34, 37, 899),
        server_timestamp=datetime(2022, 12, 21, 18, 34, 38, 231),
    )
}
