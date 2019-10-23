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
        assert options[0]['name']
        assert options[0]['takeout']
        assert options[0]['delivery']
        assert options[0]['distance']
        assert options[0]['price']

    def test_make_recommendations(self, recommend):
        default_recommendations = recommend.make_recommendations()
        assert len(default_recommendations) == 3
        assert 'name' in default_recommendations[1]
        assert 'price' in default_recommendations[2]

    # asking for more recommendations than available will return all options
    def test_make_recommendations_exceeds_options(self, recommend):
        total_options = len(recommend.get_options())
        recommendations = recommend.make_recommendations(100)
        assert len(recommendations) == total_options

    def test_make_recommendations_negative(self, recommend):
        recommendations = recommend.make_recommendations(-10)
        assert len(recommendations) == 0

    def test_make_recommendations_with_price(self, recommend):
        recommendations = recommend.make_recommendations(price=1)
        if recommendations:
            assert recommendations[0]['price'] == '$'
