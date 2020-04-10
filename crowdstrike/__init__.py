"""
Crowdstrike API module

"""

import json
import os
import sys
import time

try:
    from loguru import logger
    import requests_oauthlib
    from oauthlib.oauth2 import BackendApplicationClient, TokenExpiredError
except ImportError as importerror:
    sys.exit(f"Failed to import a dependency, quitting. Error: {importerror}")

API_BASEURL = "https://api.crowdstrike.com"

# if you want to enable logging then you can just run `logger.enable("crowdstrike")` in your code.
logger.disable('crowdstrike')



class CrowdstrikeAPI:
    """ Crowdstrike API """
    def __init__(self, client_id, client_secret):
        """ starts up the CrowdstrikeAPI module Needs two strings,
        the client_id and client_secret, available from
        https://falcon.crowdstrike.com/support/api-clients-and-keys
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.client = BackendApplicationClient(client_id=client_id)
        self.oauth = requests_oauthlib.OAuth2Session(client=self.client)
        #grab a token to start with
        self.token = self.get_token()

    def get_token(self):
        """ Gets the latest auth token and returns it. """
        logger.debug("Requesting auth token")
        self.token = self.oauth.fetch_token(
            token_url=f"{API_BASEURL}/oauth2/token",
            client_id=self.client_id,
            client_secret=self.client_secret,
        )
        return self.token

    def get_event_streams(self, appid: str, format_str: str = None):
        """
        Discover all event streams in your environment
        https://assets.falcon.crowdstrike.com/support/api/swagger.html#/event-streams/listAvailableStreamsOAuth2
        """
        uri = '/sensors/entities/datafeed/v2'
        data = {}
        if appid:
            data['appId'] = appid
        if format_str and format_str in ('json', 'flatjson'):
            data['format'] = format_str

        response = self.request(
            uri=uri,
            request_method='get',
            data=data,
            )
        return response.json()

    def get_ccid(self):
        """ returns the CCID for installers """
        req = self.request(request_method='get', uri="/sensors/queries/installers/ccid/v1")
        req.raise_for_status()

        # TODO: actually make this handle errors
        if req.status_code == 200:
            retval = req.json().get('resources')[0]
        else:
            retval = False
        return retval

    def get_latest_sensor_id(self, filter_string: str = ""):
        """ returns the ids of the latest sensor IDs

            suggested filter: 'platform:mac' or 'platform:windows'
        """
        response = self.get_sensor_installer_ids(
            sort_string="release_date|desc",
            filter_string=filter_string,)
        if response:
            retval = response[0]
        else:
            retval = False
        return retval

    def get_sensor_installer_ids(self, sort_string: str = "", filter_string: str = ""):
        """
        returns a list of installer IDs, they're a list of SHA256's
        """
        logger.debug(f"get_sensor_installer_ids() called, sort_string: '{sort_string}', filter_string: '{filter_string}'")
        uri = '/sensors/queries/installers/v1'

        data = {
            'sort' : sort_string,
            'filter' : filter_string,
        }
 
        response = self.request(request_method='get', uri=uri, data=data)
        #logger.debug(response.json())
        logger.debug("Request headers")
        logger.debug(response.request.headers)
        #logger.debug(dir(response))
        response.raise_for_status()


        # TODO: handle pagination
        return response.json().get('resources', False)

    def get_sensor_installer_details(self, sensorid: str):
        """
        returns a dict about a particular sensor ID, or False if it can't find anything useful
        """
        logger.debug(f"Sensor ID: {sensorid}")
        uri = f"/sensors/entities/installers/v1"
        data = {
            'ids' : sensorid,
            }
        response = self.request(uri=uri,request_method='get',data=data)

        response.raise_for_status()
        logger.debug(response.headers)
        if not response.json().get('resources', False):
            retval = False
        else:
            retval = response.json().get('resources', False)[0]
        return retval

    def download_sensor(self, sensorid: str, destination_filename: str):
        """ downloads a sensor id to the filename """
        # TODO: actually check we can write to the destination_filename before we try downloading it
        uri = f'/sensors/entities/download-installer/v1'
        data = {
            'id' : sensorid,
        }
        response = self.request(
            uri=uri,
            request_method='get',
            data=data,
        )
        logger.debug(response.headers)
        response.raise_for_status()

        logger.debug(f"Writing intaller to {destination_filename}")
        with open(destination_filename, 'wb') as file_handle:
            file_handle.write(response.content)
        return True

    def do_request(self, uri : str, data : dict={}, request_method : str=None):
        """ does the request, this allows a single code implementation for 
            the duplicated calls in self.request() 
            
            default request method is get
        """
        fulluri = f"{API_BASEURL}{uri}"
        if not request_method:
            request_method = 'get'
        if request_method.lower() == 'get' and data:
            response = self.oauth.request(request_method, fulluri, params=data)
        else:
            response = self.oauth.request(request_method, fulluri, data=data)
        return response

    def request(self, uri: str, request_method: str = None, data: dict = None):
        """ does a request

        request_method is a string, either get / post / delete etc
            default is set in self.do_request()
        """
        # TODO: handle rate limiting
        # Requests will return the following headers:
        # X-RateLimit-Limit : Request limit per minute. type = integer
        # X-RateLimit-Remaining : The number of requests remaining for the sliding one minute window. type = integer
        logger.debug(f"request(uri='{uri}', request_method='{request_method}', data='{data}'")
        try:
            req = self.do_request(uri=uri,
                                  request_method=request_method,
                                  data=data,
                                  )
        except TokenExpiredError:
            logger.debug("Token's expired, grabbing a new one")
            self.token = self.get_token()
            req = self.do_request(uri=uri,
                                  request_method=request_method,
                                  data=data,
                                 )
            req.raise_for_status()
        return req
