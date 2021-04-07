from re import compile

POSITIVE_FLOAT_REGEX = compile("[^0-9.]")


def convert_to_float(element) -> float:
    """
    Safely converts anything to a positive float
    """
    element = POSITIVE_FLOAT_REGEX.sub("", str(element))
    if element != "":
        return float(element)
    else:
        return float(0)


def get_key(dictionary: dict, val):
    """
    Returns the first dictionary key that has a particular value.
    """
    for key, value in dictionary.items():
        if value == val:
            return key
    return None