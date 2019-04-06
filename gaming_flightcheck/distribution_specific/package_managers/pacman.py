import re
from ...utils.bash import exec_bash


def get_single_package_info(package):

    single_package_info = get_empty_single_package_info()

    returncode, pacman_output, pacman_stderr = exec_bash("pacman -Qi %s" % package)

    if returncode != 0:

        if re.search("package .+ was not found", pacman_stderr):
            single_package_info["installed"] = False
            return single_package_info

        else:
            print("ERROR : error running \"pacman -Qi %s\": %s" % (package, pacman_stderr))
            single_package_info["error"] = True
            return single_package_info

    else:

        single_package_info["installed"] = True

        for line in pacman_output.splitlines():

            if "Version" in line:

                version_line_nospace = line.strip().replace(" ", "")
                colon_index = version_line_nospace.find(":")
                if colon_index == -1 or colon_index == len(version_line_nospace) - 1:
                    print("WARNING : pacman -Qi %s : cannot parse line %s" % (package, line))
                    continue
                else:
                    version_line_items = version_line_nospace.split(":")
                    version = version_line_items[1]

                    # Stripping package release version, if any
                    if re.search("-[0-9]+$", version):
                        version = "-".join(version.split("-")[:-1])

                    single_package_info["version"] = version

                    return single_package_info

        else:
            print("ERROR : pacman -Qi %s : package found but cannot parse version" % package)
            single_package_info["error"] = True
            return single_package_info


def get_empty_single_package_info():
    return {"error": False, "installed": False, "version": ""}
