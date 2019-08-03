import pytest
from os import getenv
from src.lib.SlackClient import SlackClient


class TestSlackClient:
    @pytest.fixture
    def slack_client(self):
        slack_client = SlackClient()
        yield slack_client

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    @staticmethod
    def invalid_command_helper(command, error_msg):
        slack_client = SlackClient()
        format_check = slack_client.check_command_format(command)
        assert format_check.keys() >= {'valid', 'message', 'response_type'}
        assert format_check['valid'] == False
        assert format_check['response_type'] == SlackClient.ERROR_RESPONSE_TYPE
        assert error_msg in format_check['message']

    @staticmethod
    def process_slash_command_helper(payload, response_type, msg):
        slack_client = SlackClient()
        res_data = slack_client.process_slash_command(payload)
        assert res_data.keys() >= {'response_type', 'text', 'attachments'}
        assert res_data['response_type'] == response_type
        assert msg in res_data['text']

    def test_post_slack_message(self, slack_client):
        res = slack_client.post_slack_message({}, 'https://example.com')
        assert res.status_code == 200

    def test_get_recommendations(self, slack_client):
        recommendations = slack_client.get_recommendations(3)
        assert isinstance(recommendations, list)
        assert len(recommendations) == 3

    def test_get_recommendations_string(self, slack_client):
        recommendations = slack_client.get_recommendations(3, string_format=True)
        assert isinstance(recommendations, str)

    def test_check_command_format(self, slack_client):
        command = {
            'command': '/lunch',
            'text': 'recommend 3'
        }
        format_check = slack_client.check_command_format(command)
        assert format_check.keys() >= {'valid', 'message', 'response_type'}
        assert format_check['valid'] == True

    def test_check_command_format_invalid_command(self):
        command = {
            'command': '/foo',
            'text': 'recommend 3'
        }
        self.invalid_command_helper(command, 'Sorry, I don\'t understand. Pls fix.')

    def test_check_command_format_invalid_command_text(self):
        command = {
            'command': '/lunch',
            'text': 'foo 3'
        }
        self.invalid_command_helper(command, 'Sorry, I can\'t recognize that command 🤷🏻. Try something like `/lunch recommend 3`.')

    def test_check_command_format_invalid_command_text_length(self):
        command = {
            'command': '/lunch',
            'text': 'recommend foo 3'
        }
        self.invalid_command_helper(command, 'Sorry, I can\'t recognize that command 🤷🏻. Try something like `/lunch recommend 3`.')

    def test_check_command_format_nan(self):
        command = {
            'command': '/lunch',
            'text': 'recommend foo'
        }
        self.invalid_command_helper(command, 'isn\'t a valid number 🙄. Try again pls.')

    def test_check_command_format_negative_number(self):
        command = {
            'command': '/lunch',
            'text': 'recommend -1'
        }
        self.invalid_command_helper(command, 'Nice try 😛. Use a valid number next time.')

    def test_check_command_format_too_high_number(self):
        command = {
            'command': '/lunch',
            'text': 'recommend 100'
        }
        self.invalid_command_helper(command, 'Sorry, your number is too big 🤷🏻. Try something more reasonable.')

    def test_process_slash_command_single_option(self):
        payload = {
            'token': getenv('SLACK_VERIFICATION_TOKEN'),
            'response_url': 'https://example.com',
            'text': 'recommend 1'
        }
        self.process_slash_command_helper(payload, SlackClient.SUCCESS_RESPONSE_TYPE, 'As a _world-renowned_ chef, I personally recommend')

    def test_process_slash_command_multiple_options(self):
        payload = {
            'token': getenv('SLACK_VERIFICATION_TOKEN'),
            'response_url': 'https://example.com',
            'text': 'recommend 3'
        }
        self.process_slash_command_helper(payload, SlackClient.SUCCESS_RESPONSE_TYPE, 'As a _world-renowned_ chef, here are my top')

    def test_process_slash_command_invalid_token(self):
        payload = {
            'token': 'invalid_token',
            'response_url': 'https://example.com',
            'text': 'recommend 3'
        }
        self.process_slash_command_helper(payload, SlackClient.ERROR_RESPONSE_TYPE, 'Hmmm it appears you have the wrong token...')

    def test_process_slash_command_invalid_command_text(self):
        payload = {
            'token': getenv('SLACK_VERIFICATION_TOKEN'),
            'response_url': 'https://example.com',
            'text': 'foo 3'
        }
        self.process_slash_command_helper(payload, SlackClient.ERROR_RESPONSE_TYPE, 'Congrats, you broke me.')
