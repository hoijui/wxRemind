# $Id: wxRemHelp.py 4 2006-05-08 13:27:14Z dag $
import wx.html
from wxRemConfig import hcolor, fcolor, nfcolor, bgcolor

class Help(wx.Dialog):
    text = '''
<html>
<body>
<table bgcolor="%s" width="100%%" cellspacing="0"
cellpadding="6" border="0">
<tr>
    <td valign="center" align="center"><b>wxRemind Usage</b></td>
</tr>
</table>
<small>
<table border="0">
<tr><th>F1</th> <td>About wxRemind.</td></tr>
<tr><th>?</th> <td>Usage information (this page).</td></tr>
<tr><th>h</th> <td>Hints for creating reminders.</td></tr>
<tr><th>Space</th> <td> Switch to the current date.</td></tr>
<tr><th>Tab</th> <td> Toggle focus between the calendar and event list.</td></tr>
<tr><th>Arrow Left/Right</th> <td> In calendar, previous/next day.</td></tr>
<tr><th>Arrow Up/Down</th> <td> In calendar, previous/next week.
In event list, previous/next event.</td> </tr>
<tr><th>Page Up/Down</th> <td> In calendar, previous/next month.
In event list, previous/next page.</td></tr>
<tr><th>Enter</th> <td> In event list, edit the selected event.</td></tr>
<tr><th>c</th> <td> Display/print postscript calendar for selected month. (requires ggv)</td></tr>
<tr><th>e</th> <td> Open the default reminders file for editing.</td></tr>
<tr><th>a</th> <td> Create a new timed reminder with an <em>alert</em>.</td></tr>
<tr><th>t</th> <td> Create a new <em>timed</em> reminder without an alert.</td></tr>
<tr><th>u</th> <td> Create a new <em>untimed</em> reminder.</ltd> </tr>
<tr><th>f</th> <td> Create a new <em>floating</em> reminder.</ltd> </tr>
<tr><th>/</th> <td> Begin case-insensitive search from selected date.</td></tr>
<tr><th>n</th> <td> Search for next occurance.</td></tr>
<tr><th>R</th> <td> Refresh reminders. (Done automatically after editing.)</td></tr>
<tr><th>C-Q</th> <td> Exit.</td></tr>
</table>
</small>
</body>
</html>
''' % (hcolor)
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, 'wxRemind Usage',
                          size=(580, 580))
        html = wx.html.HtmlWindow(self)
        html.SetPage(self.text)
        html.SetBackgroundColour(fcolor)
        button = wx.Button(self, wx.ID_OK, "OK")
        button.SetDefault()
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(html, 1, wx.EXPAND|wx.ALL, 5)
        sizer.Add(button, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        self.SetSizer(sizer)
        self.SetBackgroundColour(fcolor)
        self.Layout()
