#!/usr/bin/python
import wx
import os.path
from wxRemConfig import *

class EditWindow(wx.Dialog):
    def __init__(self, filename, linenumber = -1):
        wx.Dialog.__init__(self, None, -1, 'wxRemEditor: %s' % filename)
        self.SetBackgroundColour(bgcolor)
        self.filename = filename
        self.linenumber = int(linenumber)
        fontfam = wx.MODERN
        efont = wx.Font(basefontsize, fontfam, 
                wx.NORMAL, wx.NORMAL)

        control = wx.TextCtrl(self, size=editorsize, style=wx.TE_MULTILINE | 
           wx.TE_DONTWRAP)
        self.Bind(wx.EVT_TEXT, self.SetModified, control)
        self.control = control
        control.SetBackgroundColour(fcolor)
        control.SetFont(efont)

        cancel = wx.Button(self, wx.ID_CANCEL, ' Exit ')
        self.cancel = cancel
        cancel.SetToolTipString("Quit")

        save   = wx.Button(self, wx.ID_SAVE, ' Save ')
        self.Bind(wx.EVT_BUTTON, self.OnSave, save)
        save.SetToolTipString("Save changes and continue editing")
        self.save = save

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(control, 1, wx.EXPAND | wx.ALL, 5)
        btns = wx.StdDialogButtonSizer()
        btns.AddButton(cancel)
        btns.AddButton(save)
        btns.Realize()
        sizer.Add(btns, 0, wx.EXPAND | wx.ALL , 5)
        self.SetSizerAndFit(sizer)
        self.SetBackgroundColour(bgcolor)
        sizer.Fit(self)

        control.LoadFile(self.filename)
        lines = control.GetNumberOfLines()
        print lines
        if self.linenumber < 0 or self.linenumber >= lines:
            # Get the last, non-empty line
            self.linenumber = lines - 1
            line = control.GetLineLength(self.linenumber)
            print self.linenumber, line
            while line <= 0 and self.linenumber > 0:
                self.linenumber -= 1
                line = control.GetLineLength(self.linenumber)
                print self.linenumber, line
        else:
            self.linenumber += -1
        pos = max(0, control.XYToPosition(0,self.linenumber))
        line = max(0,control.GetLineLength(self.linenumber))
        print self.linenumber, pos, line
        control.SetStyle(pos, pos+line, wx.TextAttr('BLACK', 'YELLOW'))
        control.SetInsertionPoint(pos)
        control.ShowPosition(pos)
        self.SetModified(False)

    def OnSave(self, event):
        textfile = open(self.filename, 'w')
        textfile.write(self.control.GetValue())
        textfile.close()
        self.control.DiscardEdits()
        self.SetModified(False)

    def SetModified(self, bool):
        if bool:
            self.save.Enable(True)
            self.cancel.SetLabel(' Quit ')
            self.cancel.SetToolTipString("Abandon changes and exit")
        else:
            self.save.Enable(False)
            self.cancel.SetLabel(' Exit ')
            self.cancel.SetToolTipString("Exit - file unchanged")

if __name__ == '__main__':
    app = wx.PySimpleApp() 
    dlg = EditWindow('../FLOAT', 12)
    dlg.ShowModal()
    dlg.Destroy()
    app.MainLoop()

