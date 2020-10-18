#!/usr/bin/env python3

""" tests the basic functionality of the API implementation """

import os
import sys
from datetime import date

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

def test_revoke_token(crowdstrike_client=crowdstrike):
    """ test revoke_token """

    logger.debug(crowdstrike_client.get_token())

    response = crowdstrike_client.revoke_token()
    logger.debug(response)
