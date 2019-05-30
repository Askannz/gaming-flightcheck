import re
from ..utils.bash import exec_bash


def get_library_info(system_info, lib_name):

    assert "executables_paths" in system_info.keys()

    if not system_info["executables_paths"]["ldconfig"]:
        library_info = _make_empty_library_info()
        library_info["error"] = True
        return library_info

    library_info = parse_ldconfig(system_info, lib_name)

    return library_info


def parse_ldconfig(system_info, lib_name):

    library_info = _make_empty_library_info()

    returncode, ldconfig_output, stderr = exec_bash("%s -p" % system_info["executables_paths"]["ldconfig"])

    if returncode != 0:
        _print_ldconfig_error(lib_name, "ldconfig returned an error : %s" % stderr)
        library_info["error"] = True
        return library_info
    for line in ldconfig_output.splitlines():

        line = line.strip()

        lib_name_search_res = re.search("^[\t ]*%s\\.so(\\.[0-9]+)*[\t ]+" % lib_name, line)

        if lib_name_search_res:

            i1, i2 = lib_name_search_res.span()
            line_no_lib_name = line[i2:]

            parentheses_search_res = re.search("^[\t ]*\\(.+\\)", line_no_lib_name)

            if not parentheses_search_res:
                _print_ldconfig_warning(lib_name, "cannot parse arch : %s" % line)
                continue

            parentheses_text = parentheses_search_res.string

            if "x86-64" in parentheses_text:
                arch = "64bit"
            else:
                arch = "32bit"

            _, i2 = parentheses_search_res.span()
            rest_of_line = line_no_lib_name[i2:]
            path_search_res = re.search("/[^ ]+$", rest_of_line)

            if not path_search_res:
                _print_ldconfig_warning(lib_name, "cannot parse library path : %s" % line)
                continue

            library_info[arch]["present"] = True
            library_info[arch]["path"] = path_search_res.string

            # No point in continuing the parsing, so we break the loop
            if library_info["64bit"]["present"] and library_info["32bit"]["present"]:
                break

    return library_info


def _make_empty_library_info():
    return {"error": False, "32bit": {"present": False, "path": ""}, "64bit": {"present": False, "path": ""}}


def _print_ldconfig_error(lib_name, msg):
    print("ERROR : ldconfig parsing for \"%s\" : %s" % (lib_name, msg))


def _print_ldconfig_warning(lib_name, msg):
    print("WARNING : ldconfig parsing for \"%s\" : %s" % (lib_name, msg))
