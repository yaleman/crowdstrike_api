* THIS IS NO LONGER UPDATED *


# Crowdstrike API

Implements some of the functions to interface with the [Crowdstrike APIs](https://assets.falcon.crowdstrike.com/support/api/swagger.html).

Want to contribute? Log an issue or PR on the Repo.

To enable logging, use [loguru](https://github.com/Delgan/loguru) and run `logger.enable("crowdstrike")` in your script.

## Checking that all the endpoints are covered

`validate_api_endpoints.py` needs the `swagger.json` file from the documentation page on [crowdstrike.com](https://assets.falcon.crowdstrike.com/support/api/swagger.html), then you can check everything has an actionable method.

Eg:

    2020-10-14 18:56:57.801 | INFO     | __main__:<module>:60 - [OK] create_rtr_session() implements /real-time-response/entities/sessions/v1 : post
    2020-10-14 18:56:57.801 | INFO     | __main__:<module>:60 - [OK] delete_rtr_session() implements /real-time-response/entities/sessions/v1 : delete
    2020-10-14 18:56:57.802 | ERROR    | __main__:<module>:64 - Path not found /real-time-response/queries/put-files/v1 : get
    2020-10-14 18:56:57.802 | INFO     | __main__:<module>:60 - [OK] search_rtr_scripts() implements /real-time-response/queries/scripts/v1 : get
    2020-10-14 18:56:57.802 | INFO     | __main__:<module>:60 - [OK] list_rtr_session_ids() implements /real-time-response/queries/sessions/v1 : get
    2020-10-14 18:56:57.802 | ERROR    | __main__:<module>:64 - Path not found /samples/entities/samples/v2 : post
    2020-10-14 18:56:57.802 | ERROR    | __main__:<module>:64 - Path not found /sensors/combined/installers/v1 : get
    2020-10-14 18:56:57.802 | ERROR    | __main__:<module>:64 - Path not found /sensors/entities/datafeed-actions/v1/{partition} : post
    2020-10-14 18:56:57.803 | ERROR    | __main__:<module>:64 - Path not found /sensors/entities/datafeed/v2 : get
    2020-10-14 18:56:57.803 | ERROR    | __main__:<module>:64 - Path not found /sensors/entities/download-installer/v1 : get

... lots to do.