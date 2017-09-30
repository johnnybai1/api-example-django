# General helper functions
def build_dictionary(dic, keys):
    """
    Intended for building payload for changed fields in patient
    demographic form.
    """
    return {key: dic[key] for key in keys}


def within_time_limit(now, ref, limit):
    """
    Checks if the current time is within some range of another time.
    :param now: the current time
    :param ref: the refrence time we're comparing to
    :param limit: number of minutes after ref such that the current time
        is within an acceptable range
    :return: True if now - ref < limit, otherwise false
    """
    print now - ref