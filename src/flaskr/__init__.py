import os
import json
from flask import Flask, Response, request
from threading import Thread
from src.lib.SlackClient import SlackClient


def create_successful_response(res_data, status_code):
    return Response(json.dumps(res_data), status=status_code, content_type='application/json')


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
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
        return Response('Hello World!', status=200, content_type='text/plain')

    @app.route('/about')
    def about():
        return Response('TODO', status=200, content_type='text/plain')

    @app.route('/challenge', methods=['POST'])
    def challenge():
        # Slack requires URL verification by returning a challenge string found in the request
        challenge_str = request.json['challenge'] if 'challenge' in request.json else ''
        res_data = {
            'challenge': challenge_str
        }
        return create_successful_response(res_data, 200)

    @app.route('/choose', methods=['GET'])
    def choose():
        slack_client = SlackClient()
        num_choices = request.args.get('options', default=3, type=int)
        price_range = request.args.get('price', default=None, type=int)
        res_data = {
            'recommendations': slack_client.get_recommendations(num_choices, price_range)
        }
        return create_successful_response(res_data, 200)

    @app.route('/slack-choose', methods=['POST'])
    def slack_choose():
        payload = request.form.to_dict()

        if ('token' or 'channel_id' or 'response_url') not in payload:
            error_str = 'You\'re not Slack. Use the /choose route instead.'
            return Response(error_str, status=403, content_type='text/plain')

        slack_client = SlackClient()
        command = {
            'command': payload['command'],
            'text': payload['text']
        }
        format_check = slack_client.check_command_format(command)
        if not format_check['valid']:
            res_data = {
                'response_type': format_check['response_type'],
                'text': format_check['message']
            }
            return create_successful_response(res_data, 200)

        # creates a thread to process the incoming slash command after returning the immediate acknowledgement
        thread = Thread(target=slack_client.process_slash_command, args=(payload,))
        thread.start()

        res_data = {
            'response_type': 'in_channel'
        }
        # returns a response with HTTP status code 202 to indicate that the message has been accepted but still
        # processing
        return create_successful_response(res_data, 202)

    @app.route('/one-choice-above-them-all', methods=['GET'])
    def one_choice():
        return Response('You should eat at Wegmans!', status=200, content_type='text/plain')

    return app
