#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    : Process_Services.py
@Time    : 6/23/2020 12:08 PM
@Author  : Kazuo
@Email   : azurewhale1127@gmail.com
@Software: PyCharm
'''


class Process:

    @staticmethod
    def filter_none(data):
        """Filter unavailable data gained the web"""
        data = tuple(list(filter(None, data)))  # Filter some unexpected empty string
        return data

    @staticmethod
    def ticket_format(tik):
        """Correct false format of data gained from the web"""
        tik = tik.replace('.', '-')
        return tik

    @staticmethod
    def feature_extraction(row):
        '''Extract needed features from each instance'''
        row['Date'] = str(row['Date'])
        Date = row['Date']
        ticker = str(row['ticker']).replace('-', '.')
        Open = float(row['Open'])
        High = float(row['High'])
        Low = float(row['Low'])
        Close = float(row['Close'])
        Adj_Close = float(row['Adj Close'])
        Volume = int(row['Volume'])
        res = (Date, ticker, Open, High, Low, Close, Adj_Close, Volume)
        return res
