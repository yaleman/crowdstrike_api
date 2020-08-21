""" utility functions for the crowdstrike API """

def validate_kwargs(args_validation: dict, kwargs: dict, required: list = None):
    """ validates arguments pushed to the function

    args
    - args_validation: dict of key/types to check, example below checks if action is a string and ids is a list
            args_validation = {
                'action' : str,
                'ids' : list,
            }
    - required: if passed, it'll require those keys to be set

    """
    for key in kwargs:
        if key not in args_validation:
            raise ValueError(f"{key} not a valid argument")
        if not isinstance(kwargs[key], args_validation[key]):
            raise TypeError(f"{key} not the valid type, should be: {args_validation[key]}, was {type(kwargs[key])}")
    if required:
        for key in required:
            if key not in kwargs:
                raise ValueError(f"argument {key} needs to be set")
    return True
