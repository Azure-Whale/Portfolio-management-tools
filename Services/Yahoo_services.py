#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    : Yahoo_services.py
@Time    : 6/23/2020 10:06 AM
@Author  : Kazuo
@Email   : azurewhale1127@gmail.com
@Software: PyCharm
'''

from pandas_datareader import data as yahoo_data
import pandas_datareader as dr


class Yahoo_Services:

    @staticmethod
    def get_stock(ticker, begin, end):
        data = dr.DataReader(ticker, start=begin, end=end, data_source='yahoo')
        return data

    @staticmethod
    def get_market_cap(tik):
        temp = yahoo_data.get_quote_yahoo(tik)['marketCap'].values
        market_cap = float(temp[0]) * 1000000000  # unit transformation
        return market_cap

    @staticmethod
    def get_feature(feature,tik):
        return yahoo_data.get_quote_yahoo(tik)[feature].values
