from ..utils.bash import exec_bash


def get_limits_info(system_info):

    return parse_ulimits()


def parse_ulimits():

    limits_info = _make_empty_limits_info()

    returncode, ulimit_output, stderr = exec_bash("ulimit -Hn")  # ulimit is not an executable

    ulimit_output = ulimit_output.strip()

    if returncode != 0:
        _print_ulimit_error("ulimit returned an error : %s" % stderr)
        limits_info["error"] = True
        return limits_info

    try:
        limit_value = int(ulimit_output)
    except ValueError:
        _print_ulimit_error("non-int value : %s" % ulimit_output)
        limits_info["error"] = True
        return limits_info

    limits_info["file_limit"] = limit_value

    return limits_info


def _make_empty_limits_info():
    return {"error": False, "file_limit": 0}


def _print_ulimit_error(msg):
    print("ERROR : ulimit parsing : %s" % msg)
