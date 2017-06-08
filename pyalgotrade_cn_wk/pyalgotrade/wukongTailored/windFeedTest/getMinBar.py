# -*- coding: utf-8 -*-
"""
Created on Tue May 23 09:22:15 2017

@author: Think
"""

import pandas as pd
from WindPy import *
from WindPy import w
import datetime, time
import os
import sys

"""
import sys
reload(sys)
sys.setdefaultencoding('utf8')
"""

class WindStock():
    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))
    
    
    
    def AStockHisData(self,symbols,start_date,end_date,step=0):
        
        count = 0
        print (self.getCurrentTime(),":Download stock starting ")
        for symbol in symbols:     #遍历股票池
           
            #download bein 
            if count == 2:         #下载前十只股票
                return
            print "handle one symbol"
      
            try:
                
                """
                #前复权方式
                stock = w.wsd(symbol, "windcode,sec_name,open,high,low,close,volume,trade_status,pct_chg,maxupordown",start_date,end_date, "adjDate=0;unit=1;PriceAdj=F")
   
                index_data = pd.DataFrame()
                index_data['Date'] = stock.Times
                index_data['windcode'] = stock.Data[0]
                index_data['sec_name'] = stock.Data[1]
                index_data['Open'] = stock.Data[2]
                index_data['High'] = stock.Data[3]
                index_data['Low'] = stock.Data[4]
                index_data['Close'] = stock.Data[5]
                index_data['Volume'] = stock.Data[6]
                
                index_data['Adj Close'] = stock.Data[5]      #需要修改
                index_data['trade_status'] = stock.Data[7]               #需要判断
                
    
             
                index_data['pct_chg'] = stock.Data[8]
                index_data['maxupordown'] = stock.Data[9]
                index_data['new_column'] = 1
                         
                          
                index_data = index_data.replace(u'交易',1)
                index_data = index_data.replace(u'停牌一天',0)
                """
                stock=w.wsi(symbol, "open,high,low,close,volume,amt", "2015-12-22 09:00:00", "2015-12-22 14:06:15")
                index_data = pd.DataFrame()
                index_data['Date'] = stock.Times
                index_data['Open'] = stock.Data[0]
                index_data['High'] = stock.Data[1]
                index_data['Low'] = stock.Data[2]
                index_data['Close'] = stock.Data[3]
                index_data['Volume'] = stock.Data[4]
                index_data['Adj Close'] = stock.Data[3] 
                
                index_data['trade_status'] = 1
                index_data['maxupordown'] = 0
                index_data['new_column'] = 1
                
                index_data.to_csv("dataFileFeedMin/"+str(symbol)+ ".csv",index = False,encoding="gbk")  #去除索引
                
            except Exception as e:
                print "Exceptin : %s" %(e)
                    
            count +=1
        
            
        print (self.getCurrentTime(),":download stock has finished")
        return
    
    def getAStockCodesFromCsv(self):
        #file_path = os.path.join(os.getcwd(),'Stock.csv')
        return 
    
    def getAStockCodesWind(self,end_date):
     
        stockCodes=w.wset("sectorconstituent","date="+end_date+";sectorid=a001010100000000")
        if stockCodes.ErrorCode!=0:
            print "get data failed, exit!"
            return None
        else:
            #print str(stockCodes.Data[2]).decode('unicode_escape')
            stock_data = pd.DataFrame()
            stock_data['code'] = stockCodes.Data[1]
            stock_data['name'] = stockCodes.Data[2]
            
            stock_data.to_csv("dataFileFeed/allStocks.csv",index = False,encoding="gbk")  #去除索引
            
            
            return  stock_data['code']

def main():
    
    
    w.start()
    
    windstock = WindStock()
    start_date = '20160520'
    end_date = '20170529'
    
    #获取A股所有的股票代码
    symbols=windstock.getAStockCodesWind(end_date)   
    #print "hello"
    
    fm = pd.DataFrame(symbols)
    fm = fm.T
    #print fm
    windstock.AStockHisData(symbols, start_date,end_date)
    
    #save the data into csv files

    w.stop()
        
if __name__ == "__main__":
    main()

        
        
        
        
        
        
        
        
        
        
        
            
        