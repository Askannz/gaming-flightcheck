from ..utils.Checklist import Checklist
from .esync import check_esync


def make_checklist(system_info):

    checklist = Checklist()

    check_esync(system_info, checklist)

    return checklist
