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

# find a few different crowdstrike ids
ids = crowdstrike.get_sensor_installer_ids(
    sort_string="release_date|desc",
    filter_string='platform:"mac"'
)
ids = crowdstrike.get_sensor_installer_ids(
    sort_string="release_date|desc",
)
ids = crowdstrike.get_sensor_installer_ids(
    filter_string='platform:"mac"'
)


# test downloading the latest macOS installer
maclatest = crowdstrike.get_latest_sensor_id(filter_string='platform:"mac"')
logger.info(
    json.dumps(
        # also tests showing an installer's data
        crowdstrike.get_sensor_installer_details(maclatest),
        indent=2
    )
)

logger.info("Testing download to temporary directory....")
# this'll write it to a temporary directory which is removed afterwards
with tempfile.TemporaryDirectory() as tmpdirname:
    filename = f'{tmpdirname}/FalconSensorMacOS.pkg'
    response = crowdstrike.download_sensor(maclatest, filename)
    if not os.path.exists(filename):
        raise ValueError(f'Failed to download file :(')
logger.info("Download looks to have worked!")
