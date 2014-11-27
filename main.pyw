# This file is using the following encoding: utf-8

import sys
import os
import wx
import application
import interface
import i18n
import output
import paths
import globalVars
import config
from logHandler import logger as log

"""
This is the Bright launcher. It initializes all required core components in order for the application to start successfully and then starts the application.
"""

class FVApp(wx.App):

	def OnInit(self):
		log.info("starting Application")
		self.name = application.name+" - %s"%wx.GetUserId()
		self.instance = wx.SingleInstanceChecker(self.name)
		if self.instance.IsAnotherRunning():
			wx.MessageBox("Application already running.", application.name, wx.ICON_WARNING|wx.OK)
			return False
		try:
			config.initialize()
		except:
			log.exception("Error initializing configuration subsystem")
			return False
		try:
			i18n.setup()
		except:
			log.exception("Error initializing internationalization i18n system.")
			return False

		try:
			output.setup()
			output.speak(_("Wellcome to %s") %application.name)
		except:
			wx.MessageBox(_("Failed to initialize output subsystem. The application may not be started. Please contact development team for help."), _("Error"), wx.ICON_ERROR|wx.OK)
			return False
		self.SetAssertMode(wx.PYAPP_ASSERT_SUPPRESS)
		self.Bind(wx.EVT_QUERY_END_SESSION, lambda evt: None)
		self.Bind(wx.EVT_END_SESSION, self.onEndSession)
		return True

	def onEndSession(self, evt):
		log.warn("Windows session ending, closing the application.")
		return interface.shutdown(silent=True)


def main():
	wxLog= paths.data_path('wx.log')
	try:
		os.remove(wxLog)
		os.remove(paths.data_path("{0}.log".format(application.name)))
	except os.error:
		pass
	#Extra log messages
	log.info("Windows version info: %r"%sys.getwindowsversion())
	log.info("Python version info: %r"%sys.version_info)
	log.info("Using %s version %s."%(application.name, application.version[0]))
	globalVars.App= FVApp(redirect=True, useBestVisual=True, filename=wxLog)
	wx.Log_SetActiveTarget(wx.LogStderr())
	wx.Log_SetTraceMask(wx.TraceMessages)
	log.info("Initializing GUI.")
	interface.mainFrame=interface.mainInterface(None, wx.ID_ANY, "Social Gate")
	wx.GetApp().SetTopWindow(interface.mainFrame)
	globalVars.App.MainLoop()

if __name__=="__main__":
	try:
		main()
	except:
		log.exception("Application startup failure.")