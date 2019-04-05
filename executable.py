from bash import exec_bash


def get_executables_availability(exec_names_list):

    available_executables = []
    for exec_name in exec_names_list:
        if is_executable_in_path(exec_name):
            available_executables.append(exec_name)

    return available_executables


def is_executable_in_path(exec_name):

    returncode, _, _ = exec_bash("which %s" % exec_name)

    return (returncode == 0)
