from logHandler import logger
logging=logger.getChild('core.interface')
from main import *

import globalVars
import output
import sys
import application
import wx

def exit():
	confirm=wx.MessageDialog(None, _("Are you sure you want to exit %s?.")%application.name, _("Confirm Exit"), wx.YES|wx.NO|wx.ICON_WARNING)
	application.MainFrame.DisplayDialog(confirm)
	answer=confirm.ShowModal()
	if answer==wx.ID_YES:
		exitConfirmed=True
	else:
		exitConfirmed=False
		application.MainFrame.CloseDialog(confirm)
		return
	if exitConfirmed:
		shutdown()

def shutdown(silent=False):
	exited=False
	if not silent:
		output.speak(_("See You Later!"), True)
	logging.debug("Closing all open windows.")
	try:
		for child in application.MainFrame.GetChildren():
			wx.CallAfter(child.Destroy)
	except: logging.exception("Error, couldn't destroy open windows.")
	try: application.Hotkey.unregisterHotkeys()
	except: logging.exception("Error unregistering hotkeys.")
	application.MainFrame.Destroy()
	wx.GetApp().ExitMainLoop()
	exited=True
	sys.exit(1)