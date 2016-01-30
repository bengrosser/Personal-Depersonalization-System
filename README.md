## Personal Depersonalization System

[Personal Depersonalization System](http://bengrosser.com/projects/personal-depersonalization-system/) is an automated query machine that depersonalizes my Google profile by hiding my real interests and inclinations within a sea of random noise. The work grabs words from Webster’s 1934 Second International dictionary, searches for them, and selects one of the results to visit. It also occasionally changes locations and meta search categories.  It was first exhibited in the peer-reviewed show *Accepted Knowing* at *Figure One* in Champaign, IL, July 2011.

### Files

__src__ contains the files of interest:
* pds.py : the primary code
* killpds.py : kills a running pds process
* ipreport.py : some reporting for remote management

### Dependencies

* written to work with Google Chrome on OS X
* uses/requires AppleScript
* uses/requires [appscript](http://appscript.sourceforge.net/index.html)
* uses the built-in unix dictionary on OS X
* maybe other things I've forgotten

### Note

* This code is currently written to run the app in an exhibition mode (meaning it full-screens Chrome and wants the foreground). It wouldn't take too much work to adapt for background activity.
* There is currently no handling of two-factor authentication. To work around this, comment out logout/login code and login/authenticate manually.

### Project Homepage
* [Personal Depersonalization System](http://bengrosser.com/projects/personal-depersonalization-system/)
