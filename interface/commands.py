from logHandler import logger
log = logger.getChild('interface.commands')

import interface
import wx
import output

class InterfaceCommands(object):
	def quit(self, key):
		interface.exit()
