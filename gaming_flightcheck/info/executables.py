import os
from .. import utils


def get_executables_paths(exec_names_list):

    paths = {}

    for exec_name in exec_names_list:

        exec_path = get_executable_path_from_PATH(exec_name)

        if exec_path is None:
            exec_path = get_executable_path_in_sbin(exec_name)

        paths[exec_name] = exec_path

    return paths


def get_executable_path_from_PATH(exec_name):

    returncode, stdout, _ = utils.bash.exec_bash("which %s" % exec_name)

    if returncode != 0:
        return stdout.strip()
    else:
        return None


def get_executable_path_in_sbin(exec_name):

    sbin_exec_path = os.path.join("/", "sbin", exec_name)

    if os.path.isfile(sbin_exec_path):
        return sbin_exec_path
    else:
        return None
