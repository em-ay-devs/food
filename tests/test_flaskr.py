import pytest
from os import getenv, pardir, path
from dotenv import load_dotenv
from json import dumps, loads
from src.flaskr import create_app

load_dotenv(dotenv_path=path.join(path.dirname(__file__), pardir, 'src/configs/.env'))


class TestFlaskr:
    @pytest.fixture
    def client(self):
        client = create_app().test_client(use_cookies=False)
        yield client

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

    def test_get_index(self, client):
        res = client.get('/', follow_redirects=True)
        assert res.status_code == 200
        assert res.data.decode('UTF-8') == 'Hello World!'

    def test_get_about(self, client):
        res = client.get('/about', follow_redirects=True)
        assert res.status_code == 200
        assert res.data.decode('UTF-8') == 'TODO'

    def test_post_challenge(self, client):
        res = client.post('/challenge', data=dumps(dict(challenge='foo')), content_type='application/json', follow_redirects=True)
        assert res.status_code == 200
        assert res.content_type == 'application/json'
        assert loads(res.data.decode('UTF-8'))['challenge'] == 'foo'

    def test_get_choose(self, client):
        res = client.get('/choose', follow_redirects=True)
        assert res.status_code == 200
        assert res.content_type == 'application/json'
        assert 'recommendations' in loads(res.data.decode('UTF-8'))

    def test_post_slack_choose(self, client):
        req_data = {
            'token': getenv('SLACK_VERIFICATION_TOKEN'),
            'channel_id': 'a_slack_channel_id',
            'response_url': 'https://example.com',
            'command': '/lunch',
            'text': 'recommend 3'
        }
        res = client.post('/slack-choose', data=req_data, follow_redirects=True)
        assert res.status_code == 202
        assert res.content_type == 'application/json'
        assert loads(res.data.decode('UTF-8'))['response_type'] == 'in_channel'

    def test_post_slack_choose_invalid_payload(self, client):
        req_data = {
            'command': '/lunch',
            'text': 'recommend 3'
        }
        res = client.post('/slack-choose', data=req_data, follow_redirects=True)
        assert res.status_code == 403
        assert res.content_type == 'text/plain'
        assert res.data.decode('UTF-8') == 'You\'re not Slack. Use the /choose route instead.'

    def test_post_slack_choose_invalid_command_text(self, client):
        req_data = {
            'token': getenv('SLACK_VERIFICATION_TOKEN'),
            'channel_id': 'a_slack_channel_id',
            'response_url': 'https://example.com',
            'command': '/lunch',
            'text': 'recommend foo'
        }
        res = client.post('/slack-choose', data=req_data, follow_redirects=True)
        assert res.status_code == 200
        assert res.content_type == 'application/json'
        assert loads(res.data.decode('UTF-8'))['response_type'] == 'ephemeral'

    def test_get_one_choice_above_them_all(self, client):
        res = client.get('/one-choice-above-them-all', follow_redirects=True)
        assert res.status_code == 200
        assert res.content_type == 'text/plain'
        assert res.data.decode('UTF-8') == 'You should eat at Wegmans!'
