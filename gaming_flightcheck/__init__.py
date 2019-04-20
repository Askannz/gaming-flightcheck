from .info.executables import get_executables_availability
from .info.distribution import get_distribution_info
from .info.pci import get_GPUs_PCI_info
from .info.opengl import get_opengl_info
from .info.cpu import get_cpu_governor_info
from .info.limits import get_limits_info
from .info.nvidia import get_nvidia_PAT_info
from .info.display import get_PRIME_sync_info
from .info.vulkan import get_vulkan_info
from .distribution_specific.ArchlinuxContext import ArchlinuxContext
from .distribution_specific.UbuntuContext import UbuntuContext


def print_system_info():

    system_info = {}

    system_info["available_executables"] = \
        get_executables_availability(["lsb_release", "hostnamectl", "ldconfig", "lspci", "glxinfo", "xrandr", "vulkaninfo"])
    system_info["distribution"] = get_distribution_info(system_info)
    system_info["GPUs_PCI"] = get_GPUs_PCI_info(system_info)
    system_info["opengl"] = get_opengl_info(system_info)
    system_info["cpu_governor"] = get_cpu_governor_info(system_info)
    system_info["limits"] = get_limits_info(system_info)
    system_info["nvidia_PAT"] = get_nvidia_PAT_info(system_info)
    system_info["PRIME_sync"] = get_PRIME_sync_info(system_info)
    system_info["vulkan"] = get_vulkan_info(system_info)

    if system_info["distribution"]["name"] == "archlinux":
        distribution_context = ArchlinuxContext()
    elif system_info["distribution"]["name"] == "ubuntu":
        distribution_context = UbuntuContext()

    system_info["distribution_specific"] = {}
    system_info["distribution_specific"]["packages"] = distribution_context.get_packages_info(system_info)

    distribution_info = system_info["distribution"]

    print("")
    print("Distribution : %s" % distribution_info["name"].capitalize())

    gpus_pci_map = system_info["GPUs_PCI"]["pci_map"]

    print("")
    print("GPU list :")

    for bus_id in gpus_pci_map.keys():

        print("\t%s %s (%s)" % (gpus_pci_map[bus_id]["vendor"], gpus_pci_map[bus_id]["name"], bus_id))
        print("\t\tAvailable modules: %s" % "/".join(gpus_pci_map[bus_id]["available_modules"]))
        print("\t\tModule in use: %s" % gpus_pci_map[bus_id]["active_module"])

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
    print("\tlibvulkan present :\n"
          "\t\t32-bit : %s\n"
          "\t\t64-bit : %s"
          % (("yes" if libvulkan_info["32bit"] else "no"),
             ("yes" if libvulkan_info["64bit"] else "no")))

    ICDs_info = system_info["vulkan"]["ICDs"]
    print("\tAvailable ICDs :")
    for ICD_filename in ICDs_info["files_list"]:
        print("\t\t%s" % ICD_filename)

    extensions_info = system_info["vulkan"]["extensions"]
    print("\tExtensions :")
    for ICD_filename in extensions_info["by_ICD"].keys():
        print("\t\t%s :" % ICD_filename)
        extensions_dict = extensions_info["by_ICD"][ICD_filename]["extensions"]
        for extension_name in extensions_dict.keys():
            print("\t\t\t%s : %s" % (extension_name, "yes" if extensions_dict[extension_name] else "no"))

    packages_info = system_info["distribution_specific"]["packages"]

    if system_info["distribution"]["name"] == "archlinux":

        print("")
        print("Archlinux packages :")

        print("\tMultilib repository enabled : %s"
              % ("yes" if packages_info["multilib"]["enabled"] else "no"))

        print("\tInstalled :")
        for package in packages_info["packages_dict"].keys():
            single_package_info = packages_info["packages_dict"][package]
            if single_package_info["installed"]:
                print("\t\t%s (%s)" % (package, single_package_info["version"]))

        print("\tNot installed :")
        for package in packages_info["packages_dict"].keys():
            single_package_info = packages_info["packages_dict"][package]
            if not single_package_info["installed"]:
                print("\t\t%s" % package)

    elif system_info["distribution"]["name"] == "ubuntu":

        print("")
        print("Ubuntu packages :")

        print("\ti386 architecture enabled : %s"
              % ("yes" if packages_info["i386_arch"]["enabled"] else "no"))

        print("\tInstalled :")
        for package_name_pattern in packages_info["packages_dict"].keys():

            if len(packages_info["packages_dict"][package_name_pattern]["packages"]) == 0:
                continue

            for package_name in packages_info["packages_dict"][package_name_pattern]["packages"].keys():

                single_package_info = \
                    packages_info["packages_dict"][package_name_pattern]["packages"][package_name]

                print("\t\t%s (%s, 32bit : %s, 64bit : %s)"
                      % (package_name, single_package_info["version"],
                         "yes" if single_package_info["32bit"] else "no",
                         "yes" if single_package_info["64bit"] else "no"))

        print("\tNot installed :")
        for package_name_pattern in packages_info["packages_dict"].keys():
            if len(packages_info["packages_dict"][package_name_pattern]["packages"]) == 0:
                print("\t\t%s" % package_name_pattern)
