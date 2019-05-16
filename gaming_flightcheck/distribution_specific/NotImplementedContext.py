from ._DistributionContext import _DistributionContext


class NotImplementedContext(_DistributionContext):

    def get_packages_info(self, system_info):

        packages_info = self._get_empty_packages_info()

        return packages_info

    @staticmethod
    def _get_empty_packages_info():
        packages_info = {"error": False}
        return packages_info
