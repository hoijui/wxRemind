import wx
from wxRemHints import Hints
from wxRemConfig import *

class DataXferValidator(wx.PyValidator):
    def __init__(self, data, key):
        wx.PyValidator.__init__(self)
        self.data = data
        self.key = key

    def Clone(self):
        """
        Note that every validator must implement the Clone() method.
        """
        return DataXferValidator(self.data, self.key)

    def Validate(self, win):
        return True


    def TransferToWindow(self):
        textCtrl = self.GetWindow()
        if self.key == 'alert':
            textCtrl.SetSelection(self.data.get(self.key, 0))
        else:
            textCtrl.SetValue(self.data.get(self.key, ""))
        return True 

    def TransferFromWindow(self):
        textCtrl = self.GetWindow()
        if self.key == 'alert':
            self.data[self.key] = textCtrl.GetSelection()
        elif self.key in ('date', 'time', 'warn', 'msg'):
            self.data[self.key] = textCtrl.GetValue()
            # print "validating data[%s] = '%s'" % (self.key, self.data[self.key]) 
            if self.data[self.key] == '':
                wx.MessageBox("A required field is empty!", "Error")
                textCtrl.SetBackgroundColour("yellow")
                textCtrl.SetFocus()
                textCtrl.Refresh()
                return False
        else:
            self.data[self.key] = textCtrl.GetValue()

        return True



class MyDialog(wx.Dialog):
    def __init__(self, data, type='u'):
        # type = f_loat, u_ntimed, t_imed, a_lert
        if type == 'f':
            title = "floating event"
            about_txt = """\
This floating event will be displayed on the event list for the 'date' set
below and reminders will begin appearing on the current day's event list
'warning days' earlier. Click Help for details on the date and warning
fields in floating reminders.\
"""
        elif type == 'u':
            title = "untimed event"
            about_txt = """\
This untimed event will be displayed on the event list for the 'date' set
below. Click Help for details on the 'date' field and for date substitutions in
the message fields.\
"""
        elif type == 't':
            title = "timed event"
            about_txt = """\
This timed event will be displayed on the event list for the 'date', 'time' and
'duration' set below. Click Help for details on the date, time and duration
fields, and for date and time substitutions in the message fields.\
"""
        elif type == 'a':
            title = "alert event"
            about_txt = """\
This alert event will be displayed on the event list for the 'date', 'time' and
'duration' set below.  Click Help for details on the date, time and duration
fields, and for date and time substitutions in the message fields. \
"""
        else:
            # unrecognized type
            raise NameError, 'unrecognized type: %s' % type 

        wx.Dialog.__init__(self, None, -1, "wxRemind: %s" % title, size=(600,400))
        self.SetBackgroundColour(nfcolor)

        # Create the text controls
        about   = wx.StaticText(self, -1, about_txt)
        date_l  = wx.StaticText(self, -1, "Date:")
        if type == 'f':
            warn_l  = wx.StaticText(self, -1, "Warning Days:")
        if type in ('t', 'a'):
            time_l  = wx.StaticText(self, -1, "Time (24 hour):")
            duration_l  = wx.StaticText(self, -1, "Duration:")
        msg_l  = wx.StaticText(self, -1, "Message:")
        if type in ('u', 't', 'a'):
            omsg_l  = wx.StaticText(self, -1, "Other Message:")
        if type == 'a':
            alert_l  = wx.StaticText(self, -1, "Alert:")

        date_t  = wx.TextCtrl(self, validator=DataXferValidator(data, "date"))
        if type == 'f':
            warn_t  = wx.TextCtrl(self, validator=DataXferValidator(data, "warn"))
        if type in ('t', 'a'):
            time_t  = wx.TextCtrl(self, validator=DataXferValidator(data, "time"))
            duration_t  = wx.TextCtrl(self, validator=DataXferValidator(data, "dur"))
        msg_t  = wx.TextCtrl(self, validator=DataXferValidator(data, "msg"))
        if type in ('u', 't', 'a'):
            omsg_t = wx.TextCtrl(self, validator=DataXferValidator(data, "omsg"))
        if type == 'a':
            alertList = [
                'pop-up display plus default sound',
                'pop-up display',
                'pop-up display plus spoken message',
                'spoken message', 
               ]
            alert_t = wx.RadioBox(self, -1, "", (20,20), wx.DefaultSize,
                        alertList, 2, wx.RA_SPECIFY_COLS,
                        validator=DataXferValidator(data, "alert"))

        # Use standard button IDs
        help = wx.Button(self, wx.ID_HELP)
        self.Bind(wx.EVT_BUTTON, self.OnHelp, help)
        cancel = wx.Button(self, wx.ID_CANCEL)
        okay   = wx.Button(self, wx.ID_OK)
        okay.SetDefault()

        # Layout with sizers
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(about, 0, wx.ALL, 5)
        sizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)

        fgs = wx.FlexGridSizer(3, 2, 5, 5)
        fgs.Add(date_l, 0, wx.ALIGN_RIGHT)
        fgs.Add(date_t, 0, wx.EXPAND)
        if type == 'f':
            fgs.Add(warn_l, 0, wx.ALIGN_RIGHT)
            fgs.Add(warn_t, 0, wx.EXPAND)
        if type in ('t', 'a'):
            fgs.Add(time_l, 0, wx.ALIGN_RIGHT)
            fgs.Add(time_t, 0, wx.EXPAND)
            fgs.Add(duration_l, 0, wx.ALIGN_RIGHT)
            fgs.Add(duration_t, 0, wx.EXPAND)
        fgs.Add(msg_l, 0, wx.ALIGN_RIGHT)
        fgs.Add(msg_t, 0, wx.EXPAND)
        if type in ('u', 't',  'a'):
            fgs.Add(omsg_l, 0, wx.ALIGN_RIGHT)
            fgs.Add(omsg_t, 0, wx.EXPAND)
        if type == 'a':
            fgs.Add(alert_l, 0, wx.ALIGN_RIGHT)
            fgs.Add(alert_t, 0, wx.EXPAND)

        fgs.AddGrowableCol(1)
        sizer.Add(fgs, 0, wx.EXPAND|wx.ALL, 5)

        btns = wx.StdDialogButtonSizer()
        btns.AddButton(help)
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()
        sizer.Add(btns, 0, wx.EXPAND|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def OnHelp(self, event):
        # show the hints page
        dlg = Hints(self)
        dlg.ShowModal()
        dlg.Destroy()

if __name__ == '__main__':
    import pprint
    import sys
    try:
        type = sys.argv[1]
    except:
        type = 'f'
    app = wx.PySimpleApp()

    data = { "date" : "17 May 2006" }
    dlg = MyDialog(data, type)
    dlg.ShowModal()
    dlg.Destroy()

    wx.MessageBox("You entered these values:\n\n" +
                pprint.pformat(data))

    app.MainLoop()
