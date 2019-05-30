
def check_amdgpu_radeon_conflict(system_info, checklist):

    gpus_pci_info = system_info["GPUs_PCI"]

    if gpus_pci_info["error"]:
        return

    for bus_id in gpus_pci_info["pci_map"].keys():

        if "amdgpu" in gpus_pci_info["pci_map"][bus_id]["available_modules"] and \
            gpus_pci_info["pci_map"][bus_id]["active_module"] == "radeon":

            checklist.add_item("CRITICAL", "amdgpu_vs_radeon")
            return
