# $Id: wxRemAbout.py 8 2006-05-08 15:14:25Z dag $
import wx.html
from wxRemVersion import *

class About(wx.Dialog):
    text = """
<html>
<body>
<table bgcolor="#BBDB88" width="100%%" cellspacing="0"
cellpadding="6" border="0">
<tr>
    <td valign="center" align="center"><b>wxRemind</b></td>
</tr>
</table>
<small>
<center>
<em>%s</em>
</center>

<p><em>wxRemind</em> is a  graphical front-end to <em>Remind</em>, a remarkably
sophisticated calendar and alarm system.  It is similar to <em>Wyrd</em>, a
curses based front-end to remind but is based on <em>wxPython</em> rather than
curses. If there are things you like about wxRemind, they are almost certainly
due either to David Skoll (remind), to Paul Pelzl (wyrd), or to the folks
responsible for wxPython.</p>

<center>
<table border="0">
<tr> <th>remind</th>   <td>http://www.roaringpenguin.com/penguin/open_source_remind.php</td></tr>
<tr> <th>wyrd</th>     <td>www.eecs.umich.edu/~pelzlpj/wyrd</td> </tr>
<tr> <th>wxPython</th> <td>www.wxpython.org</td> </tr>
<tr> <th>wxRemind</th> <td>http://freshmeat.net/projects/wxrem/</td></tr>
<tr> <th>FSW</th><td>www.gnu.org/licenses/gpl.html</td></tr>
</table>
</center>

<p>This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the Free
Software Foundation (FSW); either version 2 of the License, or (at your option)
any later version. This program is provided in the hope that it will be useful,
but <em>without any warranty</em>; without even the implied warranty of
<em>merchantability</em> or <em>fitness for a particular purpose</em>.  See the
GNU General Public License for more details.</p>

<p><center>
Copyright (c) 2006 Daniel A. Graham &lt;daniel.graham@duke.edu&gt;
</center></p>
</small>
</body>
</html>
""" % (wxRemVersion)

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, 'About wxRemind',
                          size=(550, 540) )

        html = wx.html.HtmlWindow(self)
        html.SetPage(self.text)
        button = wx.Button(self, wx.ID_OK, "OK")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(html, 1, wx.EXPAND|wx.ALL, 5)
        sizer.Add(button, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        self.SetSizer(sizer)
        self.Layout()
