#!/usr/bin/env python3

""" tests the "rtr" endpoints """

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

crowdstrike = CrowdstrikeAPI(CLIENT_ID, CLIENT_SECRET) # pylint: disable=invalid-name


def test_list_rtr_session_ids(crowdstrike_client=crowdstrike):
    """ test delete_rtr_session with a junk ID """
    response = crowdstrike_client.list_rtr_session_ids()
    logger.debug(response)
    assert not response.get('errors')

    response = crowdstrike_client.list_rtr_session_ids(limit=1)
    logger.debug(response)
    assert len(response.get('resources')) == 1
    assert not response.get('errors')

    response = crowdstrike_client.list_rtr_session_ids(filter="user_id: '@me'")
    logger.debug(response)
    assert not response.get('errors')


def test_create_rtr_session(crowdstrike_client=crowdstrike):
    """ test create_rtr_session, should return a session ID """
    host = crowdstrike_client.hosts_query_devices(filter="product_type_desc:'Workstation'+status:'normal'+platform_name:'Windows'",
                                                  limit=1,
                                                  sort="last_seen.desc",
                                                  )
    logger.debug("host query result")
    logger.debug(host)
    assert len(host.get('resources')) > 0
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

    if session_details.get('errors'):
        for error in session_details.get('errors'):
            logger.error(json.dumps(error, indent=4))
            # 40010 is "couldn't establish comms"
            # {'code': 40010, 'message': '{"code":40401,"message":"Could not establish sensor comms"}'}
            # {'code': 40401, 'message': 'Could not establish sensor comms'}
            if error.get('code') in (40010,40401):
                logger.warning("Couldn't establish sensor comms")
            else:
                raise ValueError(f"Bad error came along: {error}")


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


def test_rtr_basic_ls(crowdstrike_client=crowdstrike):
    """ test some rtr commands """
    # filter for recently online windows devices
    fql_filter = "+".join([
        "product_type_desc:'Workstation'",
        "status:'normal'",
        "platform_name:'Windows'",
        f"last_seen: >='{date.today()}'",
    ])

    logger.debug(f"FQL Filter: {fql_filter}")
    host = crowdstrike_client.hosts_query_devices(filter=fql_filter, limit=1)
    logger.debug(host)

    if not host.get('resources'):
        logger.warning("No resources found, skipping test")
        return

    device_id = host.get('resources')[0]


    session_details = crowdstrike_client.create_rtr_session(device_id=device_id)
    logger.debug("Created session, details:")
    logger.debug(session_details)

    assert session_details.get('errors', None) in (None, [])
    if session_details.get('resources') and len(session_details.get('resources')) > 0:
        assert 'session_id' in session_details.get('resources')[0]
        session_id = session_details.get('resources')[0].get('session_id')
        assert isinstance(session_id, str)

    response = crowdstrike_client.rtr_execute_command(base_command='ls', command_string='ls c:\\', session_id=session_id)
    logger.debug(response)
    assert not response.get('errors')

    cloud_request_id = response.get('resources', [{}])[0].get('cloud_request_id')

    logger.debug(f"Waiting for response in cloud_request_id {cloud_request_id} ")

    response = crowdstrike_client.rtr_command_status_wait(cloud_request_id=cloud_request_id, interval=1, maxtime=15)
    logger.debug(response)


    response = crowdstrike_client.delete_rtr_session(session_id=session_id)
    logger.debug(response)
