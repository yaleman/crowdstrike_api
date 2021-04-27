"""
Crowdstrike API module

"""

import json
import os
import sys
import time
import errno

try:
    from loguru import logger
    import requests
    from requests.auth import HTTPBasicAuth

    import requests_oauthlib
    from oauthlib.oauth2 import BackendApplicationClient, TokenExpiredError
except ImportError as importerror:
    sys.exit(f"Failed to import a dependency, quitting. Error: {importerror}")

from .hosts import hosts_query_devices, host_action, hosts_hidden, hosts_detail
from .hostgroup import search_host_groups, get_host_groups, update_host_group, create_host_group, delete_host_groups
from .sensor_download import get_sensor_installer_details, get_ccid, get_latest_sensor_id, get_sensor_installer_ids, download_sensor
from .event_streams import get_event_streams
from .incidents import incidents_behaviors_by_id, incidents_get_crowdscores, incidents_get_details, incidents_perform_actions, incidents_query, incidents_query_behaviors
from .detects import get_detects, get_detections
from .rtr import create_rtr_session, delete_rtr_session, rtr_execute_command, rtr_command_status, rtr_command_status_wait, list_rtr_session_ids
from .rtr_admin import search_rtr_scripts, get_rtr_scripts

from .intel import *
try:
    if isinstance(THIS_SHOULD_FAIL, bool):
        raise ValueError("__all__ is missing in a module")
except ValueError:
    logger.error("__all__ is missing in a module")
    sys.exit(1)
except NameError:
    # this is good
    pass

API_BASEURL = "https://api.crowdstrike.com"

# if you want to enable logging then you can just run logger.enable("crowdstrike") in your code.
logger.disable('crowdstrike')

# set status by using the keys in here, not the values
INCIDENT_STATUS_LOOKUP = {
    20 : "New",
    25 : "Reopened",
    30 : "In progress",
    40 : "Closed",
}

# normal ones they use
INCIDENT_TAGS_STANDARD = [
    'False Positive',
    'Ignored',
    'Lateral Movement',
    'Testing',
    'True Positive',
]


class CrowdstrikeAPI:
    """ Crowdstrike API """
    def __init__(self,
                 client_id: str,
                 client_secret: str,
                 api_baseurl: str = API_BASEURL):
        """ Starts up the CrowdstrikeAPI module Needs two strings,
        the client_id and client_secret, available from
        https://falcon.crowdstrike.com/support/api-clients-and-keys

        You might want to override api_baseurl if you're in a different region, too.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.client = BackendApplicationClient(client_id=client_id)
        self.oauth = requests_oauthlib.OAuth2Session(client=self.client)
        #grab a token to start with
        self.token = self.get_token()
        self.api_baseurl = api_baseurl

    def get_token(self):
        """ Gets the latest auth token and returns it. """
        logger.debug("Requesting auth token")
        uri = '/oauth2/token'
        # this is just here for introspection purposes
        # pylint: disable=unused-variable
        method = 'post'
        self.token = self.oauth.fetch_token(
            token_url=f"{API_BASEURL}{uri}",
            client_id=self.client_id,
            client_secret=self.client_secret,
        )
        return self.token

    def revoke_token(self, **kwargs):
        """ revoke the current token

        https://assets.falcon.crowdstrike.com/support/api/swagger.html#/oauth2/oauth2RevokeToken
        """
        #token = kwargs.get('token', self.token)
        #logger.debug(self.token)
        token = kwargs.get('token', self.token.get('access_token'))

        uri = '/oauth2/revoke'
        method = 'post'
        data = {
            'token': token,
        }
        response = requests.request(url=f"{API_BASEURL}{uri}",
                                    method=method,
                                    data=data,
                                    auth=HTTPBasicAuth(self.client_id, self.client_secret)
                                    )
        logger.debug(response)
        logger.debug(response.request.headers)
        logger.debug(response.request.body)
        return response.json()

    def do_request(self, uri: str, data: dict, request_method: str = 'get'):
        """ does the request, this allows a single code implementation for
            the duplicated calls in self.request()

            default request method is get
        """
        fulluri = f"{API_BASEURL}{uri}"

        # these methods use a get-request-style-data-in-the-url nastiness.
        methods_using_params = ['get', 'delete']

        if request_method.lower() in methods_using_params and data:
            response = self.oauth.request(request_method, fulluri, params=data)
        else:
            response = self.oauth.request(request_method, fulluri, json=data)
        return response

    def request(self, uri: str, request_method: str = None, data: dict = None):
        """ does a request

        request_method is a string, either get / post / delete etc
            default is set in self.do_request()
        """
        # TODO: handle rate limiting
        # Requests will return the following headers:
        # X-RateLimit-Limit : Request limit per minute.
        #   type = integer
        # X-RateLimit-Remaining : The number of requests remaining for the sliding 1 minute window.
        #   type = integer
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

    # sensor-related things
    get_ccid = get_ccid
    get_latest_sensor_id = get_latest_sensor_id
    get_sensor_installer_details = get_sensor_installer_details
    get_sensor_installer_ids = get_sensor_installer_ids
    download_sensor = download_sensor
    #detects
    get_detects = get_detects
    get_detections = get_detections
    # event-streams
    get_event_streams = get_event_streams
    # hosts
    hosts_query_devices = hosts_query_devices
    host_action = host_action
    hosts_hidden = hosts_hidden
    hosts_detail = hosts_detail

    # incidents
    incidents_behaviors_by_id = incidents_behaviors_by_id
    incidents_get_crowdscores = incidents_get_crowdscores
    incidents_get_details = incidents_get_details
    incidents_perform_actions = incidents_perform_actions
    incidents_query = incidents_query
    incidents_query_behaviors = incidents_query_behaviors

    #hostgroups
    create_host_group = create_host_group
    search_host_groups = search_host_groups
    get_host_groups = get_host_groups
    update_host_group = update_host_group
    delete_host_groups = delete_host_groups

    # intel
    get_intel_indicators = get_intel_indicators

    #rtr
    create_rtr_session = create_rtr_session
    delete_rtr_session = delete_rtr_session
    list_rtr_session_ids = list_rtr_session_ids

    rtr_command_status = rtr_command_status
    rtr_execute_command = rtr_execute_command
    rtr_command_status_wait = rtr_command_status_wait

    #rtr_admin
    search_rtr_scripts = search_rtr_scripts
    get_rtr_scripts = get_rtr_scripts
