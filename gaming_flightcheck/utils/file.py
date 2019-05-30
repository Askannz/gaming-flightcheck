import re
from .bash import exec_bash


def get_binary_file_arch(filepath):

    result = {"error": False, "arch": False}

    returncode, stdout, _ = exec_bash("objdump -f %s" % filepath)

    if returncode != 0:
        result["error"] = True
        return result

    for line in stdout.splitlines():

        line = line.strip()

        search_res = re.search("^architecture: ", line)

        if search_res:

            _, i = search_res.span()
            rest_of_line = line[i:]

            if re.search("^i386:x86-64", rest_of_line) or re.search("^x86-64", rest_of_line):
                result["arch"] = "64bit"
            elif re.search("^i386", rest_of_line):
                result["arch"] = "32bit"
            else:
                result["error"] = True

            return result
