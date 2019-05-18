
MINIMUM_FILE_LIMIT = 524288


def check_esync(system_info, checklist):

    if system_info["limits"]["error"]:
        return

    if system_info["limits"]["file_limit"] < MINIMUM_FILE_LIMIT:
        checklist.add_item("WARNING", "esync_file_limit")

    else:
        checklist.add_item("OK", "esync_file_limit")
