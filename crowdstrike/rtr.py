""" handles interactions with the "hosts" category """

import json
import time

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

def rtr_execute_command(self, **kwargs):
    """ execute a command on a single host
    https://assets.falcon.crowdstrike.com/support/api/swagger.html#/real-time-response/RTR_ExecuteCommand

    - base_command (string) (required) - one of:
        cat
        cd
        clear
        env
        eventlog
        filehash
        getsid
        help
        history
        ipconfig
        ls
        mount
        netstat
        ps
        reg query
    - command_string (string) (required) - arguments to the command
    - session_id - (string) RTR session ID to run the command on

    returns a dict wtih
    """
    uri = '/real-time-response/entities/command/v1'
    method = 'post'
    args_validation = {
        'base_command' : str,
        'command_string' : str,
        'session_id' : str,
    }
    validate_kwargs(args_validation, kwargs, required=args_validation.keys())

    response = self.request(uri=uri,
                            request_method=method,
                            data=kwargs,
                            )
    logger.debug(f"Request body: {response.request.body}")
    logger.debug(f"Response: {response.text}")

    return response.json()

def rtr_command_status(self, cloud_request_id: str, sequence_id: int):
    """
    - cloud_request_id (string) (required) - the request ID from execute_command()
    - sequence_id (integer) (required) - command responses are chunked across sequences

    returns a JSON blob
    """
    uri = '/real-time-response/entities/command/v1'
    method = 'get'

    kwargs = {
        'cloud_request_id' : cloud_request_id,
        'sequence_id' : sequence_id,
    }
    args_validation = {
        'cloud_request_id' : str,
        'sequence_id' : int,
    }
    validate_kwargs(args_validation, kwargs, required=args_validation.keys())

    response = self.request(uri=uri,
                            request_method=method,
                            data=kwargs,
                            )
    logger.debug(f"Request body: {response.request.body}")
    logger.debug(f"Response: {response.text}")

    return response.json()

def rtr_command_status_wait(self, cloud_request_id: str, interval: int = 5, maxtime: int = 60):
    """ polls rtr_command_status() periodically until it's done, then returns the results

        - interval (int) the number of seconds between a check
        - maxtime (int) the maximum time to wait - note this will currently just calculate maxtime / interval, so isn't exact (yet)
    """
    finished = False
    iteration = 0
    while not finished:
        response = self.rtr_command_status(cloud_request_id=cloud_request_id,
                                           sequence_id=0,
                                           )
        logger.debug(response)

        # pylint: disable=no-else-return
        if response.get('resources', [{}])[0].get('complete'):
            return response
        else:
            iteration += 1
            # TODO: make this closer to the actual runtime of rtr_command_status_wait()'s call
            # pylint: disable=no-else-raise
            if (interval*iteration) > maxtime:
                raise TimeoutError(f"Waited too long for {cloud_request_id} to finish, last response: {json.dumps(response)}")
            else:
                logger.debug(f"Sleeping for {interval} second(s)")
                time.sleep(interval)
    return response
