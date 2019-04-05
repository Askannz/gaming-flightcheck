from bash import exec_bash


def is_executable_in_path(executable_name):

    returncode, _, _ = exec_bash("which %s" % executable_name)

    return (returncode == 0)
