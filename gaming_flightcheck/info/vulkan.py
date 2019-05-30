import os
import re
from ..utils.bash import exec_bash
from .libraries import is_library_installed


RELEVANT_EXTENSIONS_LIST = ["VK_EXT_transform_feedback"]


def get_vulkan_info(system_info):

    vulkan_info = {}

    vulkan_info["libvulkan"] = _get_libvulkan_info(system_info)
    vulkan_info["ICDs"] = _get_ICDs_info(system_info)
    vulkan_info["extensions"] = _get_extensions_info(system_info, vulkan_info["ICDs"])

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


def _get_extensions_info(system_info, ICDs_info):

    assert "executables_paths" in system_info.keys()

    extensions_info = _get_emtpy_extensions_info()

    if not system_info["executables_paths"]["vulkaninfo"] or ICDs_info["error"]:
        extensions_info["error"] = True
        return extensions_info

    for ICD_filename in ICDs_info["files_list"]:

        if "i686" in ICD_filename:
            continue  # vulkaninfo does not work with 32-bit ICDs

        extensions_info["by_ICD"][ICD_filename] = _get_empty_ICD_extensions_info()

        returncode, vulkaninfo_output, stderr = exec_bash("VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/%s %s"
                                                          % (ICD_filename, system_info["executables_paths"]["vulkaninfo"]))

        if returncode != 0:
            _print_vulkaninfo_warning("error running vulkaninfo with ICD %s : %s" % (ICD_filename, stderr))
            extensions_info["by_ICD"][ICD_filename]["error"] = True
            continue

        error, supported_extensions_list = _parse_vulkaninfo(vulkaninfo_output)

        if error:
            _print_vulkaninfo_warning("error parsing vulkaninfo with ICD %s" % ICD_filename)
            extensions_info["by_ICD"][ICD_filename]["error"] = True
            continue

        for extension_name in RELEVANT_EXTENSIONS_LIST:
            extensions_info["by_ICD"][ICD_filename]["extensions"][extension_name] = \
                (extension_name in supported_extensions_list)

    return extensions_info


def _parse_vulkaninfo(vulkaninfo_output):

    error = False
    supported_extensions_list = []
    found_extensions_section = False

    for line in vulkaninfo_output.splitlines():

        line = line.strip()

        if not found_extensions_section:
            if re.fullmatch("^Device Extensions.+$", line):
                found_extensions_section = True
            continue

        else:
            for extension_name in RELEVANT_EXTENSIONS_LIST:
                if extension_name in line:
                    supported_extensions_list.append(extension_name)

    if not found_extensions_section:
        error = True

    return error, supported_extensions_list


def _get_emtpy_extensions_info():
    return {"error": True, "by_ICD": {}}


def _get_empty_ICD_extensions_info():
    ICD_extensions_info = {"error": False, "extensions": {}}
    for extension_name in RELEVANT_EXTENSIONS_LIST:
        ICD_extensions_info[extension_name] = False
    return ICD_extensions_info


def _print_vulkaninfo_warning(msg):
    print("WARNING: vulkaninfo : %s" % msg)
