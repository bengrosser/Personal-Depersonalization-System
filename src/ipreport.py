#!/usr/bin/python

import socket
import subprocess

myip = socket.gethostbyname(socket.gethostname())

f = open('/Users/grosser/pds/log/goog.ip','w')
f.write(myip)
f.close()

command = ['scp']
command.append('/Users/grosser/pds/log/goog.ip')
command.append('bengrosser.com:/home/grosser/goog/goog.ip')
p = subprocess.Popen(command)
p.wait()

