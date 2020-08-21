#!/usr/bin/env python3
""" terrible tests for the sensors endpoints """
import json
import os
import sys
import tempfile

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


def test_get_detects():
    """ searches for the latest detection ID """

    crowdstrike = CrowdstrikeAPI(CLIENT_ID, CLIENT_SECRET)
    response = crowdstrike.get_detects(offset=0, limit=1)
    logger.debug(response)
    assert not response.get('errors')
    # should work, unless you've never had a detection on your account, which would be surprising ^_^
    assert response.get('resources')

def test_get_detections():
    """ pulls information on the last five detections """
    crowdstrike = CrowdstrikeAPI(CLIENT_ID, CLIENT_SECRET)

    response = crowdstrike.get_detects(offset=0, limit=5)
    ids = response.get('resources')
    assert ids

    response = crowdstrike.get_detections(ids=ids)
    logger.debug(response)
    assert not response.get('errors')
    # should work, unless you've never had a detection on your account, which would be surprising ^_^
    assert response.get('resources')



if __name__ == '__main__':
    test_get_detections()
