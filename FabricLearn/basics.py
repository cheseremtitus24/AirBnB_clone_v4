import datetime

from fabric.api import task

@task
def create_archive(c):
    archive_name = "web_static_{}.tgz".format(datetime.now().strftime('%Y%m%d%H%M%S'))
    c.local("tar -czvf {} folder_name".format(archive_name))
    return archive_name
