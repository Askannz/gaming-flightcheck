from ..utils.bash import exec_bash


def get_PRIME_sync_info(system_info):

    assert "executables_paths" in system_info.keys()

    if not system_info["executables_paths"]["xrandr"]:
        PRIME_sync_info = _make_empty_PRIME_sync_info()
        PRIME_sync_info["error"] = True
        return PRIME_sync_info

    PRIME_sync_info = parse_xrandr_PRIME_sync(system_info)

    return PRIME_sync_info


def parse_xrandr_PRIME_sync(system_info):

    PRIME_sync_info = _make_empty_PRIME_sync_info()

    returncode, xrandr_output, stderr = exec_bash("%s --verbose" % system_info["executables_paths"]["xrandr"])

    if returncode != 0:
        print("ERROR : PRIME sync : xrandr returned an error : %s" % stderr)
        PRIME_sync_info["error"] = True
        return PRIME_sync_info

    for line in xrandr_output.splitlines():

        if "PRIME Synchronization" in line:

            line_stripped = line.strip().replace(" ", "")

            colon_index = line_stripped.find(":")

            if colon_index == -1 or colon_index == len(line_stripped) - 1:
                print("ERROR : PRIME sync : cannot parse \"PRIME Synchronization\" line : %s" % line.strip())
                PRIME_sync_info["error"] = True
                return PRIME_sync_info

            status_str = line_stripped[colon_index+1:]

            try:
                status_int = int(status_str)
            except ValueError:
                print("ERROR : PRIME sync : UsePageAttributeTable has non-int value in line : %s" % line.strip())
                PRIME_sync_info["error"] = True
                return PRIME_sync_info

            if status_int not in [0, 1]:
                print("ERROR : PRIME sync : UsePageAttributeTable value is not boolean in line : %s" % line.strip())
                PRIME_sync_info["error"] = True
                return PRIME_sync_info

            PRIME_sync_info["nb_supported"] += 1

            if status_int == 1:
                PRIME_sync_info["nb_enabled"] += 1

    return PRIME_sync_info


def _make_empty_PRIME_sync_info():
    return {"error": False, "nb_supported": 0, "nb_enabled": 0}
