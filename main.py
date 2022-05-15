#!/usr/bin/python3
import json
from os import system

actions = [
    {
        "json": "pacman_update.json",
        "action": "bash -c 'pacman -Syu --noconfirm'"
    },
    {
        "json": "information-about-current-host.json",
        "action": "bash -c 'hostname && ip a && curl ifconfig.me'"
    },
    {
        "json": "information-about-current-user.json",
        "action": "bash -c 'w && whoami && echo $USER'"
    },
    {
        "json": "nmap-current.json",
        "action": "bash -c 'nmap -v -A $(curl ifconfig.me)'"
    },
    {
        "json": "exit.json",
        "action": "exit"
    },
    {
        "json": "sshd_disable.json",
        "action": "bash -c 'sudo systemctl disable --now sshd && sudo systemctl status sshd'"
    },
    {
        "json": "sshd_enable.json",
        "action": "bash -c 'sudo systemctl enable --now sshd && sudo systemctl status sshd'"
    },
    {
        "json": "killall-ssh.json",
        "action": "bash -c 'sudo killall ssh'"
    },
    {
        "json": "btop.json",
        "action": "bash -c 'btop'"
    },
    {
        "json": "htop.json",
        "action": "bash -c 'htop'"
    },
    {
        "json": "check-systemd.json",
        "action": "bash -c 'sudo systemctl --failed'"
    },
    {
        "json": "vimls.json",
        "action": "bash -c 'ls -lharc && sleep 10s && vim ./'"
    },
    { 
        "json": "date.json",
        "action": "bash -c 'echo $(date)'"
    },
    {
        "json": "timetrap-full-info.json",
        "action": "bash -c 't now && t display'"
    },
    {   
        "json": "clear.json",
        "action": "bash -c 'clear'"
    },
    {
        "json": "mode-numbers-type.json",
        "action": "<number_typing>"
    }
]

actions_numbers = [
    {
        "json": "int_num_inc1.json",
        "action": int(+1)
    },
    {   
        "json": "int_num_dec1.json",
        "action": int(-1)
    },
    {
        "json": "int_num_inc10.json",
        "action": int(+10)
    },
    {   
        "json": "int_num_dec10.json",
        "action": int(-10)
    }
]


class jsCommand(object):
    def __init__(self,custom=None):
        global actions_numbers
        global actions
        self.BUFFER=""
        self.NUMBER=0
        
        if custom == "numbers":
            self.action = action_numbers
            self.js_commands_loader(self.action_numbers)
            self.act=None

        else:
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
            k=0
            for j in range(0,len(self.act["body"])):
                #print(self.act["body"][j], i["capture"]["body"][j])
                try:
                    if i["capture"]["body"][j] == self.act["body"][j]:
                        k+=1
                except:
                    pass
            if k == len(self.act["body"]):
                if i["action"] == "<number_typing>":
                    self.number_typing()
                elif type(i["action"]) == int:
                    self.NUMBER+=i["action"]
                    return self.NUMBER
                else:
                    system("{}".format(i["action"]))
                return True
        return False
    def number_typing(self):
        print("<NUMBERS TYPING MODE>")
        numbermode()
    def get_number(self):
        return self.NUMBER



def numbermode():
    j = jsCommand(custom="numbers")
    while True:
        print("          ^^         ")
        print("         (+1)        ")
        print("<== (-10) || (+10)==>")
        print("         (-1)        ")
        print("          vv         ")
        system("sudo python3 super-remote.py 1")
        j.js_commands_read()
        nb=j.js_commands_play()
        if type(nb) == int:
            with open("/dev/stdout" ,"wb") as stdf:
                stdf.write(str(j.get_number()).encode())
                stdf.close()
        elif nb == "OK":
            pass
        elif nb == "BACK":
            pass
        else:
            pass

    
jsC = jsCommand()
while True:
    system("sudo python3 super-remote.py 2")
    jsC.js_commands_read()
    if jsC.js_commands_play():
        print("")
    else:
        print("No commands recognized!")
