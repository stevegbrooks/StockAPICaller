# -*- coding: utf-8 -*-
import pandas as pd
import re
from ANewDesign import StockAPIFactory as apiFactory
from ANewDesign.Utilities.FileReader import FileReader as fr

class UserInterface:

    stockAPICallers = []
    
    def __init__(self):
        self.stockAPICallers = []
    
    def specifyAPI(self, api, key):
        apiArgs = dict()
        apiArgs.__setitem__(api, key)
        self.stockAPICallers.append(
                apiFactory.StockAPIFactory.getAPI(apiFactory, apiArgs))
    
    def handleDataRequest(self, tickerInput):
        tickerInput = self.__parseTickerInput(tickerInput)
        stockData = pd.DataFrame()
        for caller in self.stockAPICallers:
            results = caller.getStockData(tickerInput)
            if len(stockData != 0):
                stockData = pd.merge(stockData, results, on = "stockSymbol", how = "left")
            else:
                stockData = results
        return stockData
    
    def __parseTickerInput(self, userInput):
        output = []
        match = re.search("\\.[a-zA-Z]*$", userInput, flags = 0)
        if match:
            if match.group(0) == ".xlsx" or match.group(0) == ".csv":
                self.fileInput = True
                columnNumber = 0
                output = fr.readExcelColumn(userInput, columnNumber)
            else:
                raise Exception("Currently only .xlsx and .csv files are supported.")
        else:
            output.append(userInput)
        
        return output

