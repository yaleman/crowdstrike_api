""" handles interactions with the "hosts" category """

import json

from loguru import logger

from .utilities import validate_kwargs

HOST_ACTION_NAMES = [
    'contain',
    'lift_containment',
    'hide_host',
    'unhide_host',
]

def host_action(self, **kwargs):
    """ Take various actions on the hosts in your environment.
        Contain or lift containment on a host.
        Delete or restore a host.

        action_name : str (required) one of the following
            - contain
            - lift_containment
            - hide_host
            - unhide_host
        ids: str (required)
            - ids should be a list of strings
    """
    args_validation = {
        'action_name' : str,
        'ids' : list,
    }
    validate_kwargs(args_validation, kwargs, required=args_validation.keys())
    if kwargs.get('action_name') not in HOST_ACTION_NAMES:
        error_message = f"Invalid action_name={kwargs.get('action_name')} valid options are {','.join(HOST_ACTION_NAMES)}"
        logger.error(error_message)
        raise ValueError(error_message)

    uri = '/devices/entities/devices-actions/v2'
    method = 'post'

    response = self.request(uri=uri,
                            request_method=method,
                            data=kwargs,
                            )
    logger.debug(f"Request body: {response.request.body}")
    return response.json()

def hosts_detail(self, **kwargs):
    """ Get details on one or more hosts by providing agent IDs (AID). You can get a host's agent IDs (AIDs) from the /devices/queries/devices/v1 endpoint, the Falcon console or the Streaming API

    arguments:

    - ids : list (list of Agent IDs: required)
    """
    uri = '/devices/entities/devices/v1'
    method = 'get'

    args_validation = {
        'ids' : list,
    }

    validate_kwargs(args_validation, kwargs, required=args_validation.keys())

    response = self.request(uri=uri,
                            request_method=method,
                            data=kwargs,
                            )
    return response.json()



def hosts_hidden(self, **kwargs):
    """ Retrieve hidden hosts that match the provided filter criteria.
    offset = The offset to start retrieving records from
    limit = The maximum records to return. [1-5000]
    sort = The property to sort by (e.g. status.desc or hostname.asc)
    filter = The filter expression that should be used to limit the results

    returns the json object, resources are a list of host IDs
    """

    args_validation = {
        'offset' : int,
        'limit' : int,
        'sort' : str,
        'filter' : str,
    }
    validate_kwargs(args_validation, kwargs)
    uri = '/devices/queries/devices-hidden/v1'
    method = 'get'

    response = self.request(uri=uri,
                            request_method=method,
                            data=kwargs,
                            )
    return response.json()


# GET
# /devices/queries/devices-scroll/v1
# Search for hosts in your environment by platform, hostname, IP, and other criteria with continuous pagination capability (based on offset pointer which expires after 2 minutes with no maximum limit)

def hosts_query_devices(self, **kwargs):
    """ Search for hosts in your environment by platform, hostname, IP, and other criteria.
    offset = The offset to start retrieving records from
    limit = The maximum records to return. [1-5000]
    sort = The property to sort by (e.g. status.desc or hostname.asc)
    filter = The filter expression that should be used to limit the results

    returns the json object, resources are a list of host IDs
    """

    args_validation = {
        'offset' : int,
        'limit' : int,
        'sort' : str,
        'filter' : str,
    }
    validate_kwargs(args_validation, kwargs)

    uri = '/devices/queries/devices/v1'
    method = 'get'
    logger.debug(json.dumps(kwargs, indent=2))
    response = self.request(uri=uri,
                            request_method=method,
                            data=kwargs,
                            )
    return response.json()
