""" handler for incidents """

from loguru import logger

from .utilities import validate_kwargs

def incidents_get_crowdscores(self, **kwargs):
    """ Query environment wide CrowdScore and return the entity data """
    # uri = '/incidents/combined/crowdscores/v1'
    # method = 'get'
    raise NotImplementedError

def incidents_perform_actions(self, **kwargs):
    "Perform a set of actions on one or more incidents, such as adding tags or comments or updating the incident name or description"
    # uri = '/incidents/entities/incident-actions/v1'
    # method = 'post'
    args_validation = {
        'action_parameters' : list,
        'ids' : list,
    }
    validate_kwargs(args_validation, kwargs, required=args_validation.keys())

    # validate action parameters
    for action in kwargs.get('action_parameters'):
        if not isinstance(action, dict):
            raise ValueError()
        if sorted(('name', 'value')) != sorted(set(action.keys())):
            raise ValueError(f"Keys for action_parameter have to be name, value only, got: {sorted(set(action.keys()))}")
    logger.debug(kwargs)


    raise NotImplementedError

def incidents_get_details(self, **kwargs):
    """ Get details on incidents by providing a list of incident IDs

    returns the raw object so you can look for errors and pagination and so forth

    requires:
    - ids (list) - a list of incident IDs

    returns JSON data, response key has the following sub-keys: [
                        'incident_id', 'incident_type', 'cid', 
                        'host_ids', 'hosts', 
                        'created', 'start', 'end', 'state', 
                        'status', 'tactics', 'techniques', 'objectives', 'users', 'fine_score',
                        ])

    swagger docs: https://assets.falcon.crowdstrike.com/support/api/swagger.html#/incidents/GetIncidents
    """
    uri = '/incidents/entities/incidents/GET/v1'
    method = 'post'
    args_validation = {
        'ids' : list,
    }
    validate_kwargs(args_validation, kwargs, required=args_validation.keys())
    response = self.request(uri=uri,
                            request_method=method,
                            data=kwargs,
                            )
    return response.json()

def incidents_behaviors_by_id(self, **kwargs):
    """Get details on behaviors by providing behavior IDs """
    # uri = '/incidents/entities/behaviors/GET/v1'
    # method = 'post'
    raise NotImplementedError

def incidents_query_behaviors(self, **kwargs):
    """Search for behaviors by providing an FQL filter, sorting, and paging details"""
    # uri = '/incidents/queries/behaviors/v1'
    # method = 'get'
    raise NotImplementedError

def incidents_query(self, **kwargs):
    """ Search for incidents by providing an FQL filter, sorting, and paging details

    returns a list of incidents in the format like "inc:aaaabbbbc9b94d0095fde66d407289ec:aaaabbbbe17048ad99f22746082617b5"

    docs: https://falcon.crowdstrike.com/support/documentation/86/detections-monitoring-apis

    args:
        - sort (str)
        - filter (str)
        - offset (int)
        - limit (int) - max 500, min 1

    filter examples:
        status: '20' # new
        status: '25' # reopened
        status: '30' # in progress
        status: '40' # closed

        score_range:'7.5 - 10'

        tags: 'True Positive', 'Ignored', 'Lateral Movement'

    """
    uri = '/incidents/queries/incidents/v1'
    method = 'get'
    args_validation = {
        'sort' : str,
        'filter' : str,
        'offset' : int,
        'limit' : int,
    }
    validate_kwargs(args_validation, kwargs)

    if 'limit' in kwargs:
        if int(kwargs.get('limit')) > 500:
            raise ValueError("Maximum of 500 for 'limit' on this endpoint.")
        if int(kwargs.get('limit')) < 1:
            raise ValueError("Minimum of 1 for 'limit' on this endpoint.")

    response = self.request(uri=uri,
                            request_method=method,
                            data=kwargs,
                            )
    if response.status_code == 400:
        logger.debug("Got 400 status code, potentially too large a response (max 500), or invalid filter.")
    if 'resources' in response.json():
        data = response.json().get('resources')
    else:
        logger.error("Didn't get a response")
        data = response.json()
    return data
