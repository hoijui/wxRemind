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
<p><b>Date Strings</b></p>

<p>
<small>
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
</small>
</p>

<p><b>Floating Reminders</b></p>
<small>
<p>
Date String: 15 Apr 2006
<br>Warning Days: 10
<br>Message String: File Taxes
<br>Resulting reminder: REM [float(2006,Apr,15,10)] MSG File Taxes%%
</p>

<br>
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
</small>

<p><b>Time Strings</b></p>
<br>
<small>
<table cols="2" border="0">
<tr><th>Time String</th><th align="left">Triggers</th></tr>
<tr><th>13:00</th><td>1:00PM</td></tr>
<tr><th>10:00 +45 *20</th><td>9:15AM, 9:35AM, 9:55AM and 10:00AM</td></tr>
</table>
</small>
</p>

<p><b>Duration Strings</b></p>
<br>
<small>
<table cols="2" border="0">
<tr><th>Duration String</th><th align="left">Ends at start time plus</th></tr>
<tr><th>1:15</th><td>75 minutes</td></tr>
<tr><th>0:15</th><td>15 minutes</td></tr>
</table>
</small>

<p><b>Message</b> and <b>Other Message</b></p>
<small>
<br>
'Message' is a required field for all types of reminders. 'Other Message' is
optional and, if present, will not appear in wxRemind's event list or other
remind "calendar" uses, but will appear in normal, non-calendar uses and thus
in alerts. For example,

<p>
Message: Dentist appointment
<br>Other Message: %%1
</p>

<p>would appear on the relevant event list as <em>Dentist appointment</em> but
the message for an alert triggered 20 minutes before the appointment would be
<em>Dentist appointment 20 minutes from now</em>. See below for the use of %%1
and other time and date substitution strings. Technically, if 'Other Message'
were empty, the the reminder message would simply be <em>Dentist
appointment%%</em>.  The addition of the 'Other Message', on the other hand,
yields the message <em>%%"Dentist appointment%%" %%1%%</em>.</p>
</small>

<p><b>Date Message Substitution Strings</b></p>
<small>
<br>
<table cols="2" border="0">
<tr><th>String</th><th align="left">Replaced by</th></tr>
<tr><th>%%a</th><td>"on weekday, day month year", "tomorrow", "today", etc.</td></tr>
<tr><th>%%b</th><td>"in n days' time", "tomorrow", "today", etc.</td></tr>
</table>

<p>Also %%c ... %%z &mdash; see the remind man page.</p>
</small>

<p><b>Time Message Substitution Strings</b></p>
<small>
<br>
<table cols="2" border="0">
<tr><th>String</th><th align="left">Replaced by</th></tr>
<tr><th>%%1</th><td>"now", "m minutes from now", "m minutes ago", etc.</td></tr>
<tr><th>%%2</th><td>"at hh:mmAM" or "at hh:mmPM"</td></tr>
<tr><th>%%3</th><td>"at hh:mm" in 24 hour format</td></tr>
</table>

<p>Also %%4 ... %%0 &mdash; see the remind man page.</p>
<p>
</small>
</body>
</html>
""" % (hcolor)

class Hints(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, 
                'wxRemind: Hints for creating reminders', 
                size=(600, 700))
        html = wx.html.HtmlWindow(self)
        html.SetPage(msg)
        html.SetBackgroundColour(fcolor)
        button = wx.Button(self, wx.ID_OK, "OK")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(html, 1, wx.EXPAND | wx.ALL, 4)
        sizer.Add(button, 0, wx.ALIGN_CENTER | wx.BOTTOM, 4)
        self.SetSizer(sizer)
        self.SetBackgroundColour(bgcolor)
        self.Layout()

