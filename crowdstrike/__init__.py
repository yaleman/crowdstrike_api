import json
import logging
import requests

BASEURL = 'https://api.crowdstrike.com'

class Token(object):
    def __init__(self, client_id, client_secret):
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.access_token = None
        self.expires_in = -1

        self.ratelimit_limit = -1
        self.ratelimit_remaining = -1

    def get_token(self, force_get=True):
        """ gets the token, updates the local data and returns the token 
            if the token already exists and has 30 seconds to go in life, just return it
            else grab the token, update the store and return it
            https://assets.falcon.crowdstrike.com/support/api/swagger.html#/oauth2/oauth2AccessToken
        """

        # TODO: deal with the rate limiting... somehow
        if self.access_token and self.expires_in > 30:
            return self.access_token
        else:
            url = f'{BASEURL}/oauth2/token'
            headers = {
                'accept' : 'application/json',
                'Content-Type' : 'application/x-www-form-urlencoded',
            }

            data = {
                'client_id' : self.__client_id,
                'client_secret' : self.__client_secret,
            }

            try:
                response = requests.post(url, headers=headers, data=data)
                response.raise_for_status()
                data = response.json()
                self.access_token = data['access_token']
                self.expires_in = data['expires_in']

                self.ratelimit_limit = response.headers['X-Ratelimit-Limit']
                self.ratelimit_remaining = response.headers['X-Ratelimit-Remaining']
                return self.access_token
            except requests.exceptions.HTTPError:
                error_data = json.loads(response.text)
                logging.error("Token fetch error: %s", json.dumps(error_data['errors']))
                return False

class CrowdStrikeAPI(object):
    def __init__(self, token):
        self.__token = token

    def get_event_streams(self, appid, format='json'):
        """ DIscover all event streams in your environment 

        https://assets.falcon.crowdstrike.com/support/api/swagger.html#/event-streams/listAvailableStreamsOAuth2
        """
        url = f'{BASEURL}/sensors/entities/datafeed/v2?appId={appid}'
        headers = {
            'accept' : 'application/json',
            'Authorization' : f"Bearer {self.__token.get_token()}",
            # 'Content-Type' : 'application/x-www-form-urlencoded',
        }

        response = requests.get(url, headers=headers)
        return response.text
