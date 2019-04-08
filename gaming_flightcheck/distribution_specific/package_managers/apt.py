import re
from ...utils.bash import exec_bash


def get_i386_availability_info():

    i386_availability_info = get_empty_i386_availability_info()

    returncode, dpkg_output, stderr = exec_bash("dpkg --print-foreign-architectures")

    if returncode != 0:
        print("ERROR : error running \"dpkg --print-foreign-architectures\": %s" % stderr)
        i386_availability_info["error"] = True
        return i386_availability_info

    i386_availability_info["enabled"] = ("i386" in dpkg_output)

    return i386_availability_info


def get_info_matching_packages(package_name_pattern):

    package_list_info = {"error": False, "packages": {}}

    returncode, dpkg_output, stderr = exec_bash("dpkg -l")

    if returncode != 0:
        print("ERROR : error running \"dpkg -l\": %s" % stderr)
        package_list_info["error"] = True
        return package_list_info

    lines_list = list(dpkg_output.splitlines())

    if len(lines_list) < 6:
        print("ERROR : \"dpkg -l\" parsing : header is too short (%d lines)" % len(lines_list))
        package_list_info["error"] = True
        return package_list_info

    lines_list = lines_list[5:]

    for line in lines_list:

        error, package_fields = _parse_dpkg_line(line)

        if error:
            print("ERROR : \"dpkg -l\" : error parsing line : %s" % line)
            package_list_info["error"] = True
            return package_list_info

        installed, name, version, arch = package_fields

        if re.fullmatch(package_name_pattern, name) and installed:
            single_package_info = get_empty_single_package_info()
            single_package_info["version"] = version
            single_package_info["32bit"] = (arch == "all" or arch == "i386")
            single_package_info["64bit"] = (arch == "all" or arch == "amd64")
            package_list_info["packages"][name] = single_package_info

    else:
        return package_list_info


def get_empty_i386_availability_info():
    return {"error": False, "enabled": False}


def get_empty_single_package_info():
    return {"error": False, "version": "", "32bit": False, "64bit": False}


def _parse_dpkg_line(line):

    error = False

    line = line.strip()
    line = line.replace("\t", "")
    line_items = line.split(" ")
    line_items = [it for it in line_items if it != ""]

    if len(line_items) < 4:
        print("ERROR : \"dpkg -l\" : not enough items in line : %s" % line)
        error = True
        return error, None

    status_str, name, version, arch = line_items[:4]

    if len(status_str) != 2:
        print("ERROR : \"dpkg -l\" : unknown status string in line : %s" % line)
        error = True
        return error, None

    if arch not in ["amd64", "i386", "all"]:
        print("ERROR : \"dpkg -l\" : unknown arch in line : %s" % line)
        error = True
        return error, None

    installed = (status_str[1] == "i")

    package_fields = installed, name, version, arch

    return error, package_fields
