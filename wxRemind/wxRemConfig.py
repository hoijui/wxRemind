# Configuration settings for wxRemind
# $Id: wxRemConfig.py 14 2006-05-09 12:20:50Z dag $

# REMINDERS
reminders = '/home/dag/Documents/Reminders/reminders'

# TIME DISPLAY 12 hour (1) or 24 hour (0)
twelvehour = 1

# MONTHLY CALENDAR ORIENTATION landscape (1) or portrait (0)
landscape = 1

# show splashscreen on startup for this many seconds or 0 for not at all
showsplash = 2

# EDITOR
editor = "/usr/local/bin/gvim"
# editor = "/usr/bin/emacs"

# EDIT COMMAND SUBSTITUTIONS
# %(e)s -> the editor named above
# %(n)s -> line number to edit
# %(f)s -> file name
# COMMAND FOR EDITING AN OLD APPOINTMENT
editold = "%(e)s -f +%(n)s %(f)s"        # gvim 
# editold = "%(e)s +%(n)s %(f)s"         # emacs

# COMMAND FOR EDITING A NEW APPOINTMENT (the last line in the file)
editnew = "%(e)s -f + %(f)s"          # gvim
# editnew = "%(e)s +999999 %(f)s"     # emacs

# A TIMED EVENT WITH AN ALERT
# The system command to "play wav file" 
alert_soundcmd = 'play /usr/share/sounds/KDE_Notify.wav'
# ALERT DEFAULTS 
# Display the alter box (1) or not (0)
alert_display = 1
# Silent (0), execute alert_soundcmd (1) or play spoken message (2)
alert_sound = 2
# Add a time appropriate greeting to spoken message, e.g., "Good morning"
alert_greeting = 1
# Add a name if non-null to the spoken greeting, e.g, "Good morning, Dan"
alert_whom = 'Dan'
# Replace all 3-digit numbers in msg with spoken equivalents, e.g., Replace
# '201' with '2 O1' where O is an uppercase o) and '385' with '3 85'. Thus
# '201' would be spoken as 'two oh one' and '385' as 'three eighty-five'.
# Why course numbers are spoken this way is a mystery to me.
alert_parsenums = 1

# For example, with 
#   alert_display = 1
#   alert_sound = 1
#   alert_greeting = 1
#   alert_whom = 'Dan' 
# and reminder:
#   REM 11 Apr 2006 AT 10:50 +5 DUR 1:15 RUN wxremalert -d0 -s2 %"Economics 201%" %1%
# the calendar for Apr 11 would display
#   10:50AM - 12:05PM  Economics 201
# Then, at 10:45 on Apr 11 the following message would be spoken (-s2 overrides
# the default alert_sound) but not displayed (-d0 overrides the default
# alert_display):
#   "Good morning, Dan. The time is ten forty-five. Economics two oh one five
#    minutes from now."
# and at 10:50 the the following message would be spoken:
#   "Good morning, Dan. The time is ten fifty. Economics two oh one now."s

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

# The adjustment (horizontal, vertical) to the size of the calendar: 
calsizeadj = (16, -4) 

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

# for the analog clock hands
handcolor = 'FIREBRICK'

# for the calendar
holidaycolor = 'BLACK'
headercolor = 'NAVYBLUE'
# headercolor = 'FIREBRICK'

# BACKGROUND COLORS
# bgcolor: The general background color.
# nfcolor: The background color for the event list and calendar, whichever has
# the focus.
# fcolor:  The background color for the event list and calendar, whichever does
# not have the focus.

# There are two ways of specifying these background colors. The first is simply
# to specify these colors directly, e.g., 
# bgcolor = "GRAY90"
# nfcolor = "GRAY94"
# fcolor  = "GRAY99"

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
#    bgcolor = "IVORY3"
#    nfcolor = "IVORY2"
#    fcolor  = "IVORY1"

# The advantage of the family approach is that the selected colors
# automatically blend well and help indentify the window with the focus. 

# borders: sunken (-1), flat (0) or raised (1)
# event and calendar borders
ec_border = -1
# status bar border
sb_border = 0

# show status bar with details of currently selected event.
showstatusbar = 0

# There are MANY other color settings which could be specified in this
# configuration file depending upon interest. 

# Don't change anything beyond this point
# Set the default color family
colorfamily = "IVORY"
fcolor  = "%s1" % colorfamily
nfcolor = "%s2" % colorfamily
bgcolor = "%s3" % colorfamily
defcolfam = colorfamily

from os.path import expanduser, isfile
# expand ~ in the default wxremindrc file
wxremindrc = expanduser("~/.wxremindrc")
# Get user customizations
if isfile(wxremindrc):
    execfile(wxremindrc)
    if colorfamily != defcolfam:
        # user picked a new color family
        fcolor  = "%s1" % colorfamily
        nfcolor = "%s2" % colorfamily
        bgcolor = "%s3" % colorfamily

# if user instead picked new individual colors the new values will replace the
# defaults given above.

# we might have a new reminders file at this point
# expand ~ in the reminders file
reminders = expanduser(reminders)
if not isfile(reminders):
    # trouble, we can't find the reminders file
    raise NameError, "Cannot locate %s." % reminders


# set the hex version of bgcolor
import wx
app = wx.App()
cdb = wx.ColourDatabase()
cobj = cdb.FindColour(bgcolor)
rgbcolor = (cobj.Red(), cobj.Green(), cobj.Blue())
hcolor = '#%02x%02x%02x' % rgbcolor
