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

def test_create_rtr_session(crowdstrike_client=crowdstrike):
    """ test create_rtr_session, should return a session ID """
    host = crowdstrike_client.hosts_query_devices(filter="product_type_desc:'Workstation'+status:'normal'+platform_name:'Windows'", limit=1)
    logger.debug(host)

    device_id = host.get('resources')[0]

    session_details = crowdstrike_client.create_rtr_session(device_id=device_id)
    logger.debug(session_details)

    assert session_details.get('errors', None) in (None, [])
    if session_details.get('resources') and len(session_details.get('resources')) > 0:
        assert 'session_id' in session_details.get('resources')[0]
        assert isinstance(session_details.get('resources')[0].get('session_id'), str)

def test_delete_rtr_session(crowdstrike_client=crowdstrike):
    """ test delete_rtr_session, only works if create does! """
    host = crowdstrike_client.hosts_query_devices(filter="product_type_desc:'Workstation'+status:'normal'+platform_name:'Windows'", limit=1)
    logger.debug(host)

    device_id = host.get('resources')[0]

    session_details = crowdstrike_client.create_rtr_session(device_id=device_id)
    logger.debug(session_details)

    assert session_details.get('errors', None) in (None, [])
    if session_details.get('resources') and len(session_details.get('resources')) > 0:
        assert 'session_id' in session_details.get('resources')[0]
        assert isinstance(session_details.get('resources')[0].get('session_id'), str)

    response = crowdstrike_client.delete_rtr_session(session_id=session_details.get('resources')[0].get('session_id'))
    logger.debug(response)

    assert response.status_code == 204

def test_invalid_rtr_session(crowdstrike_client=crowdstrike):
    """ test delete_rtr_session with a junk ID """
    response = crowdstrike_client.delete_rtr_session(session_id='This test better fail')
    logger.debug(response)
    assert response.status_code == 400