import platform
import os
import sys
import application
from functools import wraps

def merge_paths(func):
 @wraps(func)
 def merge_paths_wrapper(*a):
  return unicode(os.path.join(func(), *a))
 return merge_paths_wrapper

@merge_paths
def data_path(app_name=application.name):
 import shlobj
 data_path = os.path.join(shlobj.SHGetFolderPath(0, shlobj.CSIDL_APPDATA), app_name)
 if not os.path.exists(data_path):
  os.mkdir(data_path)
 return data_path

@merge_paths
def app_path():
 if hasattr(sys, "frozen"):
  from win32api import GetModuleFileName #We should only be here if using py2exe hence windows
  app_path = os.path.dirname(GetModuleFileName(0))
 else:
  app_path = os.path.normpath(os.path.dirname(__file__))
 return app_path

@merge_paths
def locale_path():
 return app_path(u"locale")

@merge_paths
def sounds_path():
 return app_path(u"sounds")

