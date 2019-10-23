import os
import requests
import json
from time import sleep
from src.lib.Recommend import Recommend


class SlackClient:
    SUCCESS_RESPONSE_TYPE = 'in_channel'
    ERROR_RESPONSE_TYPE = 'ephemeral'
    recommend = None

    MAX_PRICE_RANGE = 5

    def __init__(self):
        self.recommend = Recommend()

    @staticmethod
    def post_slack_message(req_data, res_url):
        """
        Posts the response message containing the recommendations to tbe designated channel in Slack.

        :param req_data: the formatted dict containing all of the required response fields
        :param res_url: the response URL provided by Slack to send the message to
        :return:
        """
        headers = {
            'Content-Type': 'application/json'
        }
        res = requests.post(url=res_url, data=json.dumps(req_data), headers=headers)
        return res

    def get_recommendations(self, num_choices, price=None, string_format=False):
        """
        Returns either a list object containing the recommendations or a string version of that list.

        :param num_choices: the number of choices to return
        :param price: price range of restaurant as an int
        :param string_format: the flag for whether or not to return a string
        :return: a list object or string of the random recommendations
        """

        # gets the name of each recommendation object and puts them all in a list
        recommendations = [x['name'] for x in self.recommend.make_recommendations(num_choices, price)]
        recommendations_str = ', '.join(recommendations)
        return recommendations if not string_format else recommendations_str

    def check_command_format(self, command):
        """
        Checks that an incoming slash command is in the correct format and returns the appropriate error reason message
        if there's an issue.

        :param command: the command dict to be checked
        :return: a dict with a flag indicating the command's validity and the appropriate (if applicable) message and
        response type
        """

        message = ''
        response_type = ''
        is_valid = False

        # the slash command wouldn't even be triggered without the "/lunch" but let's just do a sanity check
        if command['command'] == '/lunch':
            # app mention text should be in format: "recommend N", where N is the number of choices to return
            if 'recommend' in command['text'].lower() and len(command['text'].split(' ')) == 2:
                num_choices = command['text'].split(' ')[1]
                try:
                    num_choices = int(num_choices)
                    if num_choices <= 0:
                        # 0 or negative integer given
                        message = 'Nice try 😛. Use a valid number next time.'
                        response_type = self.ERROR_RESPONSE_TYPE
                    elif num_choices > len(self.recommend.get_options()):
                        # integer greater than the number of available options given
                        message = 'Sorry, your number is too big 🤷🏻. Try something more reasonable.'
                        response_type = self.ERROR_RESPONSE_TYPE
                    else:
                        is_valid = True
                # thrown if parsing an int from num_choices fails
                except ValueError:
                    message = f'`{num_choices}` isn\'t a valid number 🙄. Try again pls.'
                    response_type = self.ERROR_RESPONSE_TYPE

                # check that price range is valid
                price = command['text'].count('$')
                if price > self.MAX_PRICE_RANGE:
                    message = f'Error: User is too affluent for this bot (max $\'s is `MAX_PRICE_RANGE`)'
                    is_valid = False
            else:
                message = 'Sorry, I can\'t recognize that command 🤷🏻. Try something like `/lunch recommend 3`.'
                response_type = self.ERROR_RESPONSE_TYPE
        else:
            message = 'Sorry, I don\'t understand. Pls fix.'
            response_type = self.ERROR_RESPONSE_TYPE

        return {
            'valid': is_valid,
            'message': message,
            'response_type': response_type
        }

    """
    Example incoming raw payload format:
      token=gIkuvaNzQIHg97ATvDxqgjtO
      &team_id=T0001
      &team_domain=example
      &enterprise_id=E0001
      &enterprise_name=Globular%20Construct%20Inc
      &channel_id=C2147483705
      &channel_name=test
      &user_id=U2147483697
      &user_name=Steve
      &command=/weather
      &text=94070
      &response_url=https://hooks.slack.com/commands/1234/5678
      &trigger_id=13345224609.738474920.8088930838d88f008e0
    """
    def process_slash_command(self, payload):
        """
        Processes a valid incoming slash command.

        :param payload: a dict with all the mapped values for slash commands given by Slack
        :return:
        """

        # fake processing time beep boop
        sleep(2)
        message = ''
        attachments = ''
        response_type = self.SUCCESS_RESPONSE_TYPE
        res_url = payload['response_url']
        token = payload['token']

        # the token received in payload should match the app's Slack verification token
        if token != os.getenv('SLACK_VERIFICATION_TOKEN'):
            message = 'Hmmm it appears you have the wrong token...'
            response_type = self.ERROR_RESPONSE_TYPE
        elif 'recommend' in payload['text'].lower() and len(payload['text'].split(' ')) == 2:
            num_choices = int(payload['text'].split(' ')[1])
            price = payload['text'].count('$')
            # gets a string of the recommendations list
            recommendations = self.get_recommendations(num_choices, price, True)
            if num_choices == 1:
                message = f'As a _world-renowned_ chef, I personally recommend `{recommendations}`. Enjoy!'
            else:
                message = f'As a _world-renowned_ chef, here are my top `{num_choices}` recommendations:'
                attachments = recommendations
        # uncomment the below block and add a conditional in check_command_format() for kudos capability
        # elif 'kudos' in payload['text'].lower() and len(payload['text'].split(' ')) == 2:
        #     user = payload['text'].split(' ')[1]
        #     recommendations = self.get_recommendations(1, True)
        #     message = f'Kudos to {user} :tada:! Let\'s celebrate by going to `{recommendations}`!'
        else:
            message = 'Congrats, you broke me.'
            response_type = self.ERROR_RESPONSE_TYPE

        res_data = {
            'response_type': response_type,
            'text': message,
            'attachments': [
                {
                    'text': attachments
                }
            ]
        }
        self.post_slack_message(res_data, res_url)
        return res_data
