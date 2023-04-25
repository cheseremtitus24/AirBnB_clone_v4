#!/usr/bin/python3
"""
This module makes use of fabric version 1.14.2
and automates the creation of archive files
on a remote host
"""

# Import Fabric's API module
from datetime import datetime
import os
import platform

from fabric.api import task, run, env
from fabric.operations import local, put

# env.hosts = [
    # '108999f0b0e4.a73c91be.alx-cod.online',
    # '54.210.108.11',
    # '54.158.179.90'
    # 'web-02.eldoret.tech',
# ]
# Set the username
# env.user = "108999f0b0e4"
# Set the password [NOT RECOMMENDED]
# env.password = "785b0035e30507820c46"


# env.hosts = ['localhost']
# env.host="108999f0b0e4.a73c91be.alx-cod.online"


@task
def do_deploy(archive_path):
    """
    deploys a web project to a remote server's
    root page
    """
    # Verify that versions directory exists and deploy the latest Version
    # Returns False if the file at the path archive_path doesn’t exist
    retval = False
    if not local_file_exists(file_to_check=archive_path):
        # file not found - return false
        retval = False
    # Upload the archive to the /tmp/ directory of the web server
    remote_path = "/tmp"
    separator = platform.system()
    if separator == 'Linux' or separator == 'Darwin':
        separator = '/'
    else:
        separator = '\\'
    uploaded_file_name = archive_path.split(separator)[-1]
    upload_success = upload_file_to_remote(
        file_to_upload=archive_path,
        remote_path=remote_path)
    if upload_success:
        # Unpack to remote directory
        post_success = do_post_unpack(
            remote_path=remote_path,
            uploaded_file_name=uploaded_file_name,
            file_separator=separator)
        if post_success:
            retval = True
        else:
            retval = False
    else:
        retval = False
    # Returns True if all operations have been done correctly, otherwise
    # returns False
    return retval


def local_file_exists(file_to_check):
    """
    the test -e command checks if file exists
    Return:
        True  : if file exists
        False : if file not found
    """
    try:
        local("test -e {}".format(file_to_check))
    except BaseException:
        return False
    else:
        return True


def remote_directory_exists(directory_to_check):
    """
    the test -e command checks if directory exists
    Return:
        True  : if directory exists
        False : if directory not found
    """
    try:
        run("test -d {}".format(directory_to_check))
    except BaseException:
        return False
    else:
        return True


def upload_file_to_remote(file_to_upload, remote_path):
    """
    Uploads a local file to a remote path
    Verifies that remote directory exists be4 upload
    """
    # verify that the remote path exists
    if remote_directory_exists(directory_to_check=remote_path):
        # remote path found continue
        try:
            put(local_path=file_to_upload, remote_path=remote_path)
        except BaseException:
            return False
        else:
            return True
    else:
        return False


def do_post_unpack(remote_path, uploaded_file_name, file_separator):
    """
    Unpacks a Remote File To a Remote directory
    """
    try:
        # filename without extension> on the web server
        file_without_extension = uploaded_file_name.split(".")[0]
        # Make target Directories
        run("mkdir -p /data/web_static/releases/{}/".format(
            file_without_extension))
        # Uncompress the archive to the folder
        # /data/web_static/releases/<archive
        run("tar -xzf {}{}{} -C /data/web_static/releases/{}/".format(
            remote_path,
            file_separator, uploaded_file_name, file_without_extension))

        # Delete the archive from the web server
        run("rm {}{}{}".format(remote_path, file_separator,
                               uploaded_file_name))

        run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(
            file_without_extension, file_without_extension))
        run("rm -rf /data/web_static/releases/{}/web_static".format(
            file_without_extension))
        # Delete the symbolic link /data/web_static/current from the web server
        run("rm -rf /data/web_static/current")
        # Create a new the symbolic link /data/web_static/current
        run("ln -s /data/web_static/releases/{} /data/web_static/current".format(
            file_without_extension))
    except BaseException:
        # Error Occurred
        return False
    else:
        return True


if __name__ == '__main__':
    # result = do_pack()
    # print(result)
    print(local_file_exists("/tmp/tim"))
