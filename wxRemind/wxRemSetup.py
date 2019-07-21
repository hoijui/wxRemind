#!/usr/bin/python
# $Id: wxRemAlert.py 14 2006-05-09 12:20:50Z dag $
import wx
from wxRemConfig import * 
import sys, os, re, datetime
import shutil
msg = []
warn = []

today = datetime.date.today().strftime("%d %b %Y")
d = {'remind' : '', 'festival' : '', 'gv' : ''}
d['gv_opts'] = gv_opts
d['calendars'] = os.path.expanduser(calendars)

reminders = os.path.expanduser("~/.reminders")
has_reminders = os.path.isfile(reminders)
reminders_backup = os.path.expanduser("~/.reminders.bak")
d['reminders'] = reminders

wxremindrc = os.path.expanduser("~/.wxremindrc")
has_wxremindrc = os.path.isfile(wxremindrc)
new_wxremindrc = False

wxremfloat = os.path.expanduser("~/.wxremfloat")
has_wxremfloat = os.path.isfile(wxremfloat)

include_line = """INCLUDE %s
REM %s MSG Thanks for using wxRemind!%%""" % (wxremfloat, today)

alert_wave = '/usr/share/sounds/KDE_Notify.wav'
has_sound = os.path.isfile(alert_wave)
if has_sound:
    d['sound'] = alert_wave
else:
    d['sound'] = ''

def make_wxremindrc(d):
    global msg, warn, new_wxremindrc
    WXREMINDRC = """\
# Configuration settings for wxRemind
# This file should be named ~/.wxremindrc

# REMIND 
remind = '%(remind)s'

# Festival (necessary for spoken alerts)
festival = '%(festival)s'

# gv (ghostview - necessary to display and print monthly calendars)
gv = '%(gv)s'
# Options to pass to gv
gv_opts = '%(gv_opts)s'
# Put temporary postscript calendar files here
calendars = '%(calendars)s'

# The reminders file
reminders = '%(reminders)s'

# TIME DISPLAY 12 hour (1) or 24 hour (0)
twelvehour = 1

# MONTHLY CALENDAR ORIENTATION landscape (1) or portrait (0)
landscape = 1

# show splashscreen on startup for this many seconds or 0 for not at all
showsplash = 2

# EDITOR - Leave empty to use interal editor
editor = ''
# editor = "/usr/local/bin/gvim"
# editor = "/usr/bin/emacs"


# EDIT COMMAND SUBSTITUTIONS
# These are irrelevant if using the default interal editor
# %%(e)s -> the editor named above
# %%(n)s -> line number to edit
# %%(f)s -> file name
# COMMAND FOR EDITING AN OLD APPOINTMENT (irrelevant with internal editor)
editold = ''                                # internal editor
# editold = "%%(e)s -f +%%(n)s %%(f)s"      # gvim 
# editold = "%%(e)s +%%(n)s %%(f)s"         # emacs
# COMMAND FOR EDITING A NEW APPOINTMENT  (irrelevant with internal editor)
editnew = ''                                # internal editor
# editnew = "%%(e)s -f + %%(f)s"            # gvim
# editnew = "%%(e)s +999999 %%(f)s"         # emacs

# A TIMED EVENT WITH AN ALERT
# The system command to "play" a wav file
alert_play = '%(play)s'
# The wave file to play
alert_wave = '%(sound)s'
# ALERT DEFAULTS 
# Display the alter box (1) or not (0)
alert_display = 1
# Silent (0), execute alert_soundcmd (1) or play spoken message (2)
alert_sound = 1
# Add a time appropriate greeting to spoken message, e.g., "Good morning"
alert_greeting = 1
# Add a name if non-null to the spoken greeting, e.g, "Good morning, Dan"
alert_whom = ''
# Replace all 3-digit numbers in msg with spoken equivalents, e.g., Replace
# '201' with '2 O1' where O is an uppercase o) and '385' with '3 85'. Thus
# '201' would be spoken as 'two oh one' and '385' as 'three eighty-five'.
# Why course and room numbers are spoken this way is a mystery to me.
alert_parsenums = 1

# The string provided for 'alert_other_message' will be inserted in the 'Other
# Message' field when a new alert reminder is created. Such a message will not
# appear on the calendar but will be appended to 'Message' for alerts. 
alert_other_message = '%%1'

# For example, with 
#   alert_display = 1
#   alert_sound = 2
#   alert_greeting = 1
#   alert_whom = 'Dan' 
#   alert_parsenums = 1
#   alert_other_message = '%%1'
# a new alert reminder created with April 11, 2006 selected on the calendar
# would initially have the following entries:
#   Date: 11 Apr 2006
#   Time:
#   Duration:
#   Message:
#   Other Message: %%1
#   Visual Alert: 2nd button (Pop-up Display) checked
#   Audible Alert: 3rd button (Spoken Message) checked
# After entering '10:50 +5' for Time, '1:15' for Duration and 'Economics 201'
# for Message, the resulting reminder would be
#   REM 11 Apr 2006 AT 10:50 +5 DUR 1:15 RUN wxremalert -d1 -s2 %%"Economics 201%%" %%1%%
# The calendar for Apr 11 would then display
#   10:50AM - 12:05PM  Economics 201
# and, at 10:45 on Apr 11 the following message would be spoken
#   "Good morning, Dan. The time is ten forty-five. Economics two oh one five
#    minutes from now."
# and later, at 10:50:
#   "Good morning, Dan. The time is ten fifty. Economics two oh one now."

# FONTSIZES
# The base fontsize
basefontsize = 10
# The adjustment to the base font size for the status bar
statusfontadj = 0
# The adjustment to the base font size for the event list
listfontadj = 0
# The adjustment to the base fontsize for the selected date header above the
# event list
datefontadj = 0
# The adjustment to the base fontsize for today button
buttonfontadj = 0
# The adjustment to the base fontsize for the calendar
calendarfontadj = 0

# Custom fontsizes may require adjustments to panel sizes.
# The absolute startup size (horizontal, vertical) of the event list
eventsize = (500,380)
# The event list resizes automatically with the window size but the calendar
# and clock keep their startup sizes.
# The default size of the calendar takes account of the font size. 
# The following adjustment (horizontal, vertical) fine tunes this default. 
calsizeadj = (16, -4) 
# The absolute size of the (fontless) analogclock: 
clocksize = 190
# The absolute size of the internal editor window:
editorsize = (800,400)

# COLORS
# calendar busy times and colors
busy0 = (30,'SLATEBLUE2')
busy1 = (75, 'BLUE2')
busy2 = (150, 'GREEN4')
busy3 = (225, 'DARKORANGE')
busy4 = (300, 'RED')
# Days with appointments totaling less than 30 minutes have foreground (font)
# color BLACK. Days with at least 30 minutes but less than 75 are SLATEBLUE2
# and so forth.
# Time to assign to events with no duration in computing day event totals:
zerominutes = 15

# for the calendar
holidaycolor = 'BLACK'
headercolor = 'NAVYBLUE'

# BACKGROUND COLORS
# bgcolor: The general background color.
# nfcolor: The background color for the event list and calendar, whichever has
# the focus.
# fcolor:  The background color for the event list and calendar, whichever does
# not have the focus.

# There are two ways of specifying these background colors. The first is simply
# to specify these colors directly, e.g., 
# handcolor = 'GRAY50'
# bgcolor   = "GRAY90"
# nfcolor   = "GRAY94"
# fcolor    = "GRAY99"

# The second way is to specify a color 'family' from one of the 'numbered'
# color families supported by python. Here is a partial list:

#    "AZURE" "BISQUE" "CORNSILK" "DARKOLIVEGREEN" "DARKSEAGREEN" "HONEYDEW"
#    "IVORY" "KHAKI" "LAVENDERBLUSH" "LEMONCHIFFON" "LIGHTGOLDENROD"
#    "LIGHTSKYBLUE" "LIGHTSTEELBLUE" "LIGHTYELLOW" "MISTYROSE" "NAVAJOWHITE"
#    "PALEGREEN" "PEACHPUFF" "THISTLE" "WHEAT" 

# For each of these python supports four named colors, e.g., 'IVORY1',
# 'IVORY2', 'IVORY3' and 'IVORY4'. Simply setting
#    colorfamily = "IVORY"
# has exactly the same effect as setting
#    handcolor = "IVORY4"
#    bgcolor   = "IVORY3"
#    nfcolor   = "IVORY2"
#    fcolor    = "IVORY1"
# and, in fact, will override any individual color settings.

colorfamily = "IVORY"


# borders: sunken (-1), flat (0) or raised (1)
# event and calendar borders
ec_border = 1
""" % d
    if has_wxremindrc:
        fo = open("%s.new" % wxremindrc, 'w')
        msg.append("""\
Found an existing %s
    and created a new wxremindrc as %s.new""" % (wxremindrc, wxremindrc))
        new_wxremindrc = True
    else:
        fo = open(wxremindrc, 'w')
        msg.append("Created new %s" % wxremindrc)
    fo.write(WXREMINDRC)
    fo.close()

def make_wxremfloat():
    global msg, warn
    WXREMFLOAT = """\
##########################################################
# Do Not Edit - Updates to wxRemind overwrite this file. #
##########################################################
# Support for floating reminders
# This file should be named ~/.wxremfloat
#   To enable floating reminders make sure your reminders file 
#   includes the line
#
#      INCLUDE %s
#
#   prior to any use of float()
#
IF  ($CalMode || $PSCal )
    # For Cal and PS calendars, only trigger the event on the due date.
    FSET float(y,m,d,n) trigger(date(y,m,d))
ELSE
    # For Simple Calendar (rem -s) and other modes, also set warning trigger,
    # priority and suffixes.
    FSET float(y,m,d,n) iif(date(y,m,d) == today(), trigger(today()) + \\
    " PRIORITY 1000", trigger(MAX(realtoday(), date(y,m,d)-n)) + \\
    iif(n >= date(y,m,d) - today(), " PRIORITY " + \\
    (1000 + (date(y,m,d) - today())),"")))

    FSET msgsuffix(x) iif(0 > x, "", \\
    998 >= x, " (" + (1000-x) + " days ago)", \\
    999 >= x, " (yesterday)", \\
    1000 >= x, " (today)", \\
    1001 >= x, " (tomorrow)", \\
    2000 >= x, " (in " + (x - 1000) + " days)", "")

    # This calsuffix is used by wxRemind
    FSET calsuffix(x) iif(0 > x, "", \\
    998 >= x, " (" + (1000-x) + "  days ago)", \\
    999 >= x, " (yesterday)", \\
    1000 >= x, " (today) ", \\
    1001 >= x, " (tomorrow)", \\
    2000 >= x, " (in " + (x - 1000) + " days)", "")
ENDIF
""" % wxremfloat
    fo = open(wxremfloat, 'w')
    fo.write(WXREMFLOAT)
    fo.close()
    msg.append("Created %s" % wxremfloat)

def PathSearch(filename):
    search_path = os.getenv('PATH').split(os.pathsep)
    for path in search_path:
        candidate = os.path.join(path,filename)
        if os.path.os.path.isfile(candidate):
            return os.path.abspath(candidate)
    return ''

def DepCheck():
    global d, msg, warn
    v = sys.version.split()[0]
    if v < '2.3':
        warn.append("Error: Found Python %s. You need Python >= 2.3 to use this package." % v)
    else:
        msg.append("Found python version %s" % v)
    try:
        import wx
        w = wx.VERSION_STRING
        if w < '2.6.1':
            warn.append("Error: Found wxPython %s. You need wxPython >= 2.6.1 to use this package." % w)
        else:
            msg.append("Found wxPython version %s" % w)
    except:
        warn.append("Error: You do not have wxPython installed. You need wxPython >= 2.6.1 to use this package.")

    d['remind'] = PathSearch('remind')
    if d['remind']:
        msg.append("Found remind at '%s'" % d['remind'])
    else:
        warn.append("""
Error: Could not find remind in your PATH. Remind must be installed 
with the executable 'remind' in your system path.""")

    d['festival'] = PathSearch('festival')
    if d['festival']:
        msg.append("Found festival at '%s'" % d['festival'])
    else:
        warn.append("""\
Error: Could not find festival in your PATH. Festival must be installed
with the executable 'festival' in your system path for you to be able to
use spoken alerts.""")

    d['gv'] = PathSearch('gv')
    if d['gv']:
        msg.append("Found gv at '%s'" % d['gv'])
    else:
        warn.append("""\

Error: Could not find gv in your PATH. You will need to install ghostview (gv
or gnome-gv), or some other postscript viewer and to correct the setting for
'gv' in %s to be able to view and print postscript monthly calendars.""" %
wxremindrc)

    d['play'] = PathSearch('play')
    if d['play']:
        msg.append("Found play at '%s'" % d['play'])
    else:
        warn.append("""\
Error: Could not find play in your PATH. This program is part of the sox 
package and is used to play a wav file as an audible alert.  You will need 
to correct the setting for 'alert_play' in %s to be able to use sound 
alerts.""" % wxremindrc)

    if has_sound:
        msg.append("Found alert_wave file: %s" % alert_wave)
    else:
        warn.append("""\
Could not find the default alert sound wave file, %s. You will need to correct
the setting for 'alert_wave' in %s to be able to use sound alerts.""" %
(alert_wave, wxremindrc))

def make_reminders():
    global msg, warn
    # If there is an existing reminders file, see if it includes wxremfloat
    # and, if it does not, backup the file and insert the include line at the
    # beginning.
    if has_reminders:
        found = False
        msg.append("Found reminders file: '%s'" % reminders) 
        regex = re.compile(r'^\s*INCLUDE .*\.wxremfloat')
        fo = open(reminders, 'r')
        lines = fo.readlines()
        fo.close()
        for line in lines:
            if regex.match(line):
                found = True
                break
        if found:
            msg.append("  and it 'includes' .wxremfloat") 
        else:
            msg.append("  but it does not 'include' .wxremfloat") 
            lines.insert(0, "%s\n" % include_line)
            shutil.copyfile(reminders, "%s.bak" % reminders)
            msg.append("  Created backup %s.bak"% reminders)
            fo = open(reminders, 'w')
            fo.writelines(lines)
            fo.close()
            msg.append("  Inserted '%s' as the first line in %s" 
                    % (include_line, reminders))
    else:
        fo = open(reminders, 'w')
        fo.write(include_line)
        fo.close()
        msg.append("Created new %s" % reminders)



def report():
    global new_wxremindrc
    if new_wxremindrc:
        new_msg = """\
IMPORTANT: It is strongly recommended that you edit ~/.wxremindrc.new to
reflect any custom settings that you may have made in your existing
~/.wxremindrc, and then save ~/.wxremindrc.new as ~/.wxremindrc.
"""
    else:
        new_msg = ''

    if len(warn) > 0:
        warnings = """
The following warnings were generated during configuration:
  %s""" % '\n  '.join(warn)
    else:
        warnings = ''
    if len(msg) > 0:
        messages = """
The following information messages were generated during configuration:
  %s""" % '\n  '.join(msg)
    else:
        messages = ''

    print """
                ===============================
                    Configuration Completed 
                ===============================
%s%s

%s
Absent warning messages to the contrary, you should now be able run
wxremind and the other wxRemind scripts.

Once wxremind is running, pressing ? will bring up a display of usage
information.
""" % (messages, warnings, new_msg)

def setup():
    print """
                ===============================
                     wxRemind Configuration 
                ===============================

This configuration process will check for sufficiently recent versions of
'python' and 'wxPython', for the presence of 'remind', 'festival', 'gv' and
'play' in your system path and for the existence of the default alert sound
file. 

It will then create '.wxremfloat' in your home directory, overwriting any
existing file.  The contents of this file will make it possible for you to 
use floating reminders.

Next it will check for the existence of '.reminders' and '.wxremindrc' in your
home directory. If '.reminders' exists it will be checked to make sure that it
contains an 'include .wxremfloat' line. If it does not, first a backup will be
made named '.reminders.bak' and then the appropriate line will be inserted at
the beginning of the original file. If '.reminders' does not exist, then it
will be created with the necessary line as its only content.

A new configuration file will then be created called '.wxremindrc' if this file
does not alread exist and '.wxremindrc.new' otherwise. This file will
automatically contain the correct settings for 'remind', 'festival', 'gv' and
'play' and, of course, for 'reminders' and 'wxremfloat'.

Finally, a report of messages generated during configuration will be displayed.

      THIS SCRIPT MUST BE RUN WITH YOUR NORMAL USERID AND NOT AS ROOT. 
         CANCEL IF THIS IS NOT THE CASE AND RESTART AS YOURSELF.
"""

    ans = raw_input('Continue with configuration? [yN] ')
    if ans == 'y':
        DepCheck()
        make_wxremindrc(d)
        make_wxremfloat()
        make_reminders()
        report()
    else:
        print """
wxRemind configuration cancelled.
"""

if __name__ == "__main__":
    setup()
