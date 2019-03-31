from pci import list_gpus
from opengl import get_opengl_info
from cpu import get_cpu_governor_info
from limits import get_limits_info
from distribution_specific.ArchlinuxReader import ArchlinuxReader

gpus_pci_map = list_gpus()

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
