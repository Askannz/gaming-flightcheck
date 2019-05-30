from ..utils.Checklist import Checklist
from .esync import check_esync
from .cpu import check_cpu_governor
from .nouveau import check_nouveau
from .amd import check_amdgpu_radeon_conflict


def make_checklist(system_info):

    checklist = Checklist()

    check_esync(system_info, checklist)
    check_cpu_governor(system_info, checklist)
    check_nouveau(system_info, checklist)
    check_amdgpu_radeon_conflict(system_info, checklist)

    return checklist
