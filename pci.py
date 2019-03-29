import re
from bash import exec_bash


def list_gpus():

    gpus_pci_map = _get_gpus_pci_ids()
    gpus_pci_map = _add_gpu_names(gpus_pci_map)
    gpus_pci_map = _add_gpu_kernel_drivers(gpus_pci_map)

    return gpus_pci_map


def _get_gpus_pci_ids():

    VENDORS_ID_MAP = {"8086": "Intel", "1002": "AMD", "10de": "Nvidia"}

    _, lspci_output, _ = exec_bash("lspci -n")

    gpus_pci_map = {}

    for line in lspci_output.splitlines():

        line_items = line.split(" ")

        if len(line_items) < 3:
            _print_gpu_listing_warning("lspci -n : Unexpected line format : %s" % line)
            continue

        bus_id_str = line_items[0]
        class_str = line_items[1]
        vendor_product_id_str = line_items[2]

        if len(class_str) < 2:
            _print_gpu_listing_warning("lspci -n : Unexpected PCI class ID format : %s" % class_str)
            continue

        if class_str[:2] != "03":  # Not a GPU
            continue

        if not re.fullmatch("[a-f0-9]+:[a-f0-9]+", vendor_product_id_str):
            _print_gpu_listing_warning("lspci -n : Unexpected PCI vendor/product ID format : %s" % vendor_product_id_str)
            continue

        vendor_id_str, product_id_str = vendor_product_id_str.split(":")

        vendor_name = VENDORS_ID_MAP.get(vendor_id_str, "unknown")

        gpus_pci_map[bus_id_str] = {"vendor": vendor_name}

    return gpus_pci_map


def _add_gpu_names(gpus_pci_map):

    _, lspci_output, _ = exec_bash("lspci -m")

    for line in lspci_output.splitlines():

        #
        # Parsing PCI bus ID

        first_space_index = line.find(" ")

        if first_space_index == -1:
            _print_gpu_listing_warning("lspci -m : Unexpected line format : %s" % line)
            continue
        else:
            bus_id_str = line[:first_space_index]

        if bus_id_str not in gpus_pci_map.keys():
            continue

        #
        # Parsing GPU name

        quotes_indices = [i for i, c in enumerate(line) if c == "\""]

        if len(quotes_indices) < 6:
            _print_gpu_listing_warning("lspci -m : Unexpected line format : %s" % line)
            continue

        first_name_quote_index, second_name_quote_index = quotes_indices[4:6]
        gpu_name = line[first_name_quote_index+1:second_name_quote_index]

        gpus_pci_map[bus_id_str]["name"] = gpu_name

    for bus_id_str in gpus_pci_map.keys():
        if "name" not in gpus_pci_map[bus_id_str].keys():
            gpus_pci_map[bus_id_str]["name"] = "unknown"

    return gpus_pci_map


def _add_gpu_kernel_drivers(gpus_pci_map):

    _, lspci_output, _ = exec_bash("lspci -nk")

    current_bus_id_str = ""
    for i, line in enumerate(lspci_output.splitlines()):

        if len(line) == 0:
            continue

        line_items = line.split(" ")
        first_item = line_items[0].replace(" ", "")
        if re.fullmatch("[a-f0-9]{2}:[a-f0-9]{2}\\.[a-f0-9]", first_item):
            current_bus_id_str = first_item
        else:

            if current_bus_id_str not in gpus_pci_map.keys():
                continue

            kernel_modules_key = "Kernel modules:"
            kernel_modules_index = line.find(kernel_modules_key)
            if kernel_modules_index != -1 and kernel_modules_index != len(kernel_modules_key):
                kernel_modules_str = line[kernel_modules_index++len(kernel_modules_key):]
                kernel_modules = kernel_modules_str.replace(" ", "").split(",")
                if len(kernel_modules) > 0:
                    gpus_pci_map[current_bus_id_str]["available_modules"] = kernel_modules
                continue

            active_module_key = "Kernel driver in use:"
            active_module_index = line.find(active_module_key)
            if active_module_index != -1 and active_module_index != len(active_module_key):
                active_module_str = line[active_module_index+len(active_module_key):]
                active_module_str_items = active_module_str.replace(" ", "").split(",")
                if len(active_module_str_items) > 0:
                    gpus_pci_map[current_bus_id_str]["active_module"] = active_module_str_items[0]
                continue

    if current_bus_id_str == "":
        _print_gpu_listing_error("lspci -nk : Could not parse any bus IDs")

    for bus_id_str in gpus_pci_map.keys():
        if "available_modules" not in gpus_pci_map[bus_id_str].keys():
            gpus_pci_map[bus_id_str]["available_modules"] = []
        if "active_module" not in gpus_pci_map[bus_id_str].keys():
            gpus_pci_map[bus_id_str]["active_module"] = None

    return gpus_pci_map


def _print_gpu_listing_warning(msg):
    print("WARNING : GPU listing : %s" % msg)


def _print_gpu_listing_error(msg):
    print("ERROR : GPU listing : %s" % msg)
