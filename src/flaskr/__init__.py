import os
import json
from flask import Flask, Response, request
from src.lib.Recommend import Recommend


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    recommend = Recommend()
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return 'Hello World!'

    @app.route('/about')
    def about():
        return 'TODO'

    @app.route('/challenge', methods=['POST'])
    def challenge():
        # Slack requires URL verification by returning a challenge string found in the request
        challenge_str = request.json['challenge'] if 'challenge' in request.json else ''
        return challenge_str

    @app.route('/choose', methods=['GET', 'POST'])
    def choose():
        # gets the name of each recommendation object and puts them all in a list
        recommendations = [x['name'] for x in recommend.make_recommendations()]
        res_data = {
            'recommendations': recommendations
        }
        res = Response(json.dumps(res_data), status=200, content_type='application/json')
        return res

    return app
