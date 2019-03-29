from pci import list_gpus
from opengl import get_opengl_info

gpus_pci_map = list_gpus()

for bus_id in gpus_pci_map.keys():

    print("%s %s (%s)" % (gpus_pci_map[bus_id]["vendor"], gpus_pci_map[bus_id]["name"], bus_id))
    print("\tAvailable modules: %s" % ",".join(gpus_pci_map[bus_id]["available_modules"]))
    print("\tModule in use: %s" % gpus_pci_map[bus_id]["active_module"])

opengl_info = get_opengl_info()

print("Renderer: %s" % opengl_info["renderer"])
print("Renderer version: %s" % opengl_info["renderer_version"])
print("OpenGL version: %s" % opengl_info["opengl_version"])
