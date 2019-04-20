import re
from ..utils.bash import exec_bash


def is_library_installed(system_info, lib_name):

    assert "available_executables" in system_info.keys()

    if not system_info["available_executables"]["ldconfig"]:
        library_info = _make_empty_library_info()
        library_info["error"] = True
        return library_info

    library_info = parse_ldconfig(lib_name)

    return library_info


def parse_ldconfig(lib_name):

    library_info = _make_empty_library_info()

    returncode, ldconfig_output, stderr = exec_bash("ldconfig -p")

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
                library_info["64bit"] = True
            else:
                library_info["32bit"] = True

            # No point in continuing the parsing, so we break the loop
            if library_info["64bit"] and library_info["32bit"]:
                break

    return library_info


def _make_empty_library_info():
    return {"error": False, "32bit": False, "64bit": False}


def _print_ldconfig_error(lib_name, msg):
    print("ERROR : ldconfig parsing for \"%s\" : %s" % (lib_name, msg))


def _print_ldconfig_warning(lib_name, msg):
    print("WARNING : ldconfig parsing for \"%s\" : %s" % (lib_name, msg))
