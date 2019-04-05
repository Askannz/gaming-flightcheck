import re
from bash import exec_bash


def get_opengl_info(system_info):

    assert "available_executables" in system_info.keys()

    if "lspci" not in system_info["available_executables"]:
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

    opengl_version_key = "OpenGL version string:"

    for line in glxinfo_output.splitlines():

        string_index = line.find(opengl_version_key)

        if string_index != -1:

            version_string = line[string_index+len(opengl_version_key):]
            version_string_items = version_string.split(" ")

            version_string_items = [it.replace(" ", "") for it in version_string_items]
            version_string_items = [it for it in version_string_items if it != ""]

            if len(version_string_items) != 3:
                _print_glxinfo_error("%d items in version string" % len(version_string_items))
                opengl_info["error"] = True
                return opengl_info

            opengl_version = version_string_items[0]
            if not re.fullmatch("[0-9\\.]+", opengl_version):
                _print_glxinfo_error("OpenGL version is \"%s\"" % opengl_version)
                opengl_info["error"] = True
                return opengl_info
            else:
                opengl_info["opengl_version"] = opengl_version

            renderer = version_string_items[1]
            opengl_info["renderer"] = renderer

            renderer_version = version_string_items[2]
            opengl_info["renderer_version"] = renderer_version

            return opengl_info

    else:
        _print_glxinfo_error("OpenGL version string not found")
        opengl_info["error"] = True
        return opengl_info


def _make_empty_opengl_info():
    return {"error": False, "opengl_version": "",
            "renderer": "", "renderer_version": ""}


def _print_glxinfo_error(msg):
    print("ERROR : glxinfo parsing : %s" % msg)
