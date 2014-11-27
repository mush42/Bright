from logHandler import logger
logging = logger.getChild('core.output')


from accessible_output import braille, speech
import sys
import winsound

speaker = brailler = None

def speak(text, interrupt=0):
 global speaker
 if not speaker:
  setup()
 speaker.say(text,interrupt);
 try:
  Braille(text)
 except TypeError: 
  pass

def Braille (text, *args, **kwargs):
 #Braille the given text to the display.
 global brailler
 if not brailler:
  setup()
 brailler.braille(text, *args, **kwargs)

def Copy(text):
 #Copies text to the clipboard.
 import win32clipboard
 try:
  win32clipboard.OpenClipboard()
  win32clipboard.EmptyClipboard()
  win32clipboard.SetClipboardText(text)
  win32clipboard.CloseClipboard()
 except:
  return False
 return True

def setup():
 global speaker, brailler
 logging.debug("Initializing output subsystem.")
 try:
  speaker = speech.Speaker()
  brailler = braille.Brailler()
 except:
  return logging.exception("Output: Error during initialization.")

def beep(f, d):
 return winsound.Beep(f, d)
