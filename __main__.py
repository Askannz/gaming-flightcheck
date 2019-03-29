from pci import list_gpus

gpus_pci_map = list_gpus()

for bus_id in gpus_pci_map.keys():

    print("%s %s (%s)" % (gpus_pci_map[bus_id]["vendor"], gpus_pci_map[bus_id]["name"], bus_id))
    print("\tAvailable modules: %s" % ",".join(gpus_pci_map[bus_id]["available_modules"]))
    print("\tModule in use: %s" % gpus_pci_map[bus_id]["active_module"])
