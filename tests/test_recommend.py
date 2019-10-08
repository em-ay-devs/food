import pytest
from src.lib.Recommend import Recommend


class TestRecommend:
    @pytest.fixture
    def recommend(self):
        recommend = Recommend()
        yield recommend

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

    def test_get_options(self, recommend):
        options = recommend.get_options()
        assert len(options) == 30
        assert options[0]['name'] == 'B.GOOD'

    def test_make_recommendations(self, recommend):
        default_recommendations = recommend.make_recommendations()
        assert len(default_recommendations) == 3
        assert 'name' in default_recommendations[1]
        assert 'price' in default_recommendations[2]

    def test_make_recommendations_too_high(self, recommend):
        recommendations = recommend.make_recommendations(100)
        assert len(recommendations) == 0

    def test_make_recommendations_negative(self, recommend):
        recommendations = recommend.make_recommendations(-10)
        assert len(recommendations) == 0
