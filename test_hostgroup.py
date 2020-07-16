#!/usr/bin/env python3

""" tests the "hosts" endpoints """

import json
import os
import sys
# import tempfile

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



crowdstrike = CrowdstrikeAPI(CLIENT_ID, CLIENT_SECRET) # pylint: disable=invalid-name

def test_host_search_empty_filter(crowdstrike_client=crowdstrike):
    """ test with an empty filter, should return something """
    hostgroups = crowdstrike_client.search_host_groups()
    logger.debug(hostgroups)
    assert hostgroups is not None
    assert hostgroups.get('errors', None)  in (None, [])

def test_host_search_offset(crowdstrike_client=crowdstrike):
    """ test with an offset and limit, should return something """
    hostgroups = crowdstrike_client.search_host_groups(offset=1,limit=1)
    logger.debug(hostgroups)
    assert hostgroups is not None
    assert hostgroups.get('errors', None)  in (None, [])

def test_host_search_dynamic_group(crowdstrike_client=crowdstrike):
    """ test with an empty filter, should return something """
    hostgroups = crowdstrike_client.search_host_groups(filter="group_type: 'dynamic'")
    logger.debug(hostgroups)
    assert hostgroups is not None
    assert hostgroups.get('errors', None)  in (None, [])

def test_get_host_groups(crowdstrike_client=crowdstrike):
    """ relies on search_host_groups to work to get something to look for """
    searchids = crowdstrike_client.search_host_groups(limit=5)
    ids = [group.get('id') for group in searchids.get('resources')]
    logger.debug(f"Searching for {ids}")

    result = crowdstrike_client.get_host_groups(ids=ids)
    logger.debug(result)

    assert result is not None
    assert result.get('errors', None)  in (None, [])
