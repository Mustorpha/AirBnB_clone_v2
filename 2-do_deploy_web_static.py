#!/usr/bin/python3
"""
A function for deploying web_static content to web servers.
"""
import os
from datetime import datetime
from fabric.api import env, put, run
env.hosts = ['100.27.11.204', '3.85.41.254']
env.user = 'ubuntu'

def do_deploy(archive_path):
    """ Deploys archive to web servers """
    if not os.path.exists(archive_path):
        return False
    try:
        filename = os.path.basename(archive_path)
        web_static_folder = filename.split('.')[0]
        releases_path = '/data/web_static/releases/{}'.format(web_static_folder)
        tmp_path = '/tmp/{}'.format(filename)
        put(archive_path, tmp_path)
        run('mkdir -p {}'.format(releases_path))
        run('tar -xzf {} -C {}'.format(tmp_path, releases_path))
        run('rm {}'.format(tmp_path))
        run('mv {}/web_static/* {}'.format(releases_path, releases_path))
        run('rm -rf {}/web_static'.format(releases_path))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(releases_path))
        print('New version deployed!')
        return True
    except Exception as e:
        print('Error: {}'.format(e))
        return False
