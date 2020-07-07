#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    : Import_Tools.py
@Time    : 6/17/2020 10:21 PM
@Author  : Kazuo
@Email   : azurewhale1127@gmail.com
@Software: PyCharm
'''
import pandas as pd
from Services.Table_services import table_services
from Services.Log_services import *

logger = logging.getLogger(__file__)

class ReadAndLoad:
    '''Read and Load portfolio into the system, and fill the blanks at the same time'''

    def __init__(self, input_path='import/portfolio.xlsx', output_path='import/portfolio.xlsx'):
        self.path = input_path
        self.output_path = output_path
        self.portfolio = None
        self.process()

    @staticmethod
    def get_portfolio(path):
        """ Read given import then return data frame of import"""
        try:
            df = pd.read_excel(path, index=False)
            return df
        except FileNotFoundError as e:
            logger.debug('Please import portfolio in correct path')
            raise e

    def process(self):

        df = pd.read_excel(self.path, index=False)
        self.portfolio = df
        print(df)
        """ Update basic information of import """
        for index, row in self.portfolio.iterrows():  # update basic info like market_cap & Sector
            sector = table_services.fetch_one(db='tb_company', tik=row['Ticker'], feature='gics_sector')
            self.portfolio.loc[index, 'Sector'] = sector
            cap = table_services.fetch_one(db='tb_company', tik=row['Ticker'], feature='market_cap')
            self.portfolio.loc[index, 'Market Cap'] = cap
        '''Calculate the weight distribution according to the cap weights obtained'''
        total_cap = self.portfolio['Market Cap'].sum()
        for index, row in self.portfolio.iterrows():  # Update cap weight
            self.portfolio.loc[index, 'Cap Weight'] = self.portfolio.loc[index, 'Market Cap'] / total_cap
        '''Save the results'''
        self.portfolio.to_excel(self.output_path, index=False)  # Save updates info to origin csv

