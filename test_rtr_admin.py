#!/usr/bin/env python3

""" tests the "hosts" endpoints """

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

def test_search_rtr_scripts_empty_filter(crowdstrike_client=crowdstrike):
    """ test with an empty filter, should return something """
    scripts = crowdstrike_client.search_rtr_scripts()
    logger.debug(scripts)
    assert scripts is not None
    assert scripts.get('errors', None)  in (None, [])

def test_search_rtr_scripts_offset(crowdstrike_client=crowdstrike):
    """ test with an offset filter, should return something """
    scripts = crowdstrike_client.search_rtr_scripts(offset=1, limit=1)
    logger.debug(scripts)
    assert scripts is not None
    assert scripts.get('errors', None)  in (None, [])
