#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 21:35:29 2018

@author: sgb
"""
import pandas as pd
from StockAPICaller import StockAPICaller
from Utilities.FileReader import FileReader

class Zacks(StockAPICaller):
    
    def __init__(self, dataRequest):
        self.fw = FileReader()
        self.dataRequest = dataRequest
        self.fileName = self.dataRequest['endpoint']
        
    
    def getStockData(self, ticker):
        zacksData = self.fw.readExcel('__InputFiles/' + self.fileName)[['Symbol', 
                                '%Surp', 
                                'Estimate', 
                                'Reported']]
        surprise = []
        estimate = []
        reported = []
        
        rowOfInterest = zacksData.loc[zacksData['Symbol'] == ticker]
        
        if len(rowOfInterest) == 0:
            print('Unable to retrieve data from ' + self.fileName + ' for ' + ticker)
            surprise.append(0)
            estimate.append(0)
            reported.append(0)
        else:
            surprise.append(rowOfInterest['%Surp'])
            surprise.append(rowOfInterest['Estimate'])
            surprise.append(rowOfInterest['Reported'])

        if self.fileName == 'Earnings.xlsx':
            output = pd.DataFrame({'ticker' : ticker, '%Surp_E' : surprise,
                                   'Estimate_E' : estimate,
                                   'Reported_E' : reported})
        elif self.fileName == 'Sales.xlsx':
            output = pd.DataFrame({'ticker' : ticker, '%Surp_S' : surprise,
                                   'Estimate_S' : estimate,
                                   'Reported_S' : reported})
        else:
            raise Exception("The input files for Zacks must either be named" + 
                            "'Earnings.xlsx' or 'Sales.xlsx'")
        return output
        
        