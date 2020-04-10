""" downloads the latest versions of the crowdstrike endpoint tools, 
then uploads them in standard filename formats to our S3 bucket.

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
    def __init__(self, client_id, client_secret):
        """ handles some of the crowdstrike API endpoints
        
        """
        self.client_id = client_id
        self.client_secret = client_secret
        
        self.client = BackendApplicationClient(client_id=client_id)
        
        self.oauth = requests_oauthlib.OAuth2Session(client=self.client)
        
        #grab a token to start with
        self.get_token()

    def get_token(self):
        logger.debug("Requesting auth token")
        self.token = self.oauth.fetch_token(
            token_url=f"{API_BASEURL}/oauth2/token", 
            client_id=self.client_id,
            client_secret=self.client_secret,
        )

    def get_event_streams(self, appid : str, partition : str = None):
        """ 
        Discover all event streams in your environment 
        https://assets.falcon.crowdstrike.com/support/api/swagger.html#/event-streams/listAvailableStreamsOAuth2
        """
        #url = f'/sensors/entities/datafeed/v2?appId={appid}'
        uri = '/sensors/entities/datafeed-actions/v1/'
        if partition:
            uri = f'{uri}{partition}'

        response = self.request(
            uri=uri, 
            request_method='get',
            )
        return response.json()
        
    def get_ccid(self):
        """ returns the CCID for installers """
        req = self.request("/sensors/queries/installers/ccid/v1")
        req.raise_for_status()

        # TODO: actually make this handle errors
        if req.status_code == 200:
            return req.json().get('resources')[0]
        else:
            return False
    
    def get_latest_sensor_id(self, filter_string : str=""):
        """ returns the ids of the latest sensor IDs
        
            suggested filter: 'platform:mac' or 'platform:windows'
        """
        response = self.get_sensor_installer_ids(
            sort_string="release_date|desc",
            filter_string="platform:mac",
        )
        if response:
            return response[0]
        else:
            return False
    
    def get_sensor_installer_ids(self, sort_string : str="", filter_string : str=""):
        """ 
        returns a list of installer IDs, they're a list of SHA256's
        """
        uri = '/sensors/queries/installers/v1'
        
        data = {
            'sort' : sort_string,
            'filter' : filter_string,
        }
        response = self.request(uri, data=data)
        response.raise_for_status()
        
        # TODO: handle pagination
        return response.json().get('resources', False)
    
    def get_sensor_installer_details(self, sensorid : str):
        """
        returns a dict about a particular sensor ID, or False if it can't find anything useful
        """
        logger.debug(f"Sensor ID: {sensorid}")
        uri = f"/sensors/entities/installers/v1?ids={sensorid}"
        #data = {
        #    'ids' : sensorid
        #}
        response = self.request(
            uri=uri,
            request_method='get',
            #data=data,
        )
        
        response.raise_for_status()
        logger.debug(response.headers)
        if not response.json().get('resources', False):
            return False
        else:
            return response.json().get('resources', False)[0]
    
    def download_sensor(self, sensorid : str, destination_filename : str):
        """ downloads a sensor id to the filename """
        # TODO: actually check we can write to the destination_filename before we try downloading it
        uri = f'/sensors/entities/download-installer/v1?id={sensorid}'
        
        response = self.request(
            uri=uri,
            request_method='get',
        )
        logger.debug(response.headers)
        response.raise_for_status()
        
        logger.debug(f"Writing intaller to {destination_filename}")
        with open(destination_filename, 'wb') as fh:
            fh.write(response.content)
        
        return True


    def do_request(self, uri : str, data : dict={}, request_method : str=None):
        """ does the request, this allows a single code implementation for 
            the duplicated calls in self.request() 
            
            default request method is get
        """
        if not request_method:
            request_method = 'get'
        return self.oauth.request(request_method, f"{API_BASEURL}{uri}")
    
    def request(self, uri : str, request_method : str=None, data : dict={}):
        """ does a request 
        
        request_method is a string, either get / post / delete etc
            default is set in self.do_request()
        """
        # TODO: handle rate limiting
        # Requests will return the following headers:
        # X-RateLimit-Limit : Request limit per minute. type = integer
        # X-RateLimit-Remaining : The number of requests remaining for the sliding one minute window. type = integer

        try:
            req =  self.do_request(uri=uri, request_method=request_method, data=data)
        except TokenExpiredError as e:
            logger.debug("Token's expired, grabbing a new one")
            self.token = self.get_token()
            req =  self.do_request(uri=uri, request_method=request_method, data=data)

            req.raise_for_status()
        return req
