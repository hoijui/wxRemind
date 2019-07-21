import wx, wx.html
from wxRemConfig import hcolor, fcolor, nfcolor, bgcolor

msg = """
<html>
<body>
<table bgcolor="%s" width="100%%" cellspacing="0"
cellpadding="6" border="0">
<tr>
    <td valign="center" align="center"><b>Reminder Hints</b></td>
</tr>
</table>
<p><b>Creating new reminders</b></p>

<small>

<br> Select the target date in the calendar before pressing one of the following
keys to create the new reminder.
<center><table>
<tr><th>a</th> <td>a new timed reminder with an <em>alert</em>.</td></tr>
<tr><th>t</th> <td>a new <em>timed</em> reminder without an alert.</td></tr>
<tr><th>u</th> <td>a new <em>untimed</em> reminder.</ltd> </tr>
<tr><th>f</th> <td>a new <em>floating</em> reminder.</ltd> </tr>
</table></center>

<br>The selected date will automatically be placed in the date field and when
you're finished filling in the fields, you will be able to see the resulting
reminder in the event list. You can then select the new event and the status
bar will show you its details. If there's anything about it you don't like,
then you can press 'e' to bring up the editor with the cursor at the new
reminder. Pressing 'e' will even bring up a 'broken' reminder that doesn't show
up in the events list.</small>

<p><b>Date Field</b></p>
<small>
<center>
<table cols="2" border="0">
<tr><th>Date String</th><th align="left">Triggers</th></tr>
<tr><th>Empty</th><td>Every day</td></tr>
<tr><th>Tue Thu</th><td>Every Tuesday and Thursday</td></tr>
<tr><th>12</th><td>The 12th of every month</td></tr>
<tr><th>Apr 2006</th><td>Every day in April, 2006</td></tr>
<tr><th>Sat 1</th><td>The 1st Saturday in every month</td></tr>
<tr><th>Sat 1 Mar</th><td>The 1st Saturday in every March</td></tr>
<tr><th>-1</th><td>The last day of every month</td></tr>
<tr><th>Wed May</th><td>Every Wednesday in every May</td></tr>
<tr><th>Tue Thu 2006</th><td>Every Tuesday and Thursday in 2006</td></tr>
<tr><th>2005</th><td>Every day in 2005</td></tr>
<tr><th>18 May 2006 *14</th><td>Every two weeks starting 18 May 2006</td></tr>
<tr><th>Fri UNTIL 1 Jul 2006</th><td>Every Friday until 1 July 2006</td></tr>
<tr><th>5 May 2006 *1 +2 UNTIL 15 May 2006</th><td>Every day from May 5 until May 15 plus 2 days advance notice.</td></tr>
</table>
</center>
</small>


<p><b>Time Field</b></p>
<br>
<small>

Must begin with a 24 hour time in the format HH:MM. Can optionally be followed
by + and * strings.

<center>
<table cols="2" border="0">
<tr><th>Time String</th><th align="left">Triggers</th></tr>
<tr><th>13:00</th><td>1:00PM</td></tr>
<tr><th>10:00 +45 *20</th><td>9:15AM, 9:35AM, 9:55AM and 10:00AM</td></tr>
</table>
</center>
</small>
</p>

<p><b>Duration Field</b></p>
<br>
<small>
Must specify hours and minutes in the format H:MM.
<center>
<table cols="2" border="0">
<tr><th>Duration String</th><th align="left">Ends at start time plus</th></tr>
<tr><th>1:15</th><td>75 minutes</td></tr>
<tr><th>0:15</th><td>15 minutes</td></tr>
</table>
</center>
</small>

<p><b>Message / Other Message Fields</b></p>
<small>
<br>
'Message' is a required field for all types of reminders. 'Other Message' is
optional and, if present, will not appear in wxRemind's event list or other
remind "calendar" uses, but will appear in normal, non-calendar uses and thus
in alerts. For example,

<center>
<table>
<tr><td>Message: Dentist appointment</td></tr>
<tr><td>Other Message: %%1</td></tr>
</table>
</center>

<br>would appear on the relevant event list as <em>Dentist appointment</em> but
the message for an alert triggered 20 minutes before the appointment would be
<em>Dentist appointment 20 minutes from now</em>. See below for the use of %%1
and other time and date substitution strings. Technically, if 'Other Message'
were empty, the the reminder message would simply be <em>Dentist
appointment%%</em>.  The addition of the 'Other Message', on the other hand,
yields the message <em>%%"Dentist appointment%%" %%1%%</em>.
</small>

<p><b>Message Fields Date Substitution Strings</b></p>
<small>
<br>
<center>
<table cols="2" border="0">
<tr><th>String</th><th align="left">Replaced by</th></tr>
<tr><th>%%a</th><td>"on weekday, day month year", "tomorrow", "today", etc.</td></tr>
<tr><th>%%b</th><td>"in n days' time", "tomorrow", "today", etc.</td></tr>
</table>
</center>
<p>Also %%c ... %%z &mdash; see the remind man page.</p>
</small>

<p><b>Message Fields Time Substitution Strings</b></p>
<small>
<br>
<center>
<table cols="2" border="0">
<tr><th>String</th><th align="left">Replaced by</th></tr>
<tr><th>%%1</th><td>"now", "m minutes from now", "m minutes ago", etc.</td></tr>
<tr><th>%%2</th><td>"at hh:mmAM" or "at hh:mmPM"</td></tr>
<tr><th>%%3</th><td>"at hh:mm" in 24 hour format</td></tr>
</table>
</center>

<p>Also %%4 ... %%0 &mdash; see the remind man page.</p>
</small>

<p><b>Floating Reminders</b></p>
<small>
<br>
Date String: 15 Apr 2006
<br>Warning Days: 10
<br>Message String: File Taxes
<br>Resulting reminder: REM [float(2006,Apr,15,10)] MSG File Taxes%%

<center>
<table cols="5" border="0">
<tr><th>Today</th>
<th align="left">Calendar for</th><th>Display</th>
<th align="left">Calendar for</th><th>Display</th>
</tr>
<tr>
<th>Apr 2</th>
<th>Apr 5</th><td>File Taxes (in 10 days)</td>
<th>Apr 15</th><td>File Taxes (today)</td>
</tr>
<tr>
<th>Apr 6</th>
<th>Apr 6</th><td>File Taxes (in 9 days)</td>
<th>Apr 15</th><td>File Taxes (today)</td>
</tr>
<tr>
<th>Apr 14</th>
<th>Apr 14</th><td>File Taxes (tomorrow)</td>
<th>Apr 15</th><td>File Taxes (today)</td>
</tr>
<tr>
<th>Apr 16</th>
<th>Apr 16</th><td>File Taxes (yesterday)</td>
<th>Apr 15</th><td>File Taxes (today)</td>
</tr>
</table>
</center>
</small>

<p><b>Alert Reminders</b></p>
<small>
<br>

Are exactly like timed reminders but use 'RUN' rather than 'MSG' in the
reminder to invoke Remind (running in the background) to call wxremalert.  Thus
alerts will be triggered if Remind is running <em>whether or not wxRemind is
running</em>.  For example, with the following settings in ~/.wxremindrc

<table>
<tr><td>&nbsp;&nbsp;alert_display = 1</td></tr>
<tr><td>&nbsp;&nbsp;alert_sound = 2</td></tr>
<tr><td>&nbsp;&nbsp;alert_greeting = 1</td></tr>
<tr><td>&nbsp;&nbsp;alert_whom = 'Dan'</td></tr> 
<tr><td>&nbsp;&nbsp;alert_parsenums = 1</td></tr>
<tr><td>&nbsp;&nbsp;alert_other_message = '%%1'</td></tr>
</table>
a new alert reminder created with April 11, 2006 selected on the calendar
would initially have the following entries:
<table>
<tr><td>&nbsp;&nbsp;Date: 11 Apr 2006</td></tr>
<tr><td>&nbsp;&nbsp;Time:</td></tr>
<tr><td>&nbsp;&nbsp;Duration:</td></tr>
<tr><td>&nbsp;&nbsp;Message:</td></tr>
<tr><td>&nbsp;&nbsp;Other Message: %%1</td></tr>
<tr><td>&nbsp;&nbsp;Visual Alert: 2nd button (Pop-up Display) checked</td></tr>
<tr><td>&nbsp;&nbsp;Audible Alert: 3rd button (Spoken Message) checked</td></tr>
</table>
After entering '10:50 +5' for Time, '1:15' for Duration and 'Economics 201'
for Message, the resulting reminder would be
<table>
<tr><td>REM 11 Apr 2006 AT 10:50 +5 DUR 1:15 RUN wxremalert -d1 -s2 %%"Economics 201%%" %%1%%</td></tr>
</table>
The calendar for Apr 11 would then display
<table>
<tr><td>10:50AM - 12:05PM  Economics 201</td></tr>
</table>
and, at 10:45 on Apr 11 the following message would be spoken
<table>
<tr><td>"Good morning, Dan. The time is ten forty-five. Economics two oh one five
minutes from now."</td></tr>
</table>
and later, at 10:50:
<table>
<tr><td>"Good morning, Dan. The time is ten fifty. Economics two oh one now."</td></tr>
</table>

</small>
</body>
</html>
""" % (hcolor)

class Hints(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, 
                'wxRemind: Hints for creating reminders', 
                size=(620, 700))
        html = wx.html.HtmlWindow(self)
        html.SetPage(msg)
        html.SetBackgroundColour(fcolor)
        button = wx.Button(self, wx.ID_OK, "OK")
        button.SetDefault()
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(html, 1, wx.EXPAND | wx.ALL, 4)
        sizer.Add(button, 0, wx.ALIGN_CENTER | wx.BOTTOM, 4)
        self.SetSizer(sizer)
        self.SetBackgroundColour(bgcolor)
        self.Layout()

