
def check_cpu_governor(system_info, checklist):

    cpu_governor_info = system_info["cpu_governor"]

    if cpu_governor_info["error"]:
        return

    if "performance" in cpu_governor_info["available_governors"] and \
        cpu_governor_info["current_governor"] != "performance":
        checklist.add_item("WARNING", "cpu_governor")

    else:
        checklist.add_item("OK", "cpu_governor")
