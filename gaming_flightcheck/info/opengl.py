import re
from ..utils.bash import exec_bash


def get_opengl_info(system_info):

    assert "available_executables" in system_info.keys()

    if not system_info["executables_paths"]["glxinfo"]:
        opengl_info = _make_empty_opengl_info()
        opengl_info["error"] = True
        return opengl_info

    opengl_info = parse_glxinfo_opengl()

    return opengl_info


def parse_glxinfo_opengl():

    opengl_info = _make_empty_opengl_info()

    returncode, glxinfo_output, stderr = exec_bash("glxinfo")

    if returncode != 0:
        _print_glxinfo_error("glxinfo returned an error : %s" % stderr)
        opengl_info["error"] = True
        return opengl_info

    found_version_string = False
    found_renderer_string = False

    for line in glxinfo_output.splitlines():

        if not found_version_string:
            found_version_string, opengl_info = _parse_opengl_version_string(opengl_info, line)
        if not found_renderer_string:
            found_renderer_string, opengl_info = _parse_opengl_renderer_string(opengl_info, line)

        if opengl_info["error"] or (found_version_string and found_renderer_string):
            return opengl_info

    else:

        if not found_version_string:
            _print_glxinfo_error("OpenGL version string not found")
        if not found_renderer_string:
            _print_glxinfo_error("OpenGL renderer string not found")

        opengl_info["error"] = True
        return opengl_info


def _parse_opengl_version_string(opengl_info, line):

    found_version_string = False

    opengl_version_key = "OpenGL version string: "

    string_index = line.find(opengl_version_key)

    if string_index != -1 and string_index != len(line) - 1:

        found_version_string = True

        version_string = line[string_index+len(opengl_version_key):]

        first_space_index = version_string.find(" ")

        if first_space_index == -1 or first_space_index == len(version_string) - 1:
            _print_glxinfo_error("no vendor-specific string in OpenGL version : %s" % version_string)
            opengl_info["error"] = True
            return found_version_string, opengl_info

        opengl_version = version_string[:first_space_index]

        if not re.fullmatch("[0-9\\.]+", opengl_version):
            print(version_string)
            _print_glxinfo_error("OpenGL version is \"%s\"" % opengl_version)
            opengl_info["error"] = True
            return found_version_string, opengl_info
        else:
            opengl_info["opengl_version"] = opengl_version

        opengl_info["opengl_vendor_version"] = version_string[first_space_index+1:]

    return found_version_string, opengl_info


def _parse_opengl_renderer_string(opengl_info, line):

    found_renderer_string = False

    opengl_renderer_key = "OpenGL renderer string: "

    string_index = line.find(opengl_renderer_key)

    if string_index != -1 and string_index != len(line) - 1:

        found_renderer_string = True

        renderer_string = line[string_index+len(opengl_renderer_key):]
        opengl_info["renderer"] = renderer_string

    return found_renderer_string, opengl_info


def _make_empty_opengl_info():
    return {"error": False, "opengl_version": "",
            "opengl_vendor_version": "",
            "renderer": ""}


def _print_glxinfo_error(msg):
    print("ERROR : glxinfo parsing : %s" % msg)
