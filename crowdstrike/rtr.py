""" handles interactions with the "hosts" category """

# import json

from loguru import logger

from .utilities import validate_kwargs

def create_rtr_session(self, **kwargs):
    """ Create a new RTR session, will retrieve an existing session if exists.

    - device_id (string) - The host agent ID to initialize the RTR session on. RTR will retrieve an existing session for the calling user on this host
    """
    args_validation = {
        'device_id' : str,
    }
    validate_kwargs(args_validation, kwargs, required=args_validation.keys())

    uri = '/real-time-response/entities/sessions/v1'
    method = 'post'

    logger.debug(f"Creating RTR session for device_id={kwargs.get('device_id')}")
    response = self.request(uri=uri,
                            request_method=method,
                            data=kwargs,
                            )
    logger.debug(f"Request body: {response.request.body}")
    return response.json()

def delete_rtr_session(self, **kwargs):
    """ Delete a RTR session.

    - session_id (string) - RTR session ID
    """
    args_validation = {
        'session_id' : str,
    }
    validate_kwargs(args_validation, kwargs, required=args_validation.keys())

    uri = '/real-time-response/entities/sessions/v1'
    method = 'delete'

    response = self.request(uri=uri,
                            request_method=method,
                            data=kwargs,
                            )
    logger.debug(f"Request body: {response.request.body}")
    logger.debug(f"Response: {response.text}")
    return response
