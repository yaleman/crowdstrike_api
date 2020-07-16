""" handles interactions with the "hosts" category """

from loguru import logger

from .utilities import validate_kwargs

def get_host_groups(self, **kwargs):
    """ Retrieve a set of host groups by specifying their IDs
    Returns a set of Host Groups which match the filter criteria

        ids: str (required)
            - ids should be a list of strings
    """
    args_validation = {
        'ids' : list,
    }
    validate_kwargs(args_validation, kwargs, required=args_validation.keys())

    uri = '/devices/entities/host-groups/v1'
    method = 'get'

    response = self.request(uri=uri,
                            request_method=method,
                            data=kwargs,
                            )
    logger.debug(f"Request body: {response.request.body}")
    return response.json()

def search_host_groups(self, **kwargs):
    """ Search for Host Groups in your environment by providing an FQL filter and paging details.
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

    uri = '/devices/combined/host-groups/v1'
    method = 'get'

    response = self.request(uri=uri,
                            request_method=method,
                            data=kwargs,
                            )
    logger.debug(f"Request body: {response.request.body}")
    return response.json()
