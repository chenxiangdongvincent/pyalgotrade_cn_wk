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
            
            totalEquity = self.getBroker().getEquity()
            positions = self.getBroker().getPositions()
            cash = self.getBroker().getCash()
            
            print "total equity is " + str(totalEquity)
            print "total cash is " + str(cash)
            print "total positions is " + str(positions)
            
            
            print bar.getDateTime()
            #print bar.getTradeStatus()
            #print bar.getUpDownStatus()
         
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
        for instrument in self.__instruments:
        
            bar = bars[instrument]   

            
            if bar.getClose() == 8.79 and str(instrument) == "000001.SZ":
                
                #订单可部分完成，默认是createMarketOrder
                self.__position = self.enterLong(instrument, 100,True) #美股买卖最小单位为股，需要做input合法性判断
                print str(instrument) + " buy in 100 shares"
              
            if bar.getClose() == 8.81 and str(instrument) == "000001.SZ":
                self.__position == self.enterShort(instrument,100,True)
                print str(instrument) + " sell out 100 shares"
           
            if bar.getClose() == 19.19 and str(instrument) == "000002.SZ":
                self.__position = self.enterLong(instrument, 200,True) #
                print str(instrument) + " buy in 200 shares"
        

        print "\n"
        """
          
                  
feed = windfeed.Feed()
feed.addBarsFromCSV("000004.SZ", "dataFileFeed/000004.SZ.csv")

instruments = ["000004.SZ"]

myStrategy = MyStrategy(feed,instruments)

myStrategy.run()






