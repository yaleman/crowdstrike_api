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

        *** FQL is case sensitive - ie it has to be in lower case ***

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

def update_host_group(self, **kwargs):
    """
    Update Host Groups by specifying the ID of the group and details to update

    - assignment_rule (string) - the FQL for matching entities
    - description (string) - group description
    - id (string) - the group id for matching, won't update it
    - name (string) - the group name
    """
    args_validation = {"assignment_rule": str,
                       "description": str,
                       "id": str,
                       "name": str,
                      }
    required_args = ['id']

    validate_kwargs(args_validation=args_validation, kwargs=kwargs, required=required_args)
    uri = '/devices/entities/host-groups/v1'
    method = 'patch'
    # build the data for the update
    update_data = {'resources' : [kwargs]}

    response = self.request(uri=uri,
                            request_method=method,
                            data=update_data,
                            )
    logger.debug(f"Request body: {response.request.body}")
    return response.json()

def create_host_group(self, **kwargs):
    """
    Create Host Groups by specifying details

    group_type should be static or dynamic

    - name (string) (required) - the group name
    - description (string) (required) - group description
    - group_type (string) (required) - the group type
    - assignment_rule (string) - the filter for matching entities - required for dynamic groups - eg "(machine_domain:'example.com')"

    """
    args_validation = {"assignment_rule": str,
                       "description": str,
                       "group_type": str,
                       "name": str,
                      }

    validate_kwargs(args_validation=args_validation, kwargs=kwargs, required=list(args_validation.keys()))

    uri = '/devices/entities/host-groups/v1'
    method = 'post'

    data = {
        'resources' : [kwargs]
    }

    response = self.request(uri=uri,
                            request_method=method,
                            data=data,
                            )
    logger.debug(f"Request body: {response.request.body}")
    return response.json()

def delete_host_groups(self, **kwargs):
    """ deletes host groups based on a list of IDs

    - ids (list) (required) - the IDs of the groups to delete
    """
    args_validation = {"ids": list,
                      }

    validate_kwargs(args_validation=args_validation, kwargs=kwargs, required=list(args_validation.keys()))

    uri = '/devices/entities/host-groups/v1'
    method = 'delete'

    response = self.request(uri=uri,
                            request_method=method,
                            data=kwargs,
                            )
    return response.json()
