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

from pyalgotrade.wukongTailored.windFeed import bar

count = 0

class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed,instruments):
        
        strategy.BacktestingStrategy.__init__(self,feed,10000)  #初始化资金为10000元
        #self.getBroker().setCommission(TradePercentage(0.001)) #设置佣金比例
        self.setUseAdjustedValues(False)
        self.__instruments = instruments  #获取标的股票代码
        self.__position = None
   
   
    def onEnterOk(self, position):
        pass
        
    def onExitOk(self, position):
        pass
        
    
    def onBars(self,bars):
        
        for instrument in self.__instruments:
            bar = bars[instrument]
            
            print bar.getDateTime()

       
#不带参数时默认是回测日线数据           
feed = windfeed.Feed(bar.Frequency.MINUTE)
feed.addBarsFromCSV("000001.SZ", "dataFileFeedMin/000001.SZ.csv")

instruments = ["000001.SZ"]

myStrategy = MyStrategy(feed,instruments)

myStrategy.run()






