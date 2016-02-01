#!/usr/bin/env python2

from fabric.contrib import files
from fabric import api
import sys

HOSTS = ['dynasty.tetradecaexon.com']

def config_upstart():
    files.upload_template("upstart.conf", "/etc/init/node_exporter.conf",\
                          use_sudo = True)

def config_systemd():
    files.upload_template("systemd.service",\
                          "/etc/systemd/system/node_exporter.service",\
                          use_sudo = True)
    api.sudo("systemctl daemon-reload")
    api.sudo("systemctl enable node_exporter")

def node(version = "0.11.0"):
    api.run("cd ~")
    api.run("mkdir -p ~/Downloads")

    api.run("wget https://github.com/prometheus/node_exporter/releases/download/%s/node_exporter-%s.linux-amd64.tar.gz -O ~/Downloads/node_exporter.tar.gz"\
            % (version, version))

    api.run("tar xf ~/Downloads/node_exporter.tar.gz")

    with api.settings(warn_only = True):
        if api.sudo("ln -s ~/node_exporter /usr/bin").failed:
            api.sudo("rm /usr/bin/node_exporter")
            api.sudo("ln -s ~/node_exporter /usr/bin")
        if api.run("which systemctl").succeeded:
            config_systemd()
        elif api.run("which initctl").succeeded:
            config_upstart()
        else:
            print >> sys.stderr,\
                  "Failed to detect init system. Ignoring."

    api.sudo("service node_exporter start")
    
def local(*hosts):
    for host in hosts:
#        api.sudo("bash -c 'echo " + "".join(("\n         '", host, "'")) + " >> /home/elijah/Prometheus/server/prometheus.yml")
        files.append("/home/elijah/Prometheus/server/prometheus.yml",\
                 "".join(("     - '", host, ":9100'")), use_sudo = True)
    api.sudo("service prometheus restart")

def install(version = "0.11.0"):
    node(version)
    local()
    
