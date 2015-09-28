from __future__ import with_statement
from contextlib import contextmanager as _contextmanager
from fabric.api import *
from fabric.contrib.console import confirm

env.use_ssh_config = True
env.hosts = 'peterhenry'

env.directory = '/sites/projects/moviepicker'
env.activate = 'source /sites/virtualenvs/moviepicker/bin/activate'


@_contextmanager
def virtualenv():
    with cd(env.directory):
        with prefix(env.activate):
            yield


def pull():
    '''Pull the newest code from the repository.'''
    with cd(env.directory):
        run('git pull')


def install_requirements():
    '''Install the pip requirements listed in the reqs.txt file.'''
    with virtualenv():
        run('pip install -r reqs.txt')


def collect_static():
    '''Collect all static files and put in static root for Apache.'''
    with virtualenv():
        run('./manage.py collectstatic --noinput')


def restart_apache():
    '''Restart Apache daemon to begin serving changes to website.'''
    run('service apache2 restart')


def deploy():
    pull()
    install_requirements()
    collect_static()
    restart_apache()
