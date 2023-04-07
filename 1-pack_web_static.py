from fabric.api import task, run
from fabric.state import env

env.hosts = [
    # 'server.domain.tld',
    # 'localhost',
    '8c6286ded25f.7c5818d5.alx-cod.online',
    # 'ip.add.rr.ess
    # 'server2.domain.tld',
]
# Set the username
env.user = "root"

# Set the password [NOT RECOMMENDED]
env.password = "533e04c5e8f089201105"
# @task


def mytask():
    result = run('uname -a')
    # print(result)
    if (result):
        return result
    else:
        result = "Error: in Running program"
        return result


if __name__ == '__main__':
    result = mytask()
    print("The output from main is ", result)
