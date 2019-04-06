import os
from ..utils.bash import exec_bash
from .libraries import is_library_installed


def get_vulkan_info(system_info):

    vulkan_info = {}

    vulkan_info["libvulkan"] = _get_libvulkan_info(system_info)
    vulkan_info["ICDs"] = _get_ICDs_info(system_info)
    vulkan_info["vulkaninfo_status"] = _get_vulkaninfo_status_info(system_info)

    return vulkan_info


def _get_libvulkan_info(system_info):
    return is_library_installed(system_info, "libvulkan")


def _get_ICDs_info(system_info):

    ICDs_info = {"error": False, "files_list": []}

    ICDs_folder_path = "/usr/share/vulkan/icd.d/"

    if not os.path.isdir(ICDs_folder_path):
        return ICDs_info

    ICDs_info["files_list"] = list(os.listdir(ICDs_folder_path))

    return ICDs_info


def _get_vulkaninfo_status_info(system_info):

    assert "available_executables" in system_info.keys()

    vulkaninfo_status_info = {"error": False, "status_ok": False}

    if "vulkaninfo" not in system_info["available_executables"]:
        vulkaninfo_status_info["error"] = True
        return vulkaninfo_status_info

    returncode, _, _ = exec_bash("vulkaninfo")

    vulkaninfo_status_info["status_ok"] = (returncode == 0)

    return vulkaninfo_status_info
