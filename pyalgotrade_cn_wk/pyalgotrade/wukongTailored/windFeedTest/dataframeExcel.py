# -*- coding: utf-8 -*-
"""
Created on Thu Jun 08 13:20:22 2017

@author: Think
"""

import pandas as pd
import numpy as np

dates = pd.date_range('20130101', periods = 6)

df1 = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))
df2 = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))

writer = pd.ExcelWriter('output.xlsx')
df1.to_excel(writer, 'Sheet1')
df2.to_excel(writer,'Sheet2')
writer.save()