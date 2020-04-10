#!/usr/bin/env python3

import json
import os
import sys
import tempfile

try:
    from loguru import logger
    from crowdstrike import CrowdstrikeAPI
    from config import CLIENT_ID, CLIENT_SECRET
except ImportError as import_error:
    sys.exit(f"Error importing required library: {import_error}")

logger.enable("crowdstrike")

crowdstrike = CrowdstrikeAPI(CLIENT_ID, CLIENT_SECRET)

# find the crowdstrike mac ids
ids = crowdstrike.get_sensor_installer_ids(
    sort_string="release_date|desc",
    filter_string="platform:mac",
)
logger.info(
    json.dumps(
        ids, 
        indent=2
    )[:150] # limit the response to 150 chars
)
# grabbing a single installer's information
ids = crowdstrike.get_sensor_installer_ids(
    sort_string="release_date|desc",
    filter_string="platform:mac",
)
logger.info(
    json.dumps(
        crowdstrike.get_sensor_installer_details(ids[0]),
        indent=2
    )
)

# test downloading the latest macOS installer
# this'll write it to a temporary directory which is removed afterwards
maclatest = crowdstrike.get_latest_sensor_id(filter_string='platform:mac')
logger.info(
    json.dumps(
        crowdstrike.get_sensor_installer_details(maclatest),
        indent=2
    )
)
logger.info("Testing download to temporary directory....")
with tempfile.TemporaryDirectory() as tmpdirname:
    filename = f'{tmpdirname}/FalconSensorMacOS.pkg'
    response = crowdstrike.download_sensor(maclatest, filename)
    if not os.path.exists(filename):
        raise ValueError(f'Failed to download file :(')
logger.info("Download looks to have worked!")
