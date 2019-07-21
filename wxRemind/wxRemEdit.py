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
        if self.key in ('alert_s', 'alert_d'):
            textCtrl.SetSelection(self.data.get(self.key, 0))
        else:
            textCtrl.SetValue(self.data.get(self.key, ""))

        return True 

    def TransferFromWindow(self):
        textCtrl = self.GetWindow()
        if self.key in ('alert_s', 'alert_d'):
            self.data[self.key] = textCtrl.GetSelection()
        elif self.key in ('date', 'time', 'warn', 'msg'):
            self.data[self.key] = textCtrl.GetValue()
            # print "validating data[%s] = '%s'" % (self.key, self.data[self.key]) 
            if self.data[self.key] == '':
                dlg = wx.MessageDialog(None, "A required field is empty!",
                        "Error", wx.OK | wx.ICON_ERROR)
                dlg.SetBackgroundColour(nfcolor)
                dlg.ShowModal()
                dlg.Destroy()
                textCtrl.SetBackgroundColour(bgcolor)
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
            alert_lV  = wx.StaticText(self, -1, "Visual Alert:")
            alert_lA  = wx.StaticText(self, -1, "Audible Alert:")

        date_t  = wx.TextCtrl(self, validator=DataXferValidator(data, "date"))
        self.Bind(wx.EVT_TEXT, self.SetUnsavedChanges, date_t)
        if type == 'f':
            warn_t  = wx.TextCtrl(self, validator=DataXferValidator(data, "warn"))
            self.Bind(wx.EVT_TEXT, self.SetUnsavedChanges, warn_t)
        if type in ('t', 'a'):
            time_t  = wx.TextCtrl(self, validator=DataXferValidator(data, "time"))
            self.Bind(wx.EVT_TEXT, self.SetUnsavedChanges, time_t)
            duration_t  = wx.TextCtrl(self, validator=DataXferValidator(data, "dur"))
            self.Bind(wx.EVT_TEXT, self.SetUnsavedChanges, duration_t)
        msg_t  = wx.TextCtrl(self, validator=DataXferValidator(data, "msg"))
        self.Bind(wx.EVT_TEXT, self.SetUnsavedChanges, msg_t)
        if type in ('u', 't', 'a'):
            omsg_t = wx.TextCtrl(self, validator=DataXferValidator(data, "omsg"))
            self.Bind(wx.EVT_TEXT, self.SetUnsavedChanges, omsg_t)

        if type == 'a':
            alertVlist = ['None', 'Pop-up Display']
            alertAlist = ['None', 'Sound', 'Spoken Message']
            alert_tV = wx.RadioBox(self, -1, "", (20,20), wx.DefaultSize,
                        alertVlist, 2, wx.RA_SPECIFY_COLS,
                        validator=DataXferValidator(data, "alert_d"))
            self.Bind(wx.EVT_RADIOBOX, self.SetUnsavedChanges, alert_tV)
            alert_tA = wx.RadioBox(self, -1, "", (20,20), wx.DefaultSize,
                        alertAlist, 3, wx.RA_SPECIFY_COLS,
                        validator=DataXferValidator(data, "alert_s"))
            self.Bind(wx.EVT_RADIOBOX, self.SetUnsavedChanges, alert_tA)

        # Use standard button IDs
        help = wx.Button(self, wx.ID_HELP)
        self.Bind(wx.EVT_BUTTON, self.OnHelp, help)
        cancel = wx.Button(self, wx.ID_CANCEL)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, cancel)
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
            fgs.Add(alert_lV, 0, wx.ALIGN_RIGHT)
            fgs.Add(alert_tV, 0, wx.EXPAND)
            fgs.Add(alert_lA, 0, wx.ALIGN_RIGHT)
            fgs.Add(alert_tA, 0, wx.EXPAND)

        fgs.AddGrowableCol(1)
        sizer.Add(fgs, 0, wx.EXPAND|wx.ALL, 5)

        btns = wx.StdDialogButtonSizer()
        btns.AddButton(help)
        btns.AddButton(okay)
        btns.AddButton(cancel)
        btns.Realize()
        sizer.Add(btns, 0, wx.EXPAND|wx.ALL, 5)
        self.UnsavedChanges = 0

        self.SetSizer(sizer)
        sizer.Fit(self)

    def OnCancel(self, event):
        # There will be 1 modification from pasting the selected date
        if self.UnsavedChanges > 0:
            dlg = wx.MessageDialog(self, "Abandon changes?", "Modified entries", 
                    wx.wx.NO |
                    wx.wx.YES)
            dlg.SetBackgroundColour(nfcolor)
            retval = dlg.ShowModal()
            dlg.Destroy()
            if retval == wx.ID_YES:
                self.EndModal(True)
        else:
            self.EndModal(True)

    def SetUnsavedChanges(self, event):
        self.UnsavedChanges += 1

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
    dlg.UnsavedChanges = -1
    dlg.ShowModal()
    dlg.Destroy()

    wx.MessageBox("You entered these values:\n\n" +
                pprint.pformat(data))

    app.MainLoop()
