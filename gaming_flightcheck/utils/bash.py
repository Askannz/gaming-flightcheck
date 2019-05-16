import subprocess


def exec_bash(command):

    ret = subprocess.run(["bash", "-c", "LC_ALL=C %s" % command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = ret.stdout.decode('utf-8')[:-1], ret.stderr.decode('utf-8')[:-1]
    returncode = ret.returncode

    return returncode, stdout, stderr
