#!/usr/bin/python
# $Id: wxRemAlert.py 14 2006-05-09 12:20:50Z dag $
import wx
import sys, os, getopt, datetime, re
from wxRemConfig import * 

def alert():
    global alert_sound, alert_display
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'd:s:')
    except getopt.GetoptError:
        print 'options: -d[0,1] -s[0,1,2]'
        sys.exit(2)

    # check for command line overrides
    for o, a in opts:
        if o == "-d":
            alert_display = int(a)
        elif o == "-s":
            alert_sound = int(a)

    event_msg = ' '.join(args)

    if alert_sound == 1:
        os.system(alert_soundcmd)
    elif alert_sound == 2:
        if event_msg and alert_parsenums:
            event_msg = "%s " % event_msg
            # look for three consecutive digits preceeded by a non-digit and
            # followed by either a word boundary or a non-digit
            regex= re.compile(r'\D(\d{3,3})[\b\D]')
            nums = re.findall(regex, event_msg)
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
                    event_msg = re.sub(num, rep, event_msg)
                event_msg.strip()

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


        message += "The time is %s. %s" % (time, event_msg)

        cmd = "/usr/bin/festival --tts"
        try:
            si, so = os.popen2(cmd)
            si.write(message)
        finally:
            si.close()
            so.close()

    if alert_display:
        app = wx.PySimpleApp()
        dlg = wx.MessageDialog(None, "%s" % event_msg, 'wxRemind alert', 
                                wx.STAY_ON_TOP | wx.OK | wx.ICON_INFORMATION)
        dlg.SetBackgroundColour(fcolor)
        retCode = dlg.ShowModal()
        dlg.Destroy()

if __name__ == "__main__":
    alert() 

