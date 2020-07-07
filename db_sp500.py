#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    : db_sp500.py
@Time    : 6/2/2020 2:25 PM
@Author  : Kazuo
@Email   : azurewhale1127@gmail.com
@Software: PyCharm
'''

from Services.Table_services import table_services
from Useful_tools.WebCrawlerTool import WebCrawlerTool
from Services.Yahoo_services import Yahoo_Services
from Services.Process_Services import *
from Services.Log_services import *

logger = logging.getLogger(__file__)


class DBsp500:

    def tb_company_init(self, update):
        """Preparation"""
        logger.info('tb_company init..')
        logger.info('Crawling data from wiki..')
        company_data = WebCrawlerTool('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies').get_company_data()
        logger.info('Crawling done')
        '''Index information Operation SQL'''
        insert_sql = """ INSERT INTO tb_company(ticker,name,gics_sector,gics_sub_industry,cik,url) VALUES (%s,%s,%s,%s,%s,%s) """
        if not company_data:
            logger.debug('No data was collected')
        else:
            for row in company_data:
                row = Process().filter_none(row)
                table_services.insert(db='tb_company', query=insert_sql, data=row)

        if update:
            self.update_tb_company()  # Update Dynamic info in company table such as sector, cap weight
        logger.info('tb_company done')

    def update_tb_company(self):
        """ Update dynamic data  """
        tickers = table_services.fetch_all(db='tb_company', feature='ticker')
        logger.info('Updating tb_company..')
        if tickers:
            table_services().update_operation(tickers=tickers)
        logger.info('Updating tb_company done')

    def tb_daily_init(self, begin='2020-1-01', end='2020-5-31'):
        """ Preparation """
        logger.info('Init tb_daily..')
        '''Fetch ticker from table'''
        tickers = table_services.fetch_all(db='tb_company', feature='ticker')
        for tik in tickers:
            '''Format Prepossessing'''
            ticker = Process().ticket_format(tik[0])  # The ticker format is not exactly the same with the wiki on yahoo
            '''try:'''
            data = Yahoo_Services().get_stock(ticker, begin=begin, end=end).reset_index()
            data.insert(0, 'ticker', ticker)  # Insert ticker to the data frame obtained, tho the ticker is not in
            # correct format, it would be fixed in feature_extraction process
            for index, row in data.iterrows():
                res = Process().feature_extraction(row)
                table_services.insert(db='tb_daily',
                                      data=res)
        logger.info('Updating tb_daily done')
