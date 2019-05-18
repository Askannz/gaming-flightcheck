#!/usr/bin/env python3
import sys
import os
from gaming_flightcheck.info import get_system_info
from gaming_flightcheck.analysis import make_checklist


def main():

    if os.geteuid() == 0:
        print("You should not run this script as root ! Exiting.")
        sys.exit(1)

    system_info = get_system_info()
    checklist = make_checklist(system_info)

    for item_level, item_title in checklist.get_checklist_items_data():
        print("[%s] %s" % (item_level, item_title))


if __name__ == "__main__":
    main()
