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

def test_query_devices(crowdstrike_client=crowdstrike):
    """ tests query_devices() """
    logger.info("Testing get_event_streams()")
    hosts = crowdstrike_client.hosts_query_devices(limit=5)
    logger.debug(hosts)
    assert hosts is not None

def test_hosts_query_devices(crowdstrike_client=crowdstrike):
    """ test hosts_query_devices() """
    logger.info("testing hosts_detail")
    hosts = crowdstrike.hosts_query_devices(limit=5)
    test = crowdstrike_client.hosts_detail(ids=hosts.get('resources'))
    logger.debug(json.dumps(test))
    assert hosts is not None
    assert test is not None
# logger.debug("testing host_action")

# test = crowdstrike.host_action(action='lift_containment', ids=['123456789'])
# logger.debug(json.dumps(test, indent=2))

def test_hosts_hidden(crowdstrike_client=crowdstrike):
    """ test hosts_hidden() """
    logger.info('testing hosts_hidden()')
    test = crowdstrike_client.hosts_hidden(limit=10)
    logger.debug(json.dumps(test))
    assert test is not None
