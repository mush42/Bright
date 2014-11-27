from collections import OrderedDict
import datetime
from django.utils.translation import ungettext

class TimePeriod (object):
 @staticmethod
 def get_units():
  units = OrderedDict()
  units['decades'] = (_("a decade"), _("%(value)d decades"))
  units['years'] = (_("a year"), _("%(value)d years"))
  units['months'] = (_("a month"), _("%(value)d months"))
  units['weeks'] = (_("a week"), _("%(value)d weeks"))
  units['days'] = (_("a day"), _("%(value)d days"))
  units['hours'] = (_("an hour"), _("%(value)d hours"))
  units['minutes'] = (_("a minute"), _("{0} minutes"))
  units['seconds'] = (_("a second"), _("{0} seconds"))
  return units
 
 def __init__(self, date):
  now = (datetime.datetime.now() - datetime.datetime.utcfromtimestamp(0)).total_seconds()
  dt = (date - datetime.datetime.utcfromtimestamp(0)).total_seconds()
  self.seconds = int(now-dt)
  self.minutes = self.seconds / 60
  self.hours = self.minutes / 60
  self.days = self.hours / 24
  self.weeks = self.days / 7
  self.years = int(self.days / 365.25)
  self.months = int(self.years * 12 + (self.days - self.years * 365.25) / 30)
  self.decades = self.years / 10
  self.units = self.get_units()
 
 def __repr__(self):
  return "TimePeriod(" + repr(self.seconds) + ")"
 
 def __str__(self):
  return str(self.__unicode__())
 
 def __unicode__(self):
  for unit in self.units.keys():
   value = getattr(self, unit, 0)
   if value == 1:
    return self.units[unit][0].format(value)
   elif value > 1:
    res = ungettext(self.units[unit][0], self.units[unit][1], value) %{'value':value}
    return res
  return (self.units['seconds'][0], self.units['seconds'][1], self.seconds) %{'value':self.seconds}


_ = lambda s: s