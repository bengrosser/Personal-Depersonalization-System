#/usr/bin/python

# Personal Depersonalization System
# 
# v 1.0
# by Ben Grosser
# July, 2011

# first exhibited at Figure One, Champaign, IL, July 2011

# Google search automation for the conceptual art purpose of filling 
# Google's data profile of me with random bullshit.  Takes a random
# word from the dictionary, searches for it, and then clicks on a link,
# repeat forever (or at least while being viewed).  System also changes
# location, meta search categories, etc.

# http://bengrosser.com/projects/personal-depersonalization-system/



from appscript import *
from time import sleep
from random import uniform
from random import randint 
from random import shuffle
import sys
import os
import signal

runlength = 1005
metaexpanded = False
pausemeta = False
lastchoice = 0

def slowtype(text):
    for char in text:
        app(u'System Events').keystroke(char)
        sleep(uniform(0.1,1.0))

chrome = app('Google Chrome')
system = app('System Events')

# get dictionary words
d1 = open('/usr/share/dict/web2')
d2 = open('/usr/share/dict/web2a')

words = []

for line in d1:
    words.append(line)

for line in d2:
    words.append(line)

d1.close()
d2.close()

# words/location log file
#log = open('goog.log','a')

pid = open('/Users/grosser/pds/log/goog.pid','w')
pid.write(str(os.getpid()))
pid.close()

def handler(signum,frame):
    log.close()

signal.signal(signal.SIGHUP,handler)

totalwords = len(words)
wordchoice = range(0,totalwords-1)
shuffle(wordchoice)

# get zipcode info
z = open('/Users/grosser/pds/src/zips.txt')
zipfile = z.readlines()
z.close()
zips = []
for line in zipfile:
    zips.append(line[0:5])
zippicks = []
zippicks = range(0,len(zips))
shuffle(zippicks)


# setup location change template
locationchance = []

cnt = 0

while cnt < runlength:
    pick = randint(0,100)
    if pick > 92:
        locationchance.append(1)
    else:
        locationchance.append(0)
    cnt += 1


cnt = 0

# login first
chrome.quit()
sleep(3)
chrome = app('Google Chrome')
sleep(2)
chrome.activate()
sleep(2)
system.keystroke(u'f',using=[k.command_down,k.shift_down])
sleep(2)
chrome.windows[1].active_tab.URL.set(u'http://www.google.com/accounts/Logout')
sleep(2)
# username
slowtype("")
sleep(.5)
system.keystroke(u'\t')
sleep(.5)
# password
slowtype("")
sleep(.5)
system.keystroke(u'\r')
sleep(1)




# do the searching
while cnt < runlength:
    # load google homepage
    chrome.activate()
    chrome.windows[1].active_tab.URL.set(u'http://www.google.com')
    sleep(uniform(0.4,0.9))

    # check if we're changing location during this search term
    if locationchance[cnt] == 1:
        changinglocation = True
    else:
        changinglocation = False

    # type the search term and hit enter
    word = words[wordchoice[cnt]]
    print "search term: %s" % word
    slowtype(word)
    system = app('System Events')
    system.keystroke(u'\r')
    sleep(uniform(0.3,0.8))

    # if we're changing location, then do it
    if(changinglocation):
        pausemeta = True

        # click the 'change location' text
        #chrome.windows[1].active_tab.execute(javascript=u"google.x(this,function(){google.loc.toggleLocationChange()});var e=arguments[0]||window.event;e.stopPropagation?e.stopPropagation():e.cancelBubble=true;return false;")

        chrome.windows[1].active_tab.execute(javascript=u"function simulateClick(elm) { var evt = document.createEvent('MouseEvents'); evt.initMouseEvent('click', true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null); var canceled = !elm.dispatchEvent(evt); }; simulateClick(document.getElementById('toggle_location_link'));")

        sleep(uniform(0.3,0.8))

        # focus on the new text box
        chrome.windows[1].active_tab.execute(javascript=u"document.getElementById('lc-input').focus();")

        sleep(uniform(0.3,0.8))

        # get a new zip
        newzip = zips[zippicks[cnt]]
        print '[' + newzip + ']',

        # slowtype the new zip
        slowtype(newzip)

        # hit return
        system = app('System Events')
        system.keystroke(u'\r')

        sleep(uniform(1.2,1.8))

        # now refocus on the search box for the next step
        chrome.windows[1].active_tab.execute(javascript=u"document.getElementsByName('q').focus();")

        # end location change

    # metaitem change
    # seven choices: all, video, books, blogs, discussions, patents
    # much higher chance of all
    metachoice = [0,0,0,0,2,5,7,8]
    #metachoice = [0,2,7,8]
    shuffle(metachoice)
    metapick = metachoice[randint(0,len(metachoice)-1)]

    print "metapick = %d" % metapick
    print "lastchoice = %d" % lastchoice

    # if we're changing meta search and we didn't change location this term, then change the meta category
    if not pausemeta:

        # if the new meta item is larger than 4 (not seen), then click the 'More' button
        if metapick > 4:
            print "expanding meta because pick > 4"

            chrome.windows[1].active_tab.execute(javascript=u"document.getElementById('showmodes').onclick();")

        sleep(uniform(0.4,0.8))

        print "selecting meta item # %d" % metapick
        # click on the new meta search term
        js = 'function simulateClick(elm) { var evt = document.createEvent("MouseEvents"); evt.initMouseEvent("click", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null); var canceled = !elm.dispatchEvent(evt); }; simulateClick(document.getElementsByClassName("mitem")[' + str(metapick) + '].getElementsByClassName("kl")[0]);'
        print js

        chrome.windows[1].active_tab.execute(javascript=u"function simulateClick(elm) { var evt = document.createEvent('MouseEvents'); evt.initMouseEvent('click', true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null); var canceled = !elm.dispatchEvent(evt); }; simulateClick(document.getElementsByClassName('mitem')[" + str(metapick) + "].getElementsByClassName('kl')[0]);")

        sleep(uniform(0.4,0.8))

    lastchoice = metapick
    pausemeta = False
    # --end metaitem

    
    # ok, now we're ready to proceed with searching

    system = app('System Events')
    system.key_code(48)
    sleep(.1)




    # click on the first magnifying glass
    chrome.windows[1].active_tab.execute(javascript=u"document.getElementsByClassName('vspib')[0].click();")

    # new way
    system = app('System Events')
    system.key_code(124)
    sleep(.1)

    # select a result
    selection = randint(3,9)
    resultindex = 0

    if selection == 0:
        sleep(uniform(0.1,2.1))
    else:
        # click down through each item until we get to the selection
        while selection != 0:
            sleep(uniform(0.8,1.8))

            # if we changed location then we have to navigate a different way
            if(changinglocation):
                chrome.windows[1].active_tab.execute(javascript=u"document.getElementsByClassName('vspib')[" + str(resultindex) + "].click();")
                resultindex += 1

            # otherwise we can just use the down arrow
            else:
                system = app('System Events')
                system.key_code(125)

            selection -= 1


    sleep(uniform(0.2,0.8))

    # we're there, so now select it (based on how we got there)
    if(changinglocation):
        chrome.windows[1].active_tab.execute(javascript=u"window.location = document.getElementsByClassName('l')[" + str(resultindex-1) + "].getAttribute('href');")
    else:
        system = app('System Events')
        system.keystroke(u'\r')

    # hold for a bit so the visited page can load
    if metapick == 2:
        sleep(uniform(11.1,15.1))
    else:
        sleep(uniform(9.1,13.1))

    
    picklocation = chrome.windows[1].active_tab.URL.get()
    logline = word + ',' + picklocation + '\n'
    log = open('/Users/grosser/pds/log/goog.log','a')
    log.write(logline)
    log.close()


    changinglocation = False
    cnt += 1
    
    numstr = str(cnt) + ', '

    print numstr,
    sys.stdout.flush()



# logout 
chrome.activate()
sleep(2)
chrome.windows[1].active_tab.URL.set(u'http://www.google.com/accounts/Logout')
sleep(2)
system.keystroke(u'f',using=[k.command_down,k.shift_down])
sleep(1)
chrome.quit()

