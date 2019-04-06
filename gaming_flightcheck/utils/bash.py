import subprocess


def exec_bash(command):

    ret = subprocess.run(["bash", "-c", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = ret.stdout.decode('utf-8')[:-1], ret.stderr.decode('utf-8')[:-1]
    returncode = ret.returncode

    return returncode, stdout, stderr
