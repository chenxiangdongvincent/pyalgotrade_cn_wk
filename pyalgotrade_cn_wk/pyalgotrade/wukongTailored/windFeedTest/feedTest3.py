# -*- coding: utf-8 -*-
"""
Created on Wed Jun 07 13:07:33 2017

@author: Think
"""

from WindPy import w
import datetime
w.start()
data = w.wst("600000.SH","open","2017-06-06 09:00:00", "2017-06-06 14:04:45")

print data