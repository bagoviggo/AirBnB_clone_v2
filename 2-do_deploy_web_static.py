#!/usr/bin/python3
"""
Fabric script to distribute an archive to your web servers
"""
from fabric.api import env, put, run
from os.path import exists
import os.path
import re


env.hosts = ['54.242.191.75', '100.26.212.141']


def do_deploy(archive_path):
    """
    Deploy the web static files
    """
    if not os.path.exists(archive_path):
        return False
    try:
        put(archive_path, "/tmp/")
        file_name = archive_path.split("/")[-1]
        folder_name = re.sub('.tgz$', '', file_name)
        run("sudo mkdir -p /data/web_static/releases/{}".format(folder_name))
        run("sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(file_name, folder_name))
        run("sudo rm /tmp/{}".format(file_name))
        run("sudo mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/".format(folder_name, folder_name))
        run("sudo rm -rf /data/web_static/releases/{}/web_static"
            .format(folder_name))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s /data/web_static/releases/{}/ "
            "/data/web_static/current".format(folder_name))
        return True
    except Exception as e:
        print("Error: {}".format(e))
        return False

