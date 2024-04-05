#!/usr/bin/python3
""" Creates and distributes an archive to your web servers """
from fabric.api import *
import os
from datetime import datetime


env.user = 'ubuntu'
env.hosts = ['52.86.133.238', '52.87.211.253']


def do_pack():
    """ Generates a .tgz archive """

    local("mkdir -p versions/")
    time = datetime.now().strftime("%Y%m%d%H%M%S")
    path = "versions/web_static_{}.tgz".format(time)
    res = local("tar -cvzf {} web_static".format(path))
    if res.failed:
        return None
    return path


def do_deploy(archive_path):
    """ Distributes an archive to your web servers """

    if not os.path.exists(archive_path):
        return False

    try:
        put(archive_path, '/tmp/')
        archive_path = archive_path.split('/')[1].strip('.tgz')
        path = "/data/web_static/releases/{}".format(archive_path)
        run('mkdir -p {}/'.format(path))
        run('tar -xzf /tmp/{}.tgz -C {}/'.format(archive_path, path))
        run('rm /tmp/{}.tgz'.format(archive_path))
        run('mv {}/web_static/* {}/'.format(path, path))
        run('rm -rf {}/web_static'.format(path))
        run('rm -rf /data/web_static/current')
        run('ln -s {}/ /data/web_static/current'.format(path))
        return True
    except Exception:
        return False


def deploy():
    """ Creates and distributes an archive to your web servers """

    path = do_pack()
    if path is None:
        return False
    return do_deploy(path)
