import interface
import application
import wx
import os
from paths import app_path

class TBIcon(wx.TaskBarIcon):
	"""The Social Gate Notification Area icon object."""

	def __init__(self, parent):
		super(TBIcon, self).__init__()
		icon=wx.Icon(os.path.join(app_path(), "icon.ico"), wx.BITMAP_TYPE_ICO)
		self.SetIcon(icon, "%s"%application.name)
		self.Menu=wx.Menu()
		ExitId=wx.NewId()
		ExitOption=wx.MenuItem(self.Menu, ExitId, "E&xit", "Exit %s" %application.name)
		self.Menu.AppendItem(ExitOption)
		wx.EVT_MENU(self.Menu, ExitId, lambda evt: interface.exit())
		self.Bind(wx.EVT_TASKBAR_RIGHT_DOWN, self.onActivate)

	def Destroy(self):
		self.Menu.Destroy()
		super(TBIcon, self).Destroy()

	def onActivate(self, evt):
		self.PopupMenu(self.Menu)
