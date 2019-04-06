import os


def get_cpu_governor_info(system_info):

    return parse_cpu_governor()


def parse_cpu_governor():

    cpu_governor_info = _make_empty_cpu_governor_info()

    available_governors_path = "/sys/devices/system/cpu/cpu0/cpufreq/scaling_available_governors"
    current_governor_path = "/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"

    #
    # Returning available governors

    if not os.path.isfile(available_governors_path):
        _print_cpu_governor_error("%s does not exist" % available_governors_path)
        cpu_governor_info["error"] = True
        return cpu_governor_info
    else:
        with open(available_governors_path, "r") as f:
            available_governors_str = f.read()

        available_governors = available_governors_str.split(" ")
        available_governors = [g_str.strip() for g_str in available_governors]

        if len(available_governors) == 0:
            _print_cpu_governor_error("No CPU governors returned by %s" % available_governors_path)
            cpu_governor_info["error"] = True
            return cpu_governor_info
        else:
            cpu_governor_info["available_governors"] = available_governors

    #
    # Returning current governor

    if not os.path.isfile(current_governor_path):
        _print_cpu_governor_error("%s does not exist" % current_governor_path)
        cpu_governor_info["error"] = True
        return cpu_governor_info
    else:
        with open(current_governor_path, "r") as f:
            current_governor = f.read()

        current_governor = current_governor.strip()

        if current_governor == "":
            _print_cpu_governor_error("No CPU governor returned by %s" % current_governor_path)
            cpu_governor_info["error"] = True
            return cpu_governor_info
        else:
            cpu_governor_info["current_governor"] = current_governor

    return cpu_governor_info


def _make_empty_cpu_governor_info():
    return {"error": False,  "available_governors": [],
            "current_governor": ""}


def _print_cpu_governor_error(msg):
    print("ERROR : CPU governor detection : %s" % msg)
