
def check_nouveau(system_info, checklist):

    opengl_info = system_info["opengl"]

    if opengl_info["error"]:
        return

    if opengl_info["vendor"] == "nouveau":
        checklist.add_item("CRITICAL", "nouveau")
