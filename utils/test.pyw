import wx
from repeating_timer import RepeatingTimer as r
from winsound import Beep
def beep(): Beep(1000, 750)



app = wx.App()



frame = wx.Frame(None, title="Hi")
frame.Show(True)
t = r(3.0, beep)
t.start()
app.MainLoop()
