import os


def get_nvidia_PAT_info(system_info):

    return parse_nvidia_PAT_usage(system_info)


def parse_nvidia_PAT_usage(system_info):

    assert "GPUs_PCI" in system_info.keys()

    nvidia_PAT_info = _make_empty_nvidia_PAT_info()

    if not _check_nvidia_module_active(system_info):
        return nvidia_PAT_info

    nvidia_parameters_path = "/proc/driver/nvidia/params"

    if not os.path.isfile(nvidia_parameters_path):
        print("ERROR : nvidia PAT : file %s does not exist" % nvidia_parameters_path)
        nvidia_PAT_info["error"] = True
        return nvidia_PAT_info

    with open(nvidia_parameters_path, "r") as f:
        params_text = f.read()

    for line in params_text.splitlines():

        if "UsePageAttributeTable" in line:

            line_stripped = line.strip().replace(" ", "")

            colon_index = line_stripped.find(":")

            if colon_index == -1 or colon_index == len(line_stripped) - 1:
                print("ERROR : nvidia PAT : cannot parse UsePageAttributeTable line : %s" % line.strip())
                nvidia_PAT_info["error"] = True
                return nvidia_PAT_info

            status_str = line_stripped[colon_index+1:]

            try:
                status_int = int(status_str)
            except ValueError:
                print("ERROR : nvidia PAT : UsePageAttributeTable has non-int value in line : %s" % line.strip())
                nvidia_PAT_info["error"] = True
                return nvidia_PAT_info

            if status_int not in [0, 1]:
                print("ERROR : nvidia PAT : UsePageAttributeTable value is not boolean in line : %s" % line.strip())
                nvidia_PAT_info["error"] = True
                return nvidia_PAT_info

            nvidia_PAT_info["enabled"] = (status_int == 1)
            return nvidia_PAT_info

    else:
        print("ERROR : nvidia PAT : Cannot find UsePageAttributeTable attribute")
        nvidia_PAT_info["error"] = True
        return nvidia_PAT_info


def _check_nvidia_module_active(system_info):

    if system_info["GPUs_PCI"]["error"]:
        return False

    gpus_pci_map = system_info["GPUs_PCI"]["pci_map"]

    for bus_id in gpus_pci_map.keys():
        if gpus_pci_map[bus_id]["active_module"] == "nvidia":
            return True
    else:
        return False


def _make_empty_nvidia_PAT_info():
    return {"error": False, "enabled": False}
