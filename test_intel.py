#!/usr/bin/env python3

""" tests the "intel" endpoints """

import json
import os
import sys
from datetime import date
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

# crowdstrike = CrowdstrikeAPI(CLIENT_ID, CLIENT_SECRET) # pylint: disable=invalid-name


def test_get_intel_indicators():
    """ test clean get_intel_indicators """
    crowdstrike = CrowdstrikeAPI(CLIENT_ID, CLIENT_SECRET) # pylint: disable=invalid-name

    response = crowdstrike.get_intel_indicators(limit=10)
    logger.debug(response)
    assert not response.get('errors')

def test_something_indicators():
    """ tests with a set of values that failed once
        this'll fail on a "restricted" account, worked on my test account - JH 2021-03-20
    """
    payload = {
        "offset" : 5,
        "filter" : "last_updated:>1590402620",
        "limit" : 7000,
        "include_deleted" : False,
        "sort" : "last_updated.asc",
    }
    crowdstrike = CrowdstrikeAPI(CLIENT_ID, CLIENT_SECRET) # pylint: disable=invalid-name

    response = crowdstrike.get_intel_indicators(**payload)
    logger.debug(response)
    assert not response.get('errors')
