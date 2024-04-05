#!/usr/bin/python3
"""This module contains methods"""
from fabric.api import put, run, env
from os.path import exists
env.hosts = ["54.160.72.119", "54.90.17.67"]


def do_deploy(archive_path):
    """Moethod that distributes an archive to web servers"""
    if exists(archive_path) is False:
        return False
    try:
        file_name = archive_path.split("/")[-1]
        date_time = file_name.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, date_time))
        run('tar -xzf /tmp/{} -C {}{}'.format(file_name, path, date_time))
        run('rm /tmp/{}'.format(file_name))
        run('mv {0}{1}/web_static/* {0}{1}'.format(path, date_time))
        run('rm -rf {}{}/web_static/'.format(path, date_time))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, date_time))
        print("New version deployed!")
        return True
    except Exception:
        return False
