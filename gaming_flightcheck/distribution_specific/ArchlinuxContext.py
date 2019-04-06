import re
from ..info.executables import is_executable_in_path
from ..utils.bash import exec_bash
from ._DistributionContext import _DistributionContext

ARCHLINUX_PACKAGES_LIST = ["nvidia", "nvidia-utils", "lib32-nvidia-utils",
                           "vulkan-icd-loader", "lib32-vulkan-icd-loader",
                           "mesa", "lib32-mesa",
                           "vulkan-radeon", "lib32-vulkan-radeon",
                           "vulkan-intel", "lib32-vulkan-intel"]


class ArchlinuxContext(_DistributionContext):

    def get_packages_info(self, system_info):

        packages_info = self._get_empty_packages_info()

        if not is_executable_in_path("pacman"):
            print("ERROR : \"pacman\" is not in PATH."
                  "Is the distribution not Archlinux ?")
            packages_info["error"] = True
            return packages_info

        for package in ARCHLINUX_PACKAGES_LIST:
            packages_info["packages_dict"][package] = self._get_single_package_info(package)

        return packages_info

    @staticmethod
    def _get_empty_packages_info():
        packages_info = {"error": False, "packages_dict": {}}
        for package in ARCHLINUX_PACKAGES_LIST:
            packages_info["packages_dict"][package] = ArchlinuxContext._get_empty_single_package_info()
        return packages_info

    @staticmethod
    def _get_empty_single_package_info():
        return {"error": False, "installed": False, "version": ""}

    @staticmethod
    def _get_single_package_info(package):

        single_package_info = ArchlinuxContext._get_empty_single_package_info()

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
