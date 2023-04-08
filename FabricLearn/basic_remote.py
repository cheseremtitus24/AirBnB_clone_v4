"""
This module makes use of fabric version 1.14.2
and automates the creation of archive files
on a remote host
"""
# Import Fabric's API module
from fabric.api import task, run, env


env.hosts = [
#'server.domain.tld',
    # 'localhost',
    '8c6286ded25f.7c5818d5.alx-cod.online'
  # 'ip.add.rr.ess
  # 'server2.domain.tld',
]
# Set the username
env.user   = "root"

# Set the password [NOT RECOMMENDED]
env.password = "533e04c5e8f089201105"

@task
def do_pack():
    """
       compresses web folder files and
       versions them based on timestamp.
  """
    retval = None
    try:
        result = run("mkdir -p ./versions")
        # print("After Creating Dir result: ",type(str(result)))
        fileName = run('date +"%Y%m%d%H%M%S"')
        # result = run('tar -czvf versions/web_static_$(date +"%Y%m%d%H%M%S").tgz ./web_static')
        result = run('tar -czvf versions/web_static_{}.tgz ./web_static && echo $?'.format(fileName))
        # print("Result of Tar: ",result)
        fileSize = run('stat -c "%s" versions/web_static_{}.tgz'.format(fileName))
        retval = "web_static packed: versions/web_static_{}.tgz -> {}Bytes".format(fileName,fileSize)
        return retval
    except BaseException:
        return retval

    # return None
if __name__ == '__main__':
    result = do_pack()
    print(result)