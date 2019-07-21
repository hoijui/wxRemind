#!/usr/bin/python
import wx
import os.path
from wxRemConfig import *

class EditWindow(wx.Dialog):
    def __init__(self, filename, linenumber):
        wx.Dialog.__init__(self, None, -1, 'wxRemEditor: %s' % filename)
        self.SetBackgroundColour(bgcolor)
        self.filename = filename
        self.linenumber = int(linenumber)
        self.changed = False
        fontfam = wx.MODERN
        efont = wx.Font(basefontsize, fontfam, 
                wx.NORMAL, wx.NORMAL)

        control = wx.TextCtrl(self, size=editorsize, style=wx.TE_MULTILINE | 
           wx.TE_DONTWRAP)
        self.control = control
        control.SetBackgroundColour(fcolor)
        control.SetFont(efont)

        cancel = wx.Button(self, wx.ID_CANCEL, ' Exit ')
        self.Bind(wx.EVT_BUTTON, self.OnCancel, cancel)
        self.cancel = cancel
        cancel.SetToolTipString("Exit - no unsaved changes")

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
        # wait until the file is loaded to bind EVT_TEXT to avoid triggering
        # this event initially
        self.Bind(wx.EVT_TEXT, self.SetUnsavedChanges, self.control)
        self.UnsavedChanges = False
        self.save.Enable(False)
        lines = control.GetNumberOfLines()
        if self.linenumber < 0 or self.linenumber >= lines:
            # Get the last, non-empty line
            self.linenumber = lines - 1
            line = control.GetLineLength(self.linenumber)
            while line <= 0 and self.linenumber > 0:
                self.linenumber -= 1
                line = control.GetLineLength(self.linenumber)
        else:
            self.linenumber += -1
        pos = max(0, control.XYToPosition(0,self.linenumber))
        line = max(0,control.GetLineLength(self.linenumber))
        control.SetStyle(pos, pos+line, wx.TextAttr('BLACK', 'YELLOW'))
        control.SetInsertionPoint(pos)
        control.ShowPosition(pos)

    def OnSave(self, event):
        textfile = open(self.filename, 'w')
        textfile.write(self.control.GetValue())
        textfile.close()
        self.control.DiscardEdits()
        self.SetUnsavedChanges(False)
        self.changed = True

    def OnCancel(self, event):
        if self.UnsavedChanges:
            dlg = wx.MessageDialog(self, "Save changes?", "File Modified", 
                    wx.wx.CANCEL |
                    wx.wx.NO | 
                    wx.wx.YES)
            dlg.SetBackgroundColour(nfcolor)
            retval = dlg.ShowModal()
            dlg.Destroy()
            if retval == wx.ID_YES:
                self.OnSave(event)
                self.EndModal(self.changed)
            elif retval == wx.ID_NO:
                self.EndModal(self.changed)
        else:
            self.EndModal(self.changed)

    def SetUnsavedChanges(self, bool):
        if bool:
            self.save.Enable(True)
            self.cancel.SetLabel(' Quit ')
            self.cancel.SetToolTipString("Abandon changes and exit")
            self.UnsavedChanges = True
        else:
            self.save.Enable(False)
            self.cancel.SetLabel(' Exit ')
            self.cancel.SetToolTipString("Exit - no unsaved changes")
            self.UnsavedChanges = False

if __name__ == '__main__':
    app = wx.PySimpleApp() 
    dlg = EditWindow('../FLOAT', 12)
    dlg.ShowModal()
    dlg.Destroy()
    app.MainLoop()

