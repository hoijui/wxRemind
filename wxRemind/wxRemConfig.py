# Configuration settings for wxRemind
# $Id: wxRemConfig.py 14 2006-05-09 12:20:50Z dag $

# REMIND 
remind = 'remind'

# Festival (necessary for spoken alerts)
festival = ''

# ggv (Gnome Ghostview - necessary to display and print monthly calendars)
ggv = 'ggv'

# REMINDERS
reminders = '~/.reminders'

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

# Festival (necessary for spoken alerts)
# leave empty if festival is not installed
festival = ''
# festival = '/usr/bin/festival'

# EDIT COMMAND SUBSTITUTIONS
# %(e)s -> the editor named above
# %(n)s -> line number to edit
# %(f)s -> file name
# COMMAND FOR EDITING AN OLD APPOINTMENT (irrelevant with internal editor)
editold = ''                            # internal editor
# editold = "%(e)s -f +%(n)s %(f)s"     # gvim 
# editold = "%(e)s +%(n)s %(f)s"        # emacs
# COMMAND FOR EDITING A NEW APPOINTMENT (irrelevant with internal editor)
editnew = ''                            # internal editor
# editnew = "%(e)s -f + %(f)s"          # gvim
# editnew = "%(e)s +999999 %(f)s"       # emacs

# A TIMED EVENT WITH AN ALERT
# The system command to "play wav file" 
alert_play = 'play'
# The wave file to play
alert_wave = '/usr/share/sounds/KDE_Notify.wav'
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
# Why course numbers are spoken this way is a mystery to me.
alert_parsenums = 1

# The string provided for alert_other_message will be inserted in the 'Other
# Message' field when a new alert reminder is created. Such a message will not
# appear on the calendar but will be appended to 'Message' for alerts. 
alert_other_message = '%1'

# For example, with 
#   alert_display = 1
#   alert_sound = 2
#   alert_greeting = 1
#   alert_whom = 'Dan' 
#   alert_parsenums = 1
#   alert_other_message = '%1'
# a new alert reminder created with April 11, 2006 selected on the calendar
# would initially have the following entries:
#   Date: 11 Apr 2006
#   Time:
#   Duration:
#   Message:
#   Other Message: %1
#   Visual Alert: 2nd button (Pop-up Display) checked
#   Audible Alert: 3rd button (Spoken Message) checked
# After entering '10:50 +5' for Time, '1:15' for Duration and 'Economics 201'
# for Message, the resulting reminder would be
#   REM 11 Apr 2006 AT 10:50 +5 DUR 1:15 RUN wxremalert -d1 -s2 %"Economics 201%" %1%
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
# handcolor: fill color for the analog clock hands and tick marks 
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
#    handcolor = 'IVORY4'
#    bgcolor   = "IVORY3"
#    nfcolor   = "IVORY2"
#    fcolor    = "IVORY1"
# and, in fact, will override any individual color settings.

# borders: sunken (-1), flat (0) or raised (1)
# event and calendar borders
ec_border = -1
# status bar border
sb_border = 0

# show status bar with details of currently selected event.
showstatusbar = 0

# There are MANY other color settings which could be specified in this
# configuration file depending upon interest. 

##################################################################
# IT SHOULD NOT BE NECESSARY TO CHANGE ANYTHING BEYOND THIS POINT
import wx

# Set the default color family
colorfamily = "IVORY"
fcolor    = "%s1" % colorfamily
nfcolor   = "%s2" % colorfamily
bgcolor   = "%s3" % colorfamily
handcolor = "%s4" % colorfamily
defcolfam = colorfamily

from os.path import expanduser, isfile
# expand ~ in wxremindrc and the default reminders file
wxremindrc = expanduser("~/.wxremindrc")
default_reminders = expanduser(reminders)

# Get user customizations
msg = ''
rmsg = ''
emsg = ''
if isfile(wxremindrc):
    execfile(wxremindrc)
    if colorfamily != defcolfam:
        # user picked a new color family
        fcolor    = "%s1" % colorfamily
        nfcolor   = "%s2" % colorfamily
        bgcolor   = "%s3" % colorfamily
        handcolor = "%s4" % colorfamily
    msg += 'Using custom settings from ~/.wxremindrc.' 
    reminders = expanduser(reminders)
    if reminders != default_reminders:
        msg += "\nUsing the custom reminders file '%s'." % reminders
        rmsg = "\nCheck the reminders setting in '%s'," % wxremindrc
    else:
        msg += "\nUsing the default reminders file '%s'." % reminders
    if editor:
        msg += "\nUsing the custom editor '%s'." % editor
        emsg = "\nCheck the editor setting in '%s'," % wxremindrc
    else:
        msg += "\nUsing the default internal editor."

else:
    reminders = expanduser(reminders)
    msg += 'Could not find wxremindrc - using default settings.'

# if user instead picked new individual colors the new values will replace the
# defaults given above.

# we might have a new reminders file at this point
# expand ~ in the reminders file
error = 0
if not isfile(reminders):
    # fatal, we can't find the reminders file
    error = 1
    msg += "\nCannot find the reminders file '%s'!" % reminders
    msg += rmsg
if editor and not isfile(editor):
    # fatal, we can't find the custom editor
    error = 1
    msg += "\nCannot find the custom editor '%s'!" % editor
    msg += emsg
if festival and not isfile(festival):
    # fatal, we can't find festival
    error = 1
    msg += "\nCannot find the festival program '%s'!" % festival
    msg += emsg

# print msg
if error:
    app = wx.PySimpleApp()
    dlg = wx.MessageDialog(None, msg ,'wxRemConfig: Fatal Error', 
            wx.OK|wx.ICON_ERROR)
    dlg.ShowModal()
    dlg.Destroy()
    raise message

# set the hex version of bgcolor for the html page headers
app = wx.App()
cdb = wx.ColourDatabase()
cobj = cdb.FindColour(bgcolor)
rgbcolor = (cobj.Red(), cobj.Green(), cobj.Blue())
hcolor = '#%02x%02x%02x' % rgbcolor
