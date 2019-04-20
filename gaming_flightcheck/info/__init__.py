from .executables import get_executables_availability
from .distribution import get_distribution_info
from .pci import get_GPUs_PCI_info
from .opengl import get_opengl_info
from .cpu import get_cpu_governor_info
from .limits import get_limits_info
from .nvidia import get_nvidia_PAT_info
from .display import get_PRIME_sync_info
from .vulkan import get_vulkan_info
from ..distribution_specific.ArchlinuxContext import ArchlinuxContext
from ..distribution_specific.UbuntuContext import UbuntuContext


def get_system_info():

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

    return system_info
