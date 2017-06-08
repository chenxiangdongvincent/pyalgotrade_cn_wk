# -*- coding: utf-8 -*-
"""
Created on Sat May 20 15:41:50 2017

@author: Think
"""

from pyalgotrade.wukongTailored import strategy
from pyalgotrade.wukongTailored.windFeed import windfeed
from pyalgotrade.wukongTailored.broker.backtesting import TradePercentage

from pyalgotrade.stratanalyzer import returns
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.stratanalyzer import drawdown
from pyalgotrade.stratanalyzer import trades
from pyalgotrade import dispatcher

import pandas as pd
import numpy as np

count = 0

class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed,instruments):
        
        strategy.BacktestingStrategy.__init__(self,feed,100000)  #初始化资金为10000元
        #self.getBroker().setCommission(TradePercentage(0.001)) #设置佣金比例
        self.setUseAdjustedValues(False)
        self.__instruments = instruments  #获取标的股票代码
        self.__position = None
   
   
    def onEnterOk(self, position):
        pass
        
    def onExitOk(self, position):
        pass
    
    def onStart(self):
        """Override (optional) to get notified when the strategy starts executing. The default implementation is empty. """
        
        print 'strategy starts'
        pass

    def onFinish(self, bars):
        """Override (optional) to get notified when the strategy finished executing. The default implementation is empty.

        :param bars: The last bars processed.
        :type bars: :class:`pyalgotrade.bar.Bars`.
        """
        
        print 'strategy finishes'
        
        pdShares = self.getBroker().getPdShares()
        pdTradeTracker = self.getBroker().getPdTradeShares()
        print pdShares
        print pdTradeTracker
        
        writer = pd.ExcelWriter('result/output.xlsx')
        pdShares.to_excel(writer, 'Sheet1')
        pdTradeTracker.to_excel(writer,'Sheet2')
        
        pass
        
    
    def onBars(self,bars):
        
        for instrument in self.__instruments:
            bar = bars[instrument]
            
            totalEquity = self.getBroker().getEquity()
            positions = self.getBroker().getPositions()
            cash = self.getBroker().getCash()
            
            """
            print "total equity is " + str(totalEquity)
            print "total cash is " + str(cash)
            print "total positions is " + str(positions)
            """
            
            
            #每天买入100股
            self.__position = self.enterLong(instrument, 10, True)
            
            
            

            """
            global count
            if count ==0:
            
                self.__position = self.enterLong(instrument, 10, True)
                self.__position = self.enterLong(instrument, 30, True)
                count =1
            
            
            elif count == 1:
                self.__position = self.enterLong(instrument, 30, True)
                self.__position = self.enterShort(instrument,10,True)
                self.__position = self.enterShort(instrument,10,True)
                self.__position = self.enterShort(instrument,10,True)
                self.__position = self.enterShort(instrument,10,True)
            
            
            print '\n'
            """
            
          
                  
feed = windfeed.Feed()
feed.addBarsFromCSV("000001.SZ", "dataFileFeed/000001.SZ.csv")
feed.addBarsFromCSV("000002.SZ", "dataFileFeed/000002.SZ.csv")

instruments = ["000001.SZ","000002.SZ"]
#instruments = ["000002.SZ"]

myStrategy = MyStrategy(feed,instruments)

myStrategy.run()







