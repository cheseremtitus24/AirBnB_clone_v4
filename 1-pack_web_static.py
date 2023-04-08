#!/usr/bin/python3
"""
This module makes use of fabric version 1.14.2
and automates the creation of archive files
on a remote host
"""

# Import Fabric's API module
from datetime import datetime
import os

from fabric.api import task, run, env
from fabric.operations import local

# env.hosts = [
# 'server.domain.tld',
# 'localhost',
# '8c6286ded25f.7c5818d5.alx-cod.online'
# 'ip.add.rr.ess
# 'server2.domain.tld',
# ]
# Set the username
# env.user = "root"

# Set the password [NOT RECOMMENDED]
# env.password = "533e04c5e8f089201105"
# env.hosts = ['localhost']


@task
def do_pack():
    """
       compresses web folder files and
       versions them based on timestamp.
  """
    retval = None
    try:
        # Create the appropriate directory tree using native python.
        result = local("mkdir -p ./versions")
        # print("After Creating Dir result: ",type(str(result)))
        fileName = "{}".format(datetime.now().strftime('%Y%m%d%H%M%S'))
        result = local(
            "tar -czvf versions/web_static_{}.tgz\
             ./web_static".format(fileName))
        # print("Result of Tar: ",result)

        # Unix -bash implementation
        # fileSize = local(
        #    'stat -c "%s" versions/web_static_{}.tgz'.format(fileName))
        fileSize = os.stat(
            os.path.join(
                'versions',
                'web_static_{}.tgz'.format(fileName))).st_size

        retval = "web_static packed: \
        versions/web_static_{}.tgz -> {}Bytes".format(fileName, fileSize)
        return retval
    except BaseException:
        return retval


if __name__ == '__main__':
    result = do_pack()
    print(result)
