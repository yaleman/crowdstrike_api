#!/usr/bin/env python3

""" tries to work out if we've covered all the possible endpoints """

import inspect
#import ast
import json
import os
import sys

from loguru import logger

from crowdstrike import CrowdstrikeAPI

found_implementations = {}

# parse the source code of the implementation to find the endpoints we use
logger.debug(dir(CrowdstrikeAPI))
for function_name in [ fname for fname in dir(CrowdstrikeAPI) if not fname.startswith('_')]:
    logger.debug(f"Checking function {function_name}")
    target_function = getattr(CrowdstrikeAPI,function_name)

    target_uri = False #pylint: disable=invalid-name
    target_method = False #pylint: disable=invalid-name
    SOURCE_CODE = inspect.getsource(target_function)
    # some functions don't use requests, but most should
    SKIP_OAUTH_REQUEST_CHECK = ('request', 'do_request', 'get_token', 'revoke_token')
    if 'do_request' not in SOURCE_CODE and 'self.request' not in SOURCE_CODE and function_name not in SKIP_OAUTH_REQUEST_CHECK and 'NotImplementedError' not in SOURCE_CODE:
        logger.warning(f"do_request or request call not in {function_name}()")
        #logger.warning(SOURCE_CODE)
    for line in SOURCE_CODE.split("\n"):
        if line.strip().startswith('uri = '):
            target_uri = line.strip().split()[-1].replace("'", '')
            logger.debug(f"Found new target URI: {target_uri}")
        elif line.strip().startswith('method = '):
            target_method = line.strip().split()[-1].replace("'", '')
            logger.debug(f"Found new target method: {target_method}")
    if target_method and target_uri:
        logger.info(f"{function_name} implements {target_uri} [{target_method}]")
        if target_uri not in found_implementations:
            found_implementations[target_uri] = {}
        found_implementations[target_uri][target_method] = function_name

SWAGGER_FILE = 'swagger.json'

if not os.path.exists(SWAGGER_FILE):
    sys.exit(f"You'll need to download {SWAGGER_FILE} from the API docs, quitting.")

with open(SWAGGER_FILE) as fh:
    SWAGGER_DATA = json.load(fh)

logger.info(f"Host: {SWAGGER_DATA.get('host')}")

for path in SWAGGER_DATA.get('paths'):
    #logger.info(path)
    pathdata = SWAGGER_DATA.get('paths').get(path)
    for pathmethod in pathdata:
        #logger.info(pathmethod)
        if path in found_implementations:
            if pathmethod in found_implementations.get(path):
                logger.info(f"[OK] {found_implementations[path][pathmethod]}() implements {path} : {pathmethod}")
            else:
                logger.error(f"Path {path} found but not method {pathmethod}")
        else:
            logger.error(f"Path not found {path} : {pathmethod}")
