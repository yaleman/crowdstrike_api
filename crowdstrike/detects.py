""" implements the various detects endpoint things """

from loguru import logger

VALID_DETECT_STATUS = ['new', 'in_progress', 'true_positive', 'false_positive', 'ignored']

def get_detects(self, **kwargs):
    """ Search for detection IDs that match a given query

    offset (int) (query) The first detection to return, where 0 is the latest detection. Use with the limit parameter to manage pagination of results.

    limit (int) (query)	The maximum number of detections to return in this response (default: 9999; max: 9999). Use with the offset parameter to manage pagination of results.

    sort (str) (query)	 Sort detections using these options:
        - first_behavior: Timestamp of the first behavior associated with this detection
        - last_behavior: Timestamp of the last behavior associated with this detection
        - max_severity: Highest severity of the behaviors associated with this detection
        - max_confidence: Highest confidence of the behaviors associated with this detection
        - adversary_id: ID of the adversary associated with this detection, if any
        - devices.hostname: Hostname of the host where this detection was detected
        Sort either asc (ascending) or desc (descending). For example: last_behavior|asc

    filter (str) (query) Filter detections using a query in Falcon Query Language (FQL) An asterisk wildcard * includes all results.
        Common filter options include:
        - status
        - device.device_id
        - max_severity
        The full list of valid filter options is extensive. Review it in the documentation inside the Falcon console.

    q (str) (query)	Search all detection metadata for the provided string
"""
    uri = '/detects/queries/detects/v1'
    response = self.request(uri=uri,
                            request_method='get',
                            data=kwargs,
                            )
    logger.debug(response)
    response.raise_for_status()

    return response.json()

def get_detections(self, ids: list):
    """ view detection information """

    if not isinstance(ids, list):
        raise TypeError(f"ids should be of type 'list', got '{type(ids)}'")

    uri = '/detects/entities/summaries/GET/v1'
    response = self.request(uri=uri,
                            request_method='post',
                            data={'ids' : ids},
                            )
    logger.debug(response)
    response.raise_for_status()

    return response.json()

def update_detection(self, **kwargs):
    """ modify the date, assignee and visibility of detections

    assigned_to_uuid (string) - uuid of user ID that the task is assigned to

    ids (list) - one or more detection ID - from get_detects()

    show_in_ui (bool) - show the detection in falcohn. Most commonly used together with the status key's false_positive value

    status (str) - one of the following:
     - new
     - in_progress
     - true_positive
     - false_positive
     - ignored

    comment (str) optional comment to add to the detection
    """
    uri = '/detects/entities/detects/v2'

    if 'status' in kwargs and kwargs.get('status') not in VALID_DETECT_STATUS:
        set_status = kwargs.get('status')
        raise ValueError(f"Status '{set_status}' invalid - should be in {VALID_DETECT_STATUS}")
    response = self.request(uri=uri,
                            request_method='patch',
                            data=kwargs,
                            )
    logger.debug(response)
    response.raise_for_status()

    return response.json()
