#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    : WebCrawlerTool.py
@Time    : 6/15/2020 4:31 PM
@Author  : Kazuo
@Email   : azurewhale1127@gmail.com
@Software: PyCharm
'''

from urllib.request import urlopen as uReq  # Web client
import pandas as pd
import pandas_datareader as dr
import psycopg2
from bs4 import BeautifulSoup as soup  # HTML data structure
from pandas_datareader import data as yahoo_data
import matplotlib.pyplot as plt
from datetime import datetime

class WebCrawlerTool:

    def __init__(self, url='https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'):
        self.url = url

    def get_webpage(self):
        '''Get index of company names from wikipedia'''

        '''Read & Load'''
        uClient = uReq(self.url)
        page_soup = soup(uClient.read(), "html.parser")
        uClient.close()

        return page_soup

    @staticmethod
    def pre_processing(table_rows):
        '''Discard some unneccessary features, add yahoo data then return info about company'''

        data = []  # list of tickets
        head = True  # The head of the data is column names which needed to be passed

        for row in table_rows:

            if head:  # pass first iteration
                head = False
                continue

            td = row.find_all('td')
            instance = [i.text.replace('\n', '') for i in td]  # discard unneeded signs
            for i in reversed([2, 5, 6, 8]):  # discard useless columns
                instance.pop(i)
            yahoo_url = f'https://finance.yahoo.com/quote/{instance[0]}?p={instance[0]}&.tsrc=fin-srch'  # instance[0] is the ticket of the company

            instance.append(yahoo_url)
            data.append(instance)

        return data

    def get_company_data(self):
        '''Obtain index of all SP500 company from wiki'''

        index_data = self.get_webpage()  # Get website url
        table = index_data.find("table", {"class": "wikitable sortable"})  # Filter out needed tag
        table_rows = table.find_all('tr')

        # Collect all SP500 company data from wiki-pedia
        data = self.pre_processing(table_rows)  # pre process data to gain our features
        return data