import interface
import globalVars
import hotkey
import config
import systemTray
import wx
import commands
import mainwindow
import output

from utils.thread_utils import call_threaded

class mainInterface(wx.Frame):

	def __init__(self, *args, **kwargs):
		super(mainInterface, self).__init__(style=wx.DEFAULT_FRAME_STYLE ^ wx.MAXIMIZE_BOX ^ wx.MINIMIZE_BOX | wx.FRAME_NO_TASKBAR, *args, **kwargs)
		self.Center()
		self.Hide()
		self.sysTrayIcon=systemTray.TBIcon(self)
		globalVars.Hotkey=hotkey.HotkeySupport(self, commands.InterfaceCommands(), config.conf['keyboard'])
		self.showMainWindow()

	def DisplayDialog(self, dlg):
		self.Raise()
		if globalVars._firstguirun:
			dlg.Show(True)
			dlg.Hide()
		dlg.Show(True)
		dlg.Centre()
		globalVars._firstguirun=False

	def CloseDialog(self, dlg):
		self.Hide()
		dlg.Destroy()

	def Destroy(self):
		try: self.sysTrayIcon.Destroy()
		except: pass
		super(mainInterface, self).Destroy()

	def showMainWindow(self):
		interface.mainWindow = interface.mainwindow.MainWindow(parent=self)
		self.DisplayDialog(interface.mainWindow)
