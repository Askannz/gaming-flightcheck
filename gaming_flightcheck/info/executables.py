from .. import utils


def get_executables_availability(exec_names_list):

    executables_availability = {}

    for exec_name in exec_names_list:
        executables_availability[exec_name] = is_executable_in_path(exec_name)

    return executables_availability


def is_executable_in_path(exec_name):

    returncode, _, _ = utils.bash.exec_bash("which %s" % exec_name)

    return (returncode == 0)
