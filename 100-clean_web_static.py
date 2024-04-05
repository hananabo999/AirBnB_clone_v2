#!/usr/bin/python3
"""This module contains methods"""
from fabric.api import *
import os

env.hosts = ["54.160.72.119", "54.90.17.67"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/school"

def do_clean(number=0):
    """Method that deletes out-of-date archives"""
    number = 1 if int(number) == 0 else int(number)

    # Cleaning local archives
    local_archives = sorted(os.listdir("versions"))
    for i in range(number):
        local_archives.pop()

    with lcd("versions"):
        for archive in local_archives:
            local("rm ./{}".format(archive))

    # Cleaning remote archives
    with cd("/data/web_static/releases"):
        remote_archives = run("ls -tr").split()
        remote_archives = [a for a in remote_archives if "web_static_" in a]
        for i in range(number):
            remote_archives.pop()

        for archive in remote_archives:
            run("rm -rf ./{}".format(archive))
