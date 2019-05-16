from ..utils.bash import exec_bash

KNOWN_DISTRIBUTIONS = ["archlinux", "manjaro", "ubuntu"]


def get_distribution_info(system_info):

    assert "available_executables" in system_info.keys()

    if system_info["available_executables"]["hostnamectl"]:
        distribution_info = parse_distribution_from_command("hostnamectl", "Operating System")
        if not distribution_info["error"]:
            return distribution_info

    if system_info["available_executables"]["lsb_release"]:
        distribution_info = parse_distribution_from_command("lsb_release -d", "Description")
        if not distribution_info["error"]:
            return distribution_info

    _print_distribution_error("no distribution name found")
    distribution_info["error"] = True
    return distribution_info


def parse_distribution_from_command(bash_command, key):

    distribution_info = _make_empty_distribution_info()

    returncode, command_output, stderr = exec_bash(bash_command)

    if returncode != 0:
        _print_distribution_error("%s returned an error : %s" % (bash_command, stderr))
        distribution_info["error"] = True
        return distribution_info

    for line in command_output.splitlines():

        line = line.strip()

        if key + ":" in line:

            line_nospaces = line.replace(" ", "")

            colon_index = line_nospaces.find(":")

            if colon_index == -1 or colon_index == len(line_nospaces) - 1:
                _print_distribution_error("%s : cannot parse \"%s\" line : %s" % (bash_command, key, line))
                distribution_info["error"] = True
                return distribution_info

            distribution_str = line_nospaces[colon_index+1:]
            distribution_str_lower = distribution_str.lower()

            for distrib_name in KNOWN_DISTRIBUTIONS:
                if distrib_name in distribution_str_lower:
                    distribution_info["name"] = distribution_str_lower
                    break
            else:
                distribution_info["name"] = distribution_str_lower

            return distribution_info

    else:

        _print_distribution_error("%s : no distribution name found" % bash_command)
        distribution_info["error"] = True
        return distribution_info


def _make_empty_distribution_info():
    return {"error": False, "name": ""}


def _print_distribution_error(msg):
    print("ERROR : distribution detection : %s" % msg)
