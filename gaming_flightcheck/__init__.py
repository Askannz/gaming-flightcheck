from .info.executables import get_executables_availability
from .info.pci import get_GPUs_PCI_info
from .info.opengl import get_opengl_info
from .info.cpu import get_cpu_governor_info
from .info.limits import get_limits_info
from .info.nvidia import get_nvidia_PAT_info
from .info.display import get_PRIME_sync_info
from .info.vulkan import get_vulkan_info
from .distribution_specific.ArchlinuxReader import ArchlinuxReader


def print_system_info():

    system_info = {}
    checklist = []

    distribution_reader = ArchlinuxReader()
    system_info, checklist = distribution_reader.check_nvidia_packages(system_info, checklist)

    system_info["available_executables"] = \
        get_executables_availability(["ldconfig", "lspci", "glxinfo", "xrandr", "vulkaninfo"])
    system_info["GPUs_PCI"] = get_GPUs_PCI_info(system_info)
    system_info["opengl"] = get_opengl_info(system_info)
    system_info["cpu_governor"] = get_cpu_governor_info(system_info)
    system_info["limits"] = get_limits_info(system_info)
    system_info["nvidia_PAT"] = get_nvidia_PAT_info(system_info)
    system_info["PRIME_sync"] = get_PRIME_sync_info(system_info)
    system_info["vulkan"] = get_vulkan_info(system_info)

    gpus_pci_map = system_info["GPUs_PCI"]["pci_map"]

    for bus_id in gpus_pci_map.keys():

        print("%s %s (%s)" % (gpus_pci_map[bus_id]["vendor"], gpus_pci_map[bus_id]["name"], bus_id))
        print("\tAvailable modules: %s" % "/".join(gpus_pci_map[bus_id]["available_modules"]))
        print("\tModule in use: %s" % gpus_pci_map[bus_id]["active_module"])

    opengl_info = system_info["opengl"]

    print("")
    print("OpenGL :")
    print("\tRenderer: %s" % opengl_info["renderer"])
    print("\tOpenGL provider: %s" % opengl_info["opengl_provider"])
    print("\tOpenGL provider version: %s" % opengl_info["opengl_provider_version"])
    print("\tOpenGL version: %s" % opengl_info["opengl_version"])

    cpu_governor_info = system_info["cpu_governor"]

    print("")
    print("Available CPU governors: %s" % "/".join(cpu_governor_info["available_governors"]))
    print("Current CPU governor: %s" % cpu_governor_info["current_governor"])

    limits_info = system_info["limits"]

    print("")
    print("System file limit : %d" % limits_info["file_limit"])

    print("")
    print(checklist)

    nvidia_PAT_info = system_info["nvidia_PAT"]

    print("")
    print("Nvidia Page Attribute Table usage enabled : %s" % ("yes" if nvidia_PAT_info["enabled"] else "no"))

    PRIME_sync_info = system_info["PRIME_sync"]

    print("")
    print("PRIME Sync : supported on %d monitor(s), enabled on %d"
          % (PRIME_sync_info["nb_supported"], PRIME_sync_info["nb_enabled"]))

    print("")
    print("Vulkan :")

    libvulkan_info = system_info["vulkan"]["libvulkan"]
    print("\tlibvulkan installed :\n"
          "\t\t32-bit : %s\n"
          "\t\t64-bit : %s"
          % (("yes" if libvulkan_info["32bit"] else "no"),
             ("yes" if libvulkan_info["64bit"] else "no")))

    ICDs_info = system_info["vulkan"]["ICDs"]
    print("\tAvailable ICDs :")
    for file_name in ICDs_info["files_list"]:
        print("\t\t%s" % file_name)

    vulkaninfo_status_info = system_info["vulkan"]["vulkaninfo_status"]
    print("\tvulkaninfo error : %s" % ("no" if vulkaninfo_status_info["status_ok"] else "yes"))
