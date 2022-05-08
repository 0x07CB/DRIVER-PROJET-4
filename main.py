#!/usr/bin/python3
import json
from os import system

actions = [
    {
        "json": "CONFIRM_TARGET.json",
        "action": "--no-confirm"
    },
    {
        "json": "exemple-input-IDTypeCmds.json",
        "action": "--no-confirm"
    },
    {
        "json": "information-about-current-host.json",
        "action": "hostname && ip a && curl ifconfig.me"
    },
    {
        "json": "information-about-current-user.json",
        "action": "w && whoami"
    },
    {
        "json": "nmap-target.json",
        "action": "--no-confirm"
    },
    {
        "json": "DBL_CONFIRM.json",
        "action": "\n"
    },
    {
        "json": "exit.json",
        "action": "exit"
    },
    {
        "json": "sshd_disable.json",
        "action": "sudo systemctl disable --now sshd && sudo systemctl status sshd"
    },
    {
        "json": "sshd_enable.json",
        "action": "sudo systemctl enable --now sshd && sudo systemctl status sshd"
    },
    {
        "json": "killall-ssh.json",
        "action": "sudo killall ssh"
    }
]


class jsCommand(object):
    def __init__(self):
        global actions
        self.action = actions
        self.js_commands_loader(self.action)
        self.act = None
        
    def js_commands_loader(self,data_actions):
        for i in data_actions:
            with open("js_commands/{}".format(i["json"]),"rb") as f:
                i["capture"] = json.loads(f.read())
        self.action = data_actions
        
    def js_commands_read(self):
        with open("out.json",'rb') as f:
            data = json.loads(f.read())
            f.close()
        self.act = data
    
    def js_commands_play(self):
        for i in self.action:
            if i["capture"]["body"] == self.act["body"]:
                system("{}".format(i["action"]))
                return True
        return False
        

jsC = jsCommand()
while True:
    system("sudo python3 super-remote.py")
    jsC.js_commands_read()
    if jsC.js_commands_play():
        print("")
    else:
        print("No commands recognized!")
