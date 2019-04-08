from ..info.executables import is_executable_in_path
from ._DistributionContext import _DistributionContext
from .package_managers import apt

UBUNTU_PACKAGES_LIST = ["nvidia-driver-[0-9]+", "mesa-vulkan-drivers", "mesa-utils", "libvulkan1", "vulkan-utils"]


class UbuntuContext(_DistributionContext):

    def get_packages_info(self, system_info):

        packages_info = self._get_empty_packages_info()

        if not is_executable_in_path("dpkg"):
            print("ERROR : \"dpkg\" is not in PATH. "
                  "Is the distribution not Ubuntu ?")
            packages_info["error"] = True
            return packages_info

        packages_info["i386_arch"] = apt.get_i386_availability_info()

        for package_name_pattern in UBUNTU_PACKAGES_LIST:
            packages_info["packages_dict"][package_name_pattern] = apt.get_info_matching_packages(package_name_pattern)

        return packages_info

    @staticmethod
    def _get_empty_packages_info():
        packages_info = {"error": False, "packages_dict": {}}
        packages_info["i386_arch"] = apt.get_empty_i386_availability_info()

        for package in UBUNTU_PACKAGES_LIST:
            packages_info["packages_dict"][package] = []

        return packages_info
