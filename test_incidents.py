#!/usr/bin/env python3
""" terrible tests for the sensors endpoints """
import json
import os
import sys
import tempfile
import pytest

try:
    from loguru import logger
    from crowdstrike import CrowdstrikeAPI
except ImportError as import_error:
    sys.exit(f"Error importing required library: {import_error}")

# grab config from the file or environment variable
try:
    from config import CLIENT_ID, CLIENT_SECRET
except ImportError:
    if os.environ.get('CLIENT_ID'):
        logger.debug("Using Client ID from environment variable")
        CLIENT_ID = os.environ.get('CLIENT_ID')
    if os.environ.get('CLIENT_SECRET'):
        logger.debug("Using Client Secret from environment variable")
        CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
    if not CLIENT_ID and not CLIENT_SECRET:
        sys.exit("you didn't set the config either via file or environment")

logger.enable("crowdstrike")


def test_incidents():
    """ does some wide-open testing of incidents """

    crowdstrike = CrowdstrikeAPI(CLIENT_ID, CLIENT_SECRET)

    incidents = crowdstrike.incidents_query()
    logger.debug(incidents)

    assert len(incidents) > 0

    for incident in incidents:
        single_incident_details = crowdstrike.incidents_get_details(ids=[incident])
    
        #logger.info(json.dumps(single_incident_details.get('resources')[0], indent=4))
        #logger.debug(single_incident_details.get('resources')[0].get('users'))
        logger.debug(single_incident_details.get('resources')[0].get('users'))
        logger.debug(single_incident_details.get('resources')[0].get('state'))
        #logger.debug(single_incident_details.get('resources')[0].get('assigned_to', 'unassigned'))
    assert not single_incident_details.get('errors')




def test_find_closed_incidents():
    """ does some testing looking for closed incidents """

    crowdstrike = CrowdstrikeAPI(CLIENT_ID, CLIENT_SECRET)

    incidents = crowdstrike.incidents_query(filter="status: '40'")
    assert len(incidents) > 0
    logger.debug(incidents)

def test_find_true_positives():
    """ does some testing looking for true positive incidents """

    crowdstrike = CrowdstrikeAPI(CLIENT_ID, CLIENT_SECRET)

    incidents = crowdstrike.incidents_query(filter="tags: 'True Positive'")
    assert len(incidents) > 0
    logger.debug(incidents)


def test_incidents_perform_actions():
    """ tests some basic things in incidents_perform_actions """

    crowdstrike = CrowdstrikeAPI(CLIENT_ID, CLIENT_SECRET)
    #with pytest.raises(ValueError):
    crowdstrike.incidents_perform_actions(ids=['12345'],
                                                   action_parameters=[{
                                                       'name' : 'tags',
                                                       'value' : '',
                                                   },]
                                                   )
