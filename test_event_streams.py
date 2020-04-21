#!/usr/bin/env python3

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



crowdstrike = CrowdstrikeAPI(CLIENT_ID, CLIENT_SECRET)

logger.info("Testing get_event_streams()")

streams = crowdstrike.get_event_streams("testing123")

if not streams.get("resources", False):
    logger.error(json.dumps(streams))
    raise ValueError("No resources in stream response")

for resource in streams.get('resources'):
    logger.info("Stream found")
    logger.info(f"dataFeedURL: {resource.get('dataFeedURL')}")