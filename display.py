from bash import exec_bash


def get_PRIME_sync_info(available_executables):

    PRIME_sync_info = {"error": False, "nb_supported": 0, "nb_enabled": 0}

    if "xrandr" not in available_executables:
        print("ERROR : PRIME sync : xrandr not available, cannot check PRIME support")
        PRIME_sync_info["error"] = True
        return PRIME_sync_info

    returncode, xrandr_output, stderr = exec_bash("xrandr --verbose")

    if returncode != 0:
        print("ERROR : PRIME sync : xrandr returned an error : %s" % stderr)
        PRIME_sync_info["error"] = True
        return PRIME_sync_info

    for line in xrandr_output.splitlines():

        if "PRIME Synchronization" in line:

            line_stripped = line.strip().replace(" ", "")

            colon_index = line_stripped.find(":")

            if colon_index == -1:
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
