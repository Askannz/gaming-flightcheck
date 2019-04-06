from ..info.executables import is_executable_in_path
from ._DistributionContext import _DistributionContext
from .package_managers import pacman

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
            packages_info["packages_dict"][package] = pacman.get_single_package_info(package)

        return packages_info

    @staticmethod
    def _get_empty_packages_info():
        packages_info = {"error": False, "packages_dict": {}}
        for package in ARCHLINUX_PACKAGES_LIST:
            packages_info["packages_dict"][package] = pacman.get_empty_single_package_info()
        return packages_info
