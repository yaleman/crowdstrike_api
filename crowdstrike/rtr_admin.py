""" handles interactions with the "hosts" category """

# import json

from loguru import logger

from .utilities import validate_kwargs

def search_rtr_scripts(self, **kwargs):
    """ Search for Realtime Response scripts in your environment by providing an FQL filter and paging details.
    Returns a set of Host Groups which match the filter criteria

    - filter (string) - The filter expression that should be used to limit the results
    - offset (integer) - The offset to start retrieving records from
    - limit (integer) - The maximum records to return. [1-5000]
    - sort (string) - field to sort by
    """
    args_validation = {
        'filter' : str,
        'offset' : int,
        'limit' : int,
        'sort' : str,

    }
    validate_kwargs(args_validation, kwargs)

    uri = '/real-time-response/queries/scripts/v1'
    method = 'get'

    response = self.request(uri=uri,
                            request_method=method,
                            data=kwargs,
                            )
    logger.debug(f"Request body: {response.request.body}")
    return response.json()

def get_rtr_scripts(self, **kwargs):
    """ Get custom-scripts based on the IDs given, tehse are used for the RTR `runscript` command

    - ids (list) - A list of file IDs for the scripts to show
    """
    args_validation = {
        'ids' : list,
    }
    validate_kwargs(args_validation, kwargs, required=args_validation.keys())

    uri = '/real-time-response/entities/scripts/v1'
    method = 'get'

    response = self.request(uri=uri,
                            request_method=method,
                            data=kwargs,
                            )
    logger.debug(f"Request body: {response.request.body}")
    return response.json()


def execute_rtr_admin_command(self, **kwargs): #pylint: disable=unused-argument
    """
        - cloud_request_id (string) (required) - Cloud Request ID of the executed command to query
        - sequence_id (integer) (required) - Sequence ID that we want to retrieve. Command responses are chunked across sequences
    """

    args_validation = {
        'cloud_request_id' : str,
        'sequence_id' : int,

    }
    validate_kwargs(args_validation, kwargs, required=kwargs.keys())
    uri = '/real-time-response/entities/admin-command/v1'
    method = 'get'
    response = self.request(uri=uri,
                            request_method=method,
                            data=kwargs,
                            )
    logger.debug(f"Request body: {response.request.body}")
    return response.json()

def status_rtr_admin_command(self, **kwargs):
    """
    Use this endpoint to run these real time response commands:
        cat         cd
        clear        cp
        encrypt        env
        eventlog        filehash
        get        getsid
        help        history
        ipconfig        kill
        ls        map
        memdump        mkdir
        mount        mv
        netstat        ps
        put        reg query
        reg set        reg delete
        reg load        reg unload
        restart        rm
        run        runscript
        shutdown        unmap
        xmemdump        zip
    - base_command (string) Active-Responder command type we are going to execute, for example: get or cp. Refer to the RTR documentation for the full list of commands.
    - command_string (string) Full command string for the command. For example get some_file.txt
    - session_id (string) RTR session ID to run the command on

    Example Value
        Model
        {
        "base_command": "cat",
        "command_string": "cat c:\temp\badfile.txt",
        "session_id": "string"
        }
    """
    args_validation = {
        'body' : str,
        'command_string' : str,
        'session_id' : str,
    }
    validate_kwargs(args_validation, kwargs, required=kwargs.keys())
    uri = '/real-time-response/entities/admin-command/v1'
    method = 'post'
    response = self.request(uri=uri,
                            request_method=method,
                            data=kwargs,
                            )
    logger.debug(f"Request body: {response.request.body}")
    return response.json()
