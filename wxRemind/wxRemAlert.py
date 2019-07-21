#!/usr/bin/python
# $Id: wxRemAlert.py 14 2006-05-09 12:20:50Z dag $
import wx
import sys, os, getopt, datetime, re
from wxRemConfig import *

# alert types: old sd -> new t
types = {'00' : 0,
         '01' : 1,
         '10' : 2,
         '11' : 3,
         '20' : 4,
         '21' : 5}

def alert():
    global alert_type, alert_display
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'd:s:t:')
    except getopt.GetoptError:
        print 'options: -d[0,1] -s[0,1,2] -t[0,1,2,3]'
        sys.exit(2)

    # check for command line overrides
    alert_display = alert_sound = 0
    alert_display_set = alert_sound_set = alert_type_set = False
    for o, a in opts:
        if o == "-t":
            alert_type = int(a)
            alert_type_set = True
        elif o == "-d":
            alert_display = int(a)
            alert_display_set = True
        elif o == "-s":
            alert_sound = int(a)
            alert_sound_set = True

    if not alert_type_set:
        if alert_display_set or alert_sound_set:
            alert_type = types['%s%s' % (alert_sound, alert_display)]
        else:
            # make wave, display the system default
            alert_type = 3

    event_msg = ' '.join(args)
    spoken_msg = "%s " % event_msg
    if alert_type == 0:
        sys.exit(0)

    if alert_type in (2,3):
        os.system("%s %s" % (alert_play, alert_wave))
    elif alert_type in (4,5):
        if event_msg and alert_parsenums:
            # look for three consecutive digits preceeded by a non-digit and
            # followed by either a word boundary or a non-digit
            regex= re.compile(r'\D(\d{3,3})[\b\D]')
            nums = re.findall(regex, spoken_msg)
            if len(nums) > 0:
                for num in nums:
                    d0 = num[0]
                    d1 = num[1]
                    d2 = num[2]
                    if d1 == '0':
                        # replace the zero with an uppercase o
                        d1 = 'O'
                    # separate the leading digit from the following 2 digits
                    rep = "%s %s%s" % (d0,d1,d2)
                    # replace the original number
                    spoken_msg = re.sub(num, rep, spoken_msg)
                spoken_msg.strip()

        hours,minutes,seconds = \
                datetime.datetime.today().strftime("%H %M %S").split()

        hours = int(hours)
        minutes = int(minutes)
        seconds = int(seconds)

        if twelvehour:
            oclock = " o'clock"
            min = ""
            mins = ""
            spokenhours = ("twelve", "one", "two", "three", "four", "five",
            "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
            "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven")
        else:
            oclock = ""
            min = " minute"
            mins = " minutes"
            spokenhours = ("zero hours", "one hour", "two hours", "three hours",
                    "four hours", "five hours", "six hours", "seven hours",
                    "eight hours", "nine hours", "ten hours", "eleven hours",
                    "twelve hours", "thirteen hours", "fourteen hours", 
                    "fifteen hours", "sixteen hours", "seventeen hours",
                    "eighteen hours", "nineteen hours", "twenty hours",
                    "twenty one hours", "twenty two hours", "twenty three hours")

        # round current time up
        if seconds >= 50:
            minutes += 1
            if minutes >= 60:
                minutes = 0
                hours += 1
                if hours >= 24:
                    hours = 0

        message = ""

        if alert_greeting:
            try:
                Who = ", %s" % alert_whom
            except:
                Who = ''
            if hours < 12:
                message = "Good morning%s. " % Who
            elif hours < 18:
                message = "Good afternoon%s. " % Who
            else:
                message = "Good evening, %s. " % Who

        time = spokenhours[hours]

        if minutes == 0:
            time += oclock
        elif minutes == 1:
            if twelvehour:
                time += " O 1%s" % min
            else:
                time += " 1%s" % min
        elif minutes <= 9:
            if twelvehour:
                # replace the leading zero with an upper case o
                minutes = "O %d" % minutes 
            time += " %s%s" % (minutes, mins)
        else:
            time += " %s%s" % (minutes, mins)


        message += "The time is %s. %s" % (time, spoken_msg)

        if festival:
            cmd = "%s --tts" % festival
            try:
                si, so = os.popen2(cmd)
                si.write(message)
            finally:
                si.close()
                so.close()
        else:
            app = wx.PySimpleApp()
            dlg = wx.MessageDialog(None, 
    "The path to festival must be set in ~/.wxremindrc to use spoken alerts.",
                    'wxRemind alert', 
                    wx.OK | wx.STAY_ON_TOP | wx.ICON_ERROR)
            dlg.SetBackgroundColour(fcolor)
            retCode = dlg.ShowModal()
            dlg.Destroy()

    if alert_type in (1,3,5):
        app = wx.PySimpleApp()
        dlg = wx.MessageDialog(None, "%s" % event_msg, 'wxRemind alert', 
                                wx.STAY_ON_TOP | wx.OK | wx.ICON_INFORMATION)
        dlg.SetBackgroundColour(fcolor)
        retCode = dlg.ShowModal()
        dlg.Destroy()

if __name__ == "__main__":
    alert() 

