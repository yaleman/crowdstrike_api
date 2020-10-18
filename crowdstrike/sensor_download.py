""" implements the various sensor-download endpoint things """

import errno

from loguru import logger

def download_sensor(self, sensorid: str, destination_filename: str):
    """ downloads a sensor id to the filename """
    uri = '/sensors/entities/download-installer/v1'
    data = {
        'id' : sensorid,
    }
    try:
        logger.debug(f"Writing intaller to {destination_filename}")
        with open(destination_filename, 'wb') as file_handle:
            response = self.request(
                uri=uri,
                request_method='get',
                data=data,
            )
            logger.debug(response.headers)
            response.raise_for_status()

            file_handle.write(response.content)
        return True

    except IOError as file_write_error:
        error_number = file_write_error.errno
        error_string = file_write_error.strerror
        if error_number == errno.EACCES:
            logger.error(f"error {error_number}, {error_string} - Permission fail")
        elif error_number == errno.EISDIR:
            logger.error(f"error {error_number}, {error_string} - Path is a directory")
        else:
            logger.error(f"error {error_number}, {error_string}")
        return False

def get_ccid(self):
    """ returns the CCID for installers """
    req = self.request(request_method='get', uri="/sensors/queries/installers/ccid/v1")
    req.raise_for_status()

    if req.status_code == 200:
        retval = req.json().get('resources')[0]
    else:
        retval = False
    return retval

def get_latest_sensor_id(self, filter_string: str = ""):
    """ returns the ids of the latest sensor IDs

        suggested filter: 'platform:mac' or 'platform:windows'
    """
    response = self.get_sensor_installer_ids(
        sort_string="release_date|desc",
        filter_string=filter_string,)
    if response:
        retval = response[0]
    else:
        retval = False
    return retval

def get_sensor_installer_details(self, sensorid: str):
    """
    returns a dict about a particular sensor ID, or False if it can't find anything useful
    """
    logger.debug(f"Sensor ID: {sensorid}")
    uri = "/sensors/entities/installers/v1"
    data = {
        'ids' : sensorid,
        }
    response = self.request(uri=uri,
                            request_method='get',
                            data=data,
                            )

    response.raise_for_status()
    logger.debug(response.headers)
    if not response.json().get('resources', False):
        retval = False
    else:
        retval = response.json().get('resources', False)[0]
    return retval

def get_sensor_installer_ids(self, sort_string: str = "", filter_string: str = ""):
    """
    returns a list of installer IDs, they're a list of SHA256's
    """
    logger.debug(f"sort_string: '{sort_string}', filter_string: '{filter_string}'")
    uri = '/sensors/queries/installers/v1'

    data = {
        'sort' : sort_string,
        'filter' : filter_string,
    }

    response = self.request(request_method='get', uri=uri, data=data)
    #logger.debug(response.json())
    logger.debug("Request headers")
    logger.debug(response.request.headers)
    #logger.debug(dir(response))
    response.raise_for_status()


    # TODO: handle pagination
    return response.json().get('resources', False)
