from ..utils.Checklist import Checklist
from .esync import check_esync
from .cpu import check_cpu_governor
from .nouveau import check_nouveau


def make_checklist(system_info):

    checklist = Checklist()

    check_esync(system_info, checklist)
    check_cpu_governor(system_info, checklist)
    check_nouveau(system_info, checklist)

    return checklist
