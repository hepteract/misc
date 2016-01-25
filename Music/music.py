import subprocess
import signal
import os

class tunnel(object):
    def __init__(self, ip = "atercap.com"):
        self.ip = ip

    def send(self, *cmd):
        cmd = "".join(cmd)
        os.system(" ".join(("ssh", self.ip, cmd)))

ssh = tunnel()

def send_request(url, **req):
    url = "curl -s 'http://localhost:9999/" + url + "?"
    for name, value in req.items():
        url += "".join((name, "=", str(value), "&"))
    url = "".join((url[:-1],'| grep -v ^# | while read url; do mpc add "$url"; done'))
    print url
    ssh.send(url)
req = send = send_request

def mpc_command(cmd):
    ssh.send(" ".join(("mpc", cmd.strip("|&><;$()"))))
mpc = mpc_command
