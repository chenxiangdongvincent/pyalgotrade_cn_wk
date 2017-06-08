# -*- coding: utf-8 -*-
# PyAlgoTrade
#
# Copyright 2011-2015 Gabriel Martin Becedillas Ruiz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""

from pyalgotrade.wukongTailored.windFeed import csvfeed
from pyalgotrade.barfeed import common
from pyalgotrade.utils import dt
from pyalgotrade.wukongTailored.windFeed import bar

import datetime


######################################################################
## Yahoo Finance CSV parser
# Each bar must be on its own line and fields must be separated by comma (,).
#
# Bars Format:
# Date,Open,High,Low,Close,Volume,Adj Close
#
# The csv Date column must have the following format: YYYY-MM-DD

def parse_date(date):
    # Sample: 2005-12-30
    # This custom parsing works faster than:
    # datetime.datetime.strptime(date, "%Y-%m-%d")
    
  
    year = int(date[0:4])
    month = int(date[5:7])
    day = int(date[8:10])
    ret = datetime.datetime(year, month, day)
 
    #ret = datetime.datetime.strptime(date,"%Y-%m-%d %H%M%S")
    
    return ret

def parse_datetime(dateTime):
    year = int(dateTime[0:4])
    month = int(dateTime[5:7])
    day = int(dateTime[8:10])
    hour = int(dateTime[11:13])
    minute = int(dateTime[14:16])
    sec = int(dateTime[17:19])
    return datetime.datetime(year, month, day, hour, minute, sec)


class RowParser(csvfeed.RowParser):
    def __init__(self, dailyBarTime, frequency, timezone=None, sanitize=False, barClass=bar.BasicBar):
        self.__dailyBarTime = dailyBarTime
        self.__frequency = frequency
        self.__timezone = timezone
        self.__sanitize = sanitize
        self.__barClass = barClass

    def __parseDate(self, dateString):
        
        """
        print dateString
        print '\n'
        """
        
        if self.__frequency == bar.Frequency.DAY:
            ret = parse_date(dateString)
            # Time on Yahoo! Finance CSV files is empty. If told to set one, do it.
            if self.__dailyBarTime is not None:
                ret = datetime.datetime.combine(ret, self.__dailyBarTime)
        elif self.__frequency == bar.Frequency.MINUTE:
            ret = parse_datetime(dateString)
            
            
        
            
        # Localize the datetime if a timezone was given.
        if self.__timezone:
            ret = dt.localize(ret, self.__timezone)
        return ret

    def getFieldNames(self):
        # It is expected for the first row to have the field names.
        return None

    def getDelimiter(self):
        return ","

    def parseBar(self, csvRowDict):
        
        #解析时间
        
        
        dateTime = self.__parseDate(csvRowDict["Date"])
        
        close = float(csvRowDict["Close"])
        open_ = float(csvRowDict["Open"])
        high = float(csvRowDict["High"])
        low = float(csvRowDict["Low"])
        volume = float(csvRowDict["Volume"])
        adjClose = float(csvRowDict["Adj Close"])
        
        #newly add
        new_column = float(csvRowDict["new_column"])
        trade_status = float(csvRowDict["trade_status"])
        maxupordown = float(csvRowDict["maxupordown"])
        
        
        #print dateTime, close

        if self.__sanitize:
            open_, high, low, close = common.sanitize_ohlc(open_, high, low, close)


        return self.__barClass(dateTime, open_, high, low, close, volume, adjClose,new_column, trade_status,maxupordown,self.__frequency)

#裁剪修改，需要支持分钟线数据
class Feed(csvfeed.BarFeed):
    """A :class:`pyalgotrade.barfeed.csvfeed.BarFeed` that loads bars from CSV files downloaded from Yahoo! Finance.

    :param frequency: The frequency of the bars. Only **pyalgotrade.bar.Frequency.DAY** or **pyalgotrade.bar.Frequency.WEEK**
        are supported.
    :param timezone: The default timezone to use to localize bars. Check :mod:`pyalgotrade.marketsession`.
    :type timezone: A pytz timezone.
    :param maxLen: The maximum number of values that the :class:`pyalgotrade.dataseries.bards.BarDataSeries` will hold.
        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the
        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.
    :type maxLen: int.

    .. note::
        Yahoo! Finance csv files lack timezone information.
        When working with multiple instruments:

            * If all the instruments loaded are in the same timezone, then the timezone parameter may not be specified.
            * If any of the instruments loaded are in different timezones, then the timezone parameter must be set.
    """

    def __init__(self, frequency=bar.Frequency.DAY, timezone=None, maxLen=None):
        if isinstance(timezone, int):
            raise Exception("timezone as an int parameter is not supported anymore. Please use a pytz timezone instead.")

        #去掉限制
        """
        if frequency not in [bar.Frequency.DAY, bar.Frequency.WEEK]:
            raise Exception("Invalid frequency.")
        """

        super(Feed, self).__init__(frequency, maxLen)

        self.__timezone = timezone
        self.__sanitizeBars = False
        self.__barClass = bar.BasicBar

    def setBarClass(self, barClass):
        self.__barClass = barClass

    def sanitizeBars(self, sanitize):
        self.__sanitizeBars = sanitize

    def barsHaveAdjClose(self):
        return True

    def addBarsFromCSV(self, instrument, path, timezone=None):
        """Loads bars for a given instrument from a CSV formatted file.
        The instrument gets registered in the bar feed.

        :param instrument: Instrument identifier.
        :type instrument: string.
        :param path: The path to the CSV file.
        :type path: string.
        :param timezone: The timezone to use to localize bars. Check :mod:`pyalgotrade.marketsession`.
        :type timezone: A pytz timezone.
        """

        if isinstance(timezone, int):
            raise Exception("timezone as an int parameter is not supported anymore. Please use a pytz timezone instead.")

        if timezone is None:
            timezone = self.__timezone

      
        
        rowParser = RowParser(
            self.getDailyBarTime(), self.getFrequency(), timezone, self.__sanitizeBars, self.__barClass
        )
        super(Feed, self).addBarsFromCSV(instrument, path, rowParser)
