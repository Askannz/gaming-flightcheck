from .libraries import is_library_installed


def get_libvulkan_info(system_info):
    return is_library_installed(system_info, "libvulkan")
