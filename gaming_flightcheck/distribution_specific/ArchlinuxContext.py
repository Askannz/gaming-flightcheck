import itertools
import re
from ..utils.bash import exec_bash
from ._DistributionContext import _DistributionContext


class ArchlinuxContext(_DistributionContext):

    def check_nvidia_packages(self, system_info, checklist):

        packages_info = {}

        for package in ["nvidia", "nvidia-utils", "lib32-nvidia-utils"]:

            error, installed, version = self._check_package_installed(package)
            packages_info[package] = {}
            packages_info[package]["error"] = error
            packages_info[package]["installed"] = installed
            packages_info[package]["version"] = version

        for package in ["nvidia", "nvidia-utils", "lib32-nvidia-utils"]:
            if packages_info[package]["error"]:
                checklist.append(("critical", "Error parsing Nvidia packages information"))
                return system_info, checklist

        for package in ["nvidia", "nvidia-utils", "lib32-nvidia-utils"]:
            if not packages_info[package]["installed"]:
                checklist.append(("critical", "Package %s is not installed" % package))
            else:
                checklist.append(("ok", "Package %s is installed" % package))

        for p_1, p_2 in itertools.combinations(["nvidia", "nvidia-utils", "lib32-nvidia-utils"], 2):
            if packages_info[p_1]["installed"] and packages_info[p_2]["installed"] and \
               packages_info[p_1]["version"] != packages_info[p_2]["version"]:
                checklist.append(("critical", "Version mismatch between %s (%s) and %s (%s)"
                                  % (p_1, packages_info[p_1]["version"],
                                     p_2, packages_info[p_2]["version"])))

        return system_info, checklist

    @staticmethod
    def _check_package_installed(package):

        error = False
        package_installed = False
        package_version = ""

        if not ArchlinuxContext._check_package_manager():
            print("ERROR : cannot query package manager \"pacman\". "
                  "Is the distribution not Archlinux ?")
            error = True
            return error, package_installed, package_version

        else:

            returncode, pacman_output, pacman_stderr = exec_bash("pacman -Qi %s" % package)

            if returncode != 0:

                if re.search("package .+ was not found", pacman_stderr):
                    package_installed = False
                    return error, package_installed, package_version

                else:
                    print("ERROR : error querying pacman -Qi %s : %s" % (package, pacman_stderr))
                    error = True
                    return error, package_installed, package_version

            else:

                package_installed = True

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

                            # Stripping package release
                            if re.search("-[0-9]+$", version):
                                version = "-".join(version.split("-")[:-1])

                            package_version = version

                            return error, package_installed, package_version

                else:
                    print("ERROR : pacman -Qi %s : package found but cannot parse version" % package)
                    error = True
                    return error, package_installed, package_version

    def _check_package_manager():
        returncode, _, _ = exec_bash("which pacman")
        return (returncode == 0)
