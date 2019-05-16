import re
from ..utils.bash import exec_bash


def get_opengl_info(system_info):

    assert "available_executables" in system_info.keys()

    if not system_info["available_executables"]["lspci"]:
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

    opengl_version_key = "OpenGL version string:"

    string_index = line.find(opengl_version_key)

    if string_index != -1:

        found_version_string = True

        version_string = line[string_index+len(opengl_version_key):]
        version_string_items = version_string.split(" ")

        version_string_items = [it.replace(" ", "") for it in version_string_items]
        version_string_items = [it for it in version_string_items if it != ""]

        if len(version_string_items) != 3:
            _print_glxinfo_error("%d items in version string" % len(version_string_items))
            opengl_info["error"] = True
            return found_version_string, opengl_info

        opengl_version = version_string_items[0]
        if not re.fullmatch("[0-9\\.]+", opengl_version):
            _print_glxinfo_error("OpenGL version is \"%s\"" % opengl_version)
            opengl_info["error"] = True
            return found_version_string, opengl_info
        else:
            opengl_info["opengl_version"] = opengl_version

        provider = version_string_items[1]
        opengl_info["opengl_provider"] = provider

        provider_version = version_string_items[2]
        opengl_info["opengl_provider_version"] = provider_version

    return found_version_string, opengl_info


def _parse_opengl_renderer_string(opengl_info, line):

    found_renderer_string = False

    opengl_renderer_key = "OpenGL renderer string:"

    string_index = line.find(opengl_renderer_key)

    if string_index != -1:

        found_renderer_string = True

        renderer_string = line[string_index+len(opengl_renderer_key):]
        opengl_info["renderer"] = renderer_string

    return found_renderer_string, opengl_info


def _make_empty_opengl_info():
    return {"error": False, "opengl_version": "",
            "opengl_provider": "", "opengl_provider_version": "",
            "renderer": ""}


def _print_glxinfo_error(msg):
    print("ERROR : glxinfo parsing : %s" % msg)
