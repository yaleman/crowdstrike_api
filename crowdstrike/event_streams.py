""" handles the event-streams endpoints """


def get_event_streams(self, appid: str, format_str: str = "json"):
    """
    Discover all event streams in your environment
    https://assets.falcon.crowdstrike.com/support/api/swagger.html#/event-streams/listAvailableStreamsOAuth2
    """
    uri = '/sensors/entities/datafeed/v2'
    data = {
        'format' : format_str,
    }
    if appid:
        data['appId'] = appid
    else:
        raise ValueError("Need to specify an appid")
    response = self.request(
        uri=uri,
        request_method='get',
        data=data,
        )
    return response.json()

def refresh_event_stream(self, partition: int, appid: str):
    """ refresh an active event stream. use the url returned from get_event_streams
    """

    raise NotImplementedError("sorry, not done yet")
    # action_name = 'refresh_active_stream_session'
    # example valid response
    # {
    # "errors": [
    #     {
    #     "code": 0,
    #     "id": "string",
    #     "message": "string"
    #     }
    # ],
    # "meta": {
    #     "pagination": {
    #     "limit": 0,
    #     "offset": 0,
    #     "total": 0
    #     },
    #     "powered_by": "string",
    #     "query_time": 0,
    #     "trace_id": "string",
    #     "writes": {
    #     "resources_affected": 0
    #     }
    # }
    # }
