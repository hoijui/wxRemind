#!/usr/bin/python
(revname, revnumber, revdate, revtime) = \
"$Id: wxRemind.py 6 2006-05-08 14:52:05Z dag $".split()[1:5]

import os
import wx
import wx.calendar
import datetime
import linecache
import analogclock as ac 
import wx.lib.mixins.listctrl  as  listmix
from wxRemHelp import Help
from wxRemAbout import About
from wxRemHints import Hints
import wxRemEdit

# CONFIGURATION
from wxRemConfig import *
if ec_border == -1:
    BORDER = wx.SUNKEN_BORDER
elif ec_border == 0:
    BORDER = wx.NO_BORDER
elif ec_border == 1:
    BORDER = wx.RAISED_BORDER

# set the border styles
if sb_border == -1:
    SBORDER = wx.SB_NORMAL
elif sb_border == 0:
    SBORDER = wx.SB_FLAT
elif sb_border == 1:
    SBORDER = wx.SB_RAISED

sb_string = "Press F1 for information about wxRemind or ? for help."

# Prepare the replacment hash for later updating.
rephash = {'e' : editor, 'f' : None, 'n' : None, 
    'y' : None, 'm' : None, 'd' : None}
# Later when editold is called, for example, '%(e)s' will be replaced by
# rephash['e'], '%(f)s' by rephash['f'] and so forth.

import wxRemData
Data = wxRemData.RemData()

class MyClock(ac.AnalogClock):
    # Keep the clock from taking the focus
    def AcceptsFocus(*args, **kwargs):
        return False

class MyListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)

    def AcceptsFocus(*args, **kwargs):
        return True

class MyCalCtrl(wx.calendar.CalendarCtrl):
    # Let the calendar to take the focus
    def AcceptsFocus(*args, **kwargs):
        return True

class MyFrame(wx.Frame):
    def __init__(self):
        self.data = []
        self.calattr = []
        self.calfocus = 1
        fontfam = wx.DEFAULT
        bfont = wx.Font(basefontsize + buttonfontadj, fontfam, 
                wx.NORMAL, wx.NORMAL)
        # lfont = wx.Font(listfontsize, wx.TELETYPE, wx.NORMAL, wx.NORMAL, 
                # faceName=listfontfacename)
        lfont = wx.Font(basefontsize + listfontadj, fontfam, 
                wx.NORMAL, wx.NORMAL)
        dfont = wx.Font(basefontsize + datefontadj, fontfam,
                wx.NORMAL, wx.NORMAL)
        sfont = wx.Font(basefontsize + statusfontadj, fontfam,
                wx.NORMAL, wx.NORMAL)
        cfont = wx.Font(basefontsize + calendarfontadj, wx.DEFAULT,
                wx.NORMAL, wx.NORMAL)
        wx.Frame.__init__(self, None, -1, 'wxRemind', 
                size=(740,420))
        self.SetBackgroundColour(bgcolor)

        # The top (selected date) bar
        # self.datebar = wx.TextCtrl(self, -1, "", size=(-1,-1), 
                # style = wx.TE_READONLY | BORDER)
        self.datebar = wx.TextCtrl(self, -1, "DateBar", size=(-1,-1), 
                style = BORDER | wx.TE_CENTRE)
        self.datebar.SetBackgroundColour(nfcolor)
        self.datebar.SetFont(dfont)

        # The bottom (selected event details) bar
        self.detailbar = wx.StaticText(self, -1, "", size=(-1,-1),
                style = wx.NO_BORDER | wx.ST_NO_AUTORESIZE)
        # self.detailbar.SetBackgroundColour(bgcolor)
        self.detailbar.SetFont(sfont)

        # The today button
        self.tdy = wx.Button(self, -1, '', style = wx.NO_BORDER)
        self.tdy.SetFont(bfont)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.tdy)
        self.tdy.Bind(wx.EVT_CHAR, self.OnChar)
        self.tdy.SetBackgroundColour(bgcolor)
        self.tdy.SetToolTipString("Show events for today.")

        # The event list
        self.lc = MyListCtrl(self, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | 
                wx.LC_NO_HEADER | wx.WANTS_CHARS | BORDER )
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.lc) 
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated, self.lc) 
        self.lc.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.lc.Bind(wx.EVT_CHAR, self.OnChar)
        self.lc.SetFont(lfont)
        self.lc.SetBackgroundColour(bgcolor)
        self.lc.InsertColumn(0, 'Start')
        self.lc.InsertColumn(1, 'Interval')
        self.lc.InsertColumn(2, 'End')
        self.lc.InsertColumn(3, 'Message')
        self.lc_id = self.lc.GetId()

        # The calendar
        self.cal = MyCalCtrl(self, -1, wx.DateTime_Now(), size = (-1,-1),
                style = wx.calendar.CAL_SHOW_HOLIDAYS | wx.WANTS_CHARS |
                BORDER | wx.calendar.CAL_SEQUENTIAL_MONTH_SELECTION)
        self.cal.SetFont(cfont)
        # Hack to enlarge calendar window in a fontsize dependent way
        if calsizeadj[0] or calsizeadj[1]:
            size = self.cal.GetSize() + calsizeadj
            self.cal.Destroy()
            self.cal = MyCalCtrl(self, -1, wx.DateTime_Now(), size = size,
                    style = wx.calendar.CAL_SHOW_HOLIDAYS | wx.WANTS_CHARS |
                    BORDER | wx.calendar.CAL_SEQUENTIAL_MONTH_SELECTION)
            self.cal.SetFont(cfont)
        self.cal.SetHeaderColours(headercolor,fcolor)
        self.cal.SetHolidayColours(holidaycolor,fcolor)
        self.Bind(wx.calendar.EVT_CALENDAR_SEL_CHANGED, self.OnCalSelected, 
                id=self.cal.GetId())
        self.cal.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.cal.Bind(wx.EVT_CHAR, self.OnChar)
        self.cal_id = self.cal.GetId()

        # The analog clock
        self.clk = MyClock(self, size=(160+basefontsize,160+basefontsize), 
                hoursStyle=ac.TICKS_SQUARE, clockStyle=ac.SHOW_HOURS_TICKS| 
                ac.SHOW_HOURS_HAND | ac.SHOW_MINUTES_HAND| ac.SHOW_SECONDS_HAND)
        self.clk.SetTickSize(16)
        self.clk.SetTickFillColour(holidaycolor)
        self.clk.SetHandFillColour(handcolor)
        self.clk.SetFaceBorderColour(bgcolor)
        self.clk.SetHandBorderColour(handcolor)
        self.clk.SetBackgroundColour(bgcolor)
        self.clk.SetFaceFillColour(bgcolor)

        # Key bindings and focus
        self.clk.Bind(wx.EVT_CHAR, self.OnChar)
        self.clk.Bind(wx.EVT_MOUSE_EVENTS, self.Focus('res'))
        self.datebar.Bind(wx.EVT_CHAR, self.OnChar)
        self.datebar.Bind(wx.EVT_MOUSE_EVENTS, self.Focus('res'))
        self.detailbar.Bind(wx.EVT_CHAR, self.OnChar)
        self.detailbar.Bind(wx.EVT_MOUSE_EVENTS, self.Focus('res'))

        # The layout
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1  = wx.BoxSizer(wx.HORIZONTAL)
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox1.Add(self.datebar, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 4)
        vbox1.Add(self.lc, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 4)
        vbox2.Add(self.cal, 0, wx.EXPAND | wx.ALIGN_CENTER |
                wx.TOP | wx.RIGHT | wx.BOTTOM, 4)
        vbox2.Add(self.tdy, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | 
                wx.TOP | wx.RIGHT | wx.BOTTOM, 4)
        vbox2.Add(self.clk, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL |
                wx.TOP | wx.RIGHT | wx.BOTTOM, 4)
        hbox1.Add(vbox1, 1, wx.EXPAND)
        hbox1.Add(vbox2, 0, wx.EXPAND)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        vbox3 = wx.BoxSizer(wx.VERTICAL)
        vbox3.Add(self.detailbar, 0, wx.EXPAND | wx.ALL, 4)
        hbox2.Add(vbox3, 1, wx.EXPAND)
        vbox.Add(hbox1, 1, wx.EXPAND)
        vbox.Add(hbox2, 0, wx.EXPAND)
        self.SetSizer(vbox)

        # Show events for the current date.
        self.today = None
        self.Today()
        self.showDay(self.selday[0], self.selday[1], self.selday[2])

    def FormatDate(self,y,m,d):
        y,m,d = map(int, (y,m,d))
        date = datetime.date(y,m,d)
        day = int(date.strftime("%d"))
        fmtstr = "%%a,  %d %%b %%Y  " % day
        return date.strftime(fmtstr)

    def OnClick(self, event):
        self.Today()

    def Today(self):
        today = datetime.date.today()
        if not self.today or self.today != today:
            # reset data to show 'current date only' events today
            Data.getMonths()
        self.today = today
        y,m,d = self.today.strftime("%Y %m %d").split()
        self.selday = (y,m,d)
        self.tdy.SetLabel("%s " % self.FormatDate(y,m,d))
        self.cal.SetDate(wx.DateTime_Now())
        self.showDay(self.selday[0], self.selday[1], self.selday[2])
        self.Focus('cal')

    def OnMonthChange(self, y, m):
        y, m = map(int, (y,m))
        busy = Data.getMonthlyDurations(y,m)
        for i in range(1,32):
            self.cal.ResetAttr(i)
        for day in busy.keys():
            minutes = busy[day]
            attr = wx.calendar.CalendarDateAttr()
            if minutes < busy0[0]:
                attr.SetTextColour('BLACK')
                self.cal.SetAttr(day, attr)
            elif minutes < busy1[0]:
                attr.SetTextColour(busy0[1])
                self.cal.SetAttr(day, attr)
            elif minutes < busy2[0]:
                attr.SetTextColour(busy1[1])
                self.cal.SetAttr(day, attr)
            elif minutes < busy3[0]:
                attr.SetTextColour(busy2[1])
                self.cal.SetAttr(day, attr)
            elif minutes < busy4[0]:
                attr.SetTextColour(busy3[1])
                self.cal.SetAttr(day, attr)
            else:
                attr.SetTextColour(busy4[1])
                self.cal.SetAttr(day, attr)

    def OnCalSelected(self, event):
        y,m,d = event.GetDate().Format("%Y %m %d").split()
        self.showDay(y, m, d)

    def OnItemActivated(self, event):
        # Open the relevant file at the appropriate line number for editing.
        self.currentItem = event.m_itemIndex
        # only call editor if we have both a file and a line number - skip
        # "Nothing scheduled" lines in the event list.
        if self.data[self.currentItem][3]:
            rephash['f'] = self.data[self.currentItem][4]
            rephash['n'] = self.data[self.currentItem][5]
            editlist = (editold % rephash).split()
            os.spawnv(os.P_WAIT, editor, editlist)
            self.Refresh()

    def OnItemSelected(self, event):
        # Show the relevant reminder in the status bar.
        self.currentItem = event.m_itemIndex
        if self.data[self.currentItem][4]:
            file = self.data[self.currentItem][4]
            line = int(self.data[self.currentItem][5])
            reminder = linecache.getline(file,line).strip()
            self.detailbar.SetLabel(reminder)

    def OnAbout(self, event):
        # show the about page
        dlg = About(self)
        dlg.ShowModal()
        dlg.Destroy()

    def OnHelp(self, event):
        # show the help page
        dlg = Help(self)
        dlg.ShowModal()
        dlg.Destroy()

    def OnHints(self, event):
        # show the hints page
        dlg = Hints(self)
        dlg.ShowModal()
        dlg.Destroy()


    def OnMonth(self):
        # show the postscript calendar for the month
        if landscape:
            ls = '-l'
        else:
            ls = ''
        date = datetime.date(self.selday[0],
                self.selday[1],self.selday[2]).strftime("%b %Y")
        command = "remind -p %s %s | rem2ps %s | ggv -" % (reminders, date, ls)
        os.system(command)

    def OnSetFocus(self, event):
        # called by EVT_SET_FOCUS. sets bgcolor to match focus
        w = wx.Window_FindFocus()
        if w:
            curr_id = w.GetId()
            if curr_id == self.cal_id:
                self.Focus('cal')
            elif curr_id == self.lc_id:
                self.Focus('lc')

    def Focus(self, w=''):
        # Called with an argument sets appropriate focus, else toggles focus.
        if w == 'cal':
            self.setFocus('cal')
        elif w == 'lc':
            self.setFocus('lc')
        elif w == 'res':
            if self.calfocus:
                self.setFocus('cal')
            else:
                self.setFocus('lc')
        else: 
            if self.calfocus:
                self.setFocus('lc')
            else:
                self.setFocus('cal')

    def setFocus(self, target):
        if target == 'cal':
            self.cal.SetFocus()
            self.calfocus = 1
            self.detailbar.SetLabel(sb_string)
            self.cal.SetHeaderColours(headercolor,fcolor)
            self.cal.SetBackgroundColour(fcolor)
            self.datebar.SetBackgroundColour(nfcolor)
            self.lc.SetBackgroundColour(nfcolor)
            for day in range(1,32):
                attr = self.cal.GetAttr(day)
                if attr and attr.HasTextColour():
                    tc = attr.GetTextColour()
                    attr = wx.calendar.CalendarDateAttr()
                    attr.SetTextColour(tc)
                    attr.SetBackgroundColour(fcolor)
                    self.cal.SetAttr(day, attr)
                else:
                    attr = wx.calendar.CalendarDateAttr()
                    attr.SetBackgroundColour(fcolor)
                    self.cal.SetAttr(day,attr)
            if self.lc.GetSelectedItemCount():
                self.lc.SetItemState(self.currentItem, 
                        0, wx.LIST_STATE_SELECTED)
        elif target == 'lc':
            self.lc.SetFocus()
            self.calfocus = 0
            self.cal.SetHeaderColours(headercolor,nfcolor)
            self.cal.SetBackgroundColour(nfcolor)
            self.datebar.SetBackgroundColour(fcolor)
            self.lc.SetBackgroundColour(fcolor)
            for day in range(1,32):
                attr = self.cal.GetAttr(day)
                if attr and attr.HasTextColour():
                    tc = attr.GetTextColour()
                    attr = wx.calendar.CalendarDateAttr()
                    attr.SetTextColour(tc)
                    attr.SetBackgroundColour(nfcolor)
                    self.cal.SetAttr(day, attr)
                else:
                    attr = wx.calendar.CalendarDateAttr()
                    attr.SetBackgroundColour(nfcolor)
                    self.cal.SetAttr(day,attr)
            if not self.lc.GetSelectedItemCount():
                self.lc.SetItemState(self.lc.GetTopItem(), 
                        wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)

    def showDay(self,y,m,d):
        # Show the events for the specified day in the event list.
        y, m, d= map(int, (y,m,d))
        self.data = Data.getDay(y,m,d)
        if m != self.selday[1] or y != self.selday[0]:
            # the month has changed
            self.OnMonthChange(y,m)
        self.selday = (y,m,d) 
        date = datetime.date(y,m,d)
        self.lc.DeleteAllItems()
        for i in range(len(self.data)):
            index = self.lc.InsertStringItem(i, self.data[i][0])
            self.lc.SetStringItem(index, 0, self.data[i][0])
            self.lc.SetStringItem(index, 1, self.data[i][1])
            self.lc.SetStringItem(index, 2, self.data[i][2])
            self.lc.SetStringItem(index, 3, self.data[i][3])
            self.lc.SetItemData(index, i)
        self.lc.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.lc.SetColumnWidth(1, 14)
        self.lc.SetColumnWidth(2, wx.LIST_AUTOSIZE)
        self.lc.SetColumnWidth(3, wx.LIST_AUTOSIZE)
        self.datebar.SetValue(self.FormatDate(y,m,d))
        self.Focus('cal')
        self.detailbar.SetLabel(sb_string)

    def OnChar(self, event):
        keycode = event.GetKeyCode()
        # print "OnChar: %s" % str(keycode)
        if keycode == 9:            # tab
            self.Focus()
        elif keycode == 17:         # Ctrl-Q quit
            self.OnQuit()
        elif keycode == 32:         # space
            self.Today()
        elif keycode == 47:         # /: search
            self.OnSearch(event)
        elif keycode == 63:         # ? Show Help box
            self.OnHelp(event)
        # elif keycode == 81:         # Q quit
            # self.OnQuit()
        elif keycode == 82:         # R refresh
            self.Refresh()
        elif keycode == 97:         # a: alert event
            self.newEvent('a')
        elif keycode == 99:         # C show html calendar for month 
            self.OnMonth()
        elif keycode == 101:        # e: edit any event
            self.Edit(event)
        elif keycode == 102:        # f: floating reminder
            self.newEvent('f')
        elif keycode == 104:        # h: show hints
            self.OnHints(event)
        elif keycode == 110:        # n: search next
            self.findNext(event)
        elif keycode == 116:        # t (timed event)
            self.newEvent('t')
        elif keycode == 117:        # u untimed event
            self.newEvent('u')
        elif keycode == 342:        # F1 Show About box
            self.OnAbout(event)
        else:
            event.Skip()


    def newEvent(self, type):
        # Create a new event, append it to the reminders file and open the
        # editor on the last line of this file.
        y,m,d = map(int, self.selday)
        date = datetime.date(y, m, d)
        datefmt = "%d %s" % (d, date.strftime("%b %Y"))
        data = { "date" : datefmt }
        dlg = wxRemEdit.MyDialog(data, type)
        dlg.ShowModal()
        dlg.Destroy()
        if data.has_key('msg') and data['msg'] != '':
            # user did not press cancel
            if data.has_key('dur') and data['dur']:
                data['dur'] = "DUR %s" % data['dur']
            else:
                data['dur'] = ''
            if data.has_key('omsg') and data['omsg']:
                data['msg'] = '%%"%s%%" %s' % (data['msg'], data['omsg'])
            else:
                data['msg'] = '%%"%s%%"' % data['msg']
            if type == 'a':
                # convert radio button index to switch string 
                s = int(data['alert'])
                if s == 0:
                    data['alert'] = '-d1 -s1'
                elif s == 1:
                    data['alert'] = '-d1 -s0'
                elif s == 2:
                    data['alert'] = '-d1 -s2'
                else:
                    data['alert'] = '-d0 -s2'
                rem = 'REM %(date)s AT %(time)s %(dur)s RUN wxremalert ' % data
                rem += '%(alert)s %(msg)s%%' % data
            elif type == 'u':
                rem = 'REM %(date)s MSG %(msg)s%%' % data
            elif type == 't':
                rem = 'REM %(date)s AT %(time)s %(dur)s MSG %(msg)s%%' % data
            elif type == 'f':
                d,m,y = data['date'].split()
                data['date'] = "[float(%s,%s,%s,%s)]" % (y,m,d, data['warn'])
                rem = 'REM %(date)s MSG %(msg)s%%' % data
            if rem:
                rephash['f'] = "%s" % reminders
                cmd = "echo '%s' >> %s" % (rem, reminders)
                os.system(cmd)
                editlist = (editnew % rephash).split()
                # print editlist
                os.spawnv(os.P_WAIT, editor, editlist)
                self.Refresh()

    def Edit(self,evt):
        # Open the reminders file for editing.
        rephash['f'] = "%s" % reminders
        rephash['n'] = 1
        editlist = (editnew % rephash).split()
        os.spawnv(os.P_WAIT, editor, editlist)
        self.Refresh() 

    def Refresh(self):
        Data.getMonths()
        linecache.clearcache()
        self.OnMonthChange(self.selday[0], self.selday[1])
        self.showDay(self.selday[0], self.selday[1], self.selday[2])

    def OnSearch(self,evt):
        y,m,d = map(int, self.selday)
        date = datetime.date(y, m, d)
        # Hack to omit the leading zero on the day
        Data.nextdate = "%s %s" % (d, date.strftime("%b %Y"))
        dlg = wx.TextEntryDialog(
                self, 'Please enter case-insensitive search string:', 
                'Searching from %s' % Data.nextdate, '')
        dlg.SetBackgroundColour(nfcolor)
        dlg.SetValue("%s" % Data.searchstr)
        if dlg.ShowModal() == wx.ID_OK:
            str = dlg.GetValue()
            day = Data.firstOccurance(str)
            if day:
                self.showDay(day[0],day[1],day[2])
                self.cal.SetDate(wx.DateTimeFromDMY(day[2],day[1]-1,day[0]))
            else:
                self.notFound()
        dlg.Destroy()

    def findNext(self,evt):
        if Data.nextdate and Data.searchstr:
            day = Data.nextOccurance()
            if day:
                self.showDay(day[0],day[1],day[2])
                self.cal.SetDate(wx.DateTimeFromDMY(day[2],day[1]-1,day[0]))
            else:
                self.notFound()
        else:
            self.OnSearch(evt)

    def notFound(self):
        dlg = wx.MessageDialog(self, 
                'No occurances of "%s" were found after %s.' % 
                (Data.searchstr, Data.nextdate),'Failed Search', 
                wx.OK | wx.ICON_INFORMATION)
        dlg.SetBackgroundColour(nfcolor)
        Data.nextdate = ''
        dlg.ShowModal()
        dlg.Destroy()

    def OnQuit(self):
        self.Destroy()

class App(wx.App):
    def OnInit(self):
        if showsplash:
            import wxRemSplash
            bmp = wxRemSplash.getBitmap() 
            splash = wx.SplashScreen(bmp, wx.SPLASH_NO_CENTRE |
                  wx.SPLASH_TIMEOUT, showsplash*1000, None, -1)
            splash.Show()
            wx.Yield()
        self.frame = MyFrame()
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True


if __name__ == '__main__':
    app = App()
    app.MainLoop()

