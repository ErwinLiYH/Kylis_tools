import os
from paramiko import SSHClient
from scp import SCPClient
import argparse
import Kkit
import json
import getpass

def run(path, ssh_argv):
    ssh = SSHClient()
    ssh.load_system_host_keys()
    # ssh.connect(hostname="login.cirrus.ac.uk", username="s2303098", password="Liyuanhao@tf20010103")
    ssh.connect(**ssh_argv)

    remote_paths = []

    for i in os.listdir(path):
        with open(os.path.join(path, i), "r") as f:
            remote_paths += [i.strip() for i in f.readlines() if i.strip()!=""]
        os.remove(os.path.join(path, i))

    for i in remote_paths:
        name = i.split("/")[-1]
        with SCPClient(ssh.get_transport()) as scp:
            print("try to fetch %s from remote..."%i)
            scp.get(i, os.path.join(path, name))
            print("remote:"+i+"->"+"local:"+os.path.join(path, name))
def main():
    home_directory = os.environ["HOME"]

    parser = argparse.ArgumentParser(description='scp helper for "vscode remote-ssh"')
    parser.add_argument("path", type=str, action="store", help="the path of folder or file contains remote pathes")
    parser.add_argument("--config", "-c", default=os.path.join(home_directory, "ktools_conf/scphelper.conf"), type=str, action="store", help="the config file path, default is ~/Myscripts/Conf/scphelper.conf")
    args = parser.parse_args()

    if os.path.exists(args.config)==False:
        conf_dict = {}
        conf_dict["username"] = input("input user name: ")
        while True:
            passwd = getpass.getpass("input password:")
            passwd2 = getpass.getpass("please input again: ")
            if passwd==passwd2:
                break
            else:
                print("password should be same as the first one!")
        conf_dict["password"] = passwd
        conf_dict["hostname"] = input("input host name: ")

    ssh_conf = json.loads(Kkit.load(args.config, "utf-8"))
    run(args.path, ssh_conf)

if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Force quit")