from .ArchlinuxContext import ArchlinuxContext
from .UbuntuContext import UbuntuContext
from .NotImplementedContext import NotImplementedContext


def get_distribution_context(system_info):

    assert "distribution" in system_info.keys()

    if system_info["distribution"]["error"]:
        return NotImplementedContext()

    if system_info["distribution"]["name"] == "archlinux":
        return ArchlinuxContext()

    elif system_info["distribution"]["name"] == "ubuntu":
        return UbuntuContext()

    else:
        return NotImplementedContext()
