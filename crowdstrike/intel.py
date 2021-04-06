""" implements the various intel endpoint things """

import json

from loguru import logger

from .utilities import validate_kwargs

__all__ = ['get_intel_indicators']
THIS_SHOULD_FAIL = "True"

def get_intel_indicators(self, **kwargs):
    """ Get info about indicators that match provided FQL filters.

    https://assets.falcon.crowdstrike.com/support/api/swagger.html#/intel/QueryIntelIndicatorEntities

- offset (int) - Set the starting row number to return indicators from.
    Defaults to 0.

- limit (int) - Set the number of indicators to return.
    The number must be between 1 and 50000

- sort (str) - Order fields in ascending or descending order.
    Ex: published_date|asc.

- filter (str) - Filter your query by specifying FQL filter parameters.
    Filter parameters include:
    _marker, actors, deleted, domain_types, id, indicator,
    ip_address_types, kill_chains, labels, labels.created_on,
    labels.last_valid_on, labels.name, last_updated, malicious_confidence, malware_families, published_date, reports, targets, threat_types, type, vulnerabilities.

- q (str) - Perform a generic substring search across all fields.
- include_deleted (bool) - If true, include both published and deleted indicators in the response.
    Defaults to false.
    """

    method = 'get'
    uri = '/intel/combined/indicators/v1'
    args_validation = {
        'offset' : int,
        'limit' : int,
        'sort' : str,
        'filter' : str,
        'query' : str,
        'include_deleted' : bool,
    }
    validate_kwargs(args_validation, kwargs)
    logger.debug(f"kwargs: {json.dumps(kwargs)}")

    if 'limit' in kwargs:
        if (kwargs.get("limit") < 1) or (kwargs.get("limit") > 50000):
            raise ValueError("limit needs to be from 1-50000")

    # TODO: it's possible this'll throw a 400 error with the following:
    #     {
    #     "meta": {
    #         "query_time": 0.000331244,
    #         "powered_by": "msa-api",
    #         "trace_id": "xxxxxxxxxxx"
    #     },
    #     "resources": [],
    #     "errors": [
    #         {
    #         "code": 400,
    #         "message": "restricted API can only start from offset=0"
    #         }
    #     ]
    #     }
    # This doesn't happen on all accounts but it should be handled with better logging

    response = self.request(uri=uri,
                            request_method=method,
                            data=kwargs,
                            )
    logger.debug(response.json())
    return response.json()
