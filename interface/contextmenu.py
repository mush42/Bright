import wx

class ContextMenuMixin(wx.Menu):

	def __init__(self):
		super(ContextMenuMixin, self).__init__()
		actions = self.actions
		for actionFunc, actionLabel, kw in actions:
			setattr(self, actionFunc.__name__, wx.MenuItem(self, wx.NewId(), actionLabel, **kw))
			self.AppendItem(getattr(self, actionFunc.__name__))


class Test(wx.Frame, ContextMenuMixin):
	actions = ((abs, 'ABS', {}),
		(lambda s:s, 'Just A test', {}))
	def __init__(self):
		wx.Frame.__init__(self, None, name="test")
		self.Bind(wx.EVT_LEFT_DCLICK, self.onclick)
		self.Show()
	def onclick(self, e):
		for base in self.__class__.__bases__:
			try:
				self.PopupMenu(base)
			except:
				pass

if __name__ == '__main__':
	app = wx.App()
	t = Test()
	app.MainLoop()