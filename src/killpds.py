#!/usr/bin/python

from appscript import *
import os
import signal
from time import sleep

f = open('/Users/grosser/pds/log/goog.pid')
pid = f.readline()
f.close()

os.kill(int(pid),signal.SIGKILL)

chrome = app('Google Chrome')
chrome.activate()
sleep(2)
chrome.windows[1].active_tab.URL.set(u'http://www.google.com/accounts/Logout')
sleep(2)
#system.keystroke(u'f',using=[k.command_down,k.shift_down])
sleep(1)
chrome.quit()
