from pci import get_GPUs_PCI_info
from opengl import get_opengl_info
from cpu import get_cpu_governor_info
from limits import get_limits_info
from nvidia import get_PAT_usage_enabled
from display import get_PRIME_sync_info
from distribution_specific.ArchlinuxReader import ArchlinuxReader

GPUs_PCI_info = get_GPUs_PCI_info()

gpus_pci_map = GPUs_PCI_info["pci_map"]

for bus_id in gpus_pci_map.keys():

    print("%s %s (%s)" % (gpus_pci_map[bus_id]["vendor"], gpus_pci_map[bus_id]["name"], bus_id))
    print("\tAvailable modules: %s" % "/".join(gpus_pci_map[bus_id]["available_modules"]))
    print("\tModule in use: %s" % gpus_pci_map[bus_id]["active_module"])

opengl_info = get_opengl_info()

print("")
print("Renderer: %s" % opengl_info["renderer"])
print("Renderer version: %s" % opengl_info["renderer_version"])
print("OpenGL version: %s" % opengl_info["opengl_version"])

cpu_governor_info = get_cpu_governor_info()

print("")
print("Available CPU governors: %s" % "/".join(cpu_governor_info["available_governors"]))
print("Current CPU governor: %s" % cpu_governor_info["current_governor"])

limits_info = get_limits_info()

print("")
print("System file limit : %d" % limits_info["file_limit"])

distribution_reader = ArchlinuxReader()

print("")
checklist = []
system_info = {}
system_info, checklist = distribution_reader.check_nvidia_packages(system_info, checklist)
print(checklist)

nvidia_PAT_info = get_PAT_usage_enabled()

print("")
print("Page Attribute Table usage enabled : %s" % ("yes" if nvidia_PAT_info["enabled"] else "no"))

PRIME_sync_info = get_PRIME_sync_info()

print("")
print("PRIME Sync : supported on %d monitor(s), enabled on %d"
      % (PRIME_sync_info["nb_supported"], PRIME_sync_info["nb_enabled"]))
