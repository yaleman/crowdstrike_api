""" handler for incidents """

def incidents_get_crowdscores(self, **kwargs):
    """ Query environment wide CrowdScore and return the entity data """
    uri = '/incidents/combined/crowdscores/v1'
    method = 'get'
    raise NotImplementedError

def incidents_perform_actions(self, **kwargs):
    "Perform a set of actions on one or more incidents, such as adding tags or comments or updating the incident name or description"
    uri = '/incidents/entities/incident-actions/v1'
    method = 'post'
    raise NotImplementedError

def incidents_get_details(self, **kwargs):
    """ Get details on incidents by providing incident IDs"""
    uri = '/incidents/entities/incidents/GET/v1'
    method = 'post'
    raise NotImplementedError

def incidents_behaviors_by_id(self, **kwargs):
    """Get details on behaviors by providing behavior IDs """
    uri = '/incidents/entities/behaviors/GET/v1'
    method = 'post'
    raise NotImplementedError

def incidents_query_behaviors(self, **kwargs):
    """Search for behaviors by providing an FQL filter, sorting, and paging details"""
    uri = '/incidents/queries/behaviors/v1'
    method = 'get'
    raise NotImplementedError

def incidents_query(self, **kwargs):
    """Search for incidents by providing an FQL filter, sorting, and paging details"""
    uri = '/incidents/queries/incidents/v1'
    method = 'get'
    raise NotImplementedError
