import pytest
from json import dumps, loads
from src.flaskr import create_app


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
