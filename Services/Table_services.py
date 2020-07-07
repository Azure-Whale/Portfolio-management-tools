#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    : Table_services.py
@Time    : 6/10/2020 12:38 PM
@Author  : Kazuo
@Email   : azurewhale1127@gmail.com
@Software: PyCharm
'''

'''from sp500_tb import DBsp500'''
import configparser

'''Self Package'''
from Services.Database_services import DB_Services
from Services.Yahoo_services import Yahoo_Services
from Services.Process_Services import *
from Services.Log_services import *

logger = logging.getLogger(__file__)

class table_services:

    @staticmethod
    def fetch_all(db, feature):
        config = configparser.RawConfigParser()
        config.read(f'configures/{db}.ini')
        for i in config:
            print(i)
        """Get query"""
        # if feature in config['features']['features']:
        #     query = config['fetch_all'][feature]
        # else:
        try:
            query = config['fetch_all'][feature]
        except Exception as e:
            logger.debug(f'{feature} is not available, database would return None')
            raise e
        res = DB_Services().query_execution(query)
        return res

    @staticmethod
    def fetch_one(db, feature, tik, date=None):
        config = configparser.ConfigParser()
        config.read(f'configures/{db}.ini')
        """Get query"""
        query = config['fetch_one'][feature]
        """Get res"""
        if not date:  # fetch by ticker
            res = DB_Services().query_by_ticker(query, tik)
            return res
        else:  # fetch by ticker and date
            res = DB_Services().query_by_date(query, ticker=tik, date=date)
            return res

    @staticmethod
    def insert(db, data, query=None):
        if not query:
            config = configparser.ConfigParser()
            config.read(f'configures/{db}.ini')
            query = config['insert']['all']
            DB_Services().insert(query, data=data)
        else:
            DB_Services().insert(query, data=data)



    @staticmethod
    def update_cap_yahoo(tik):
        '''Using Yahoo data to update matket cap in company table by tik'''
        tik_ = Process().ticket_format(tik[0])  # convert it into correct form
        try:
            market_cap = Yahoo_Services.get_market_cap(tik_)  # the unit of the market cap is unit dollar.
            data = (market_cap, tik)
            DB_Services().update(db='tb_company', feature='market_cap', data=data)

            logger.info(f'{tik_} market cap info updated')
        except Exception as e:
            logger.debug(f'{e}')
            logger.info(f'Cant get access to the market cap info of  {tik_}')

    @staticmethod
    def update_pe_pb_yahoo(tik):
        '''Using Yahoo data to update PE & PB in company table by tik'''
        tik_ = Process().ticket_format(tik[0])
        try:
            pb = float(Yahoo_Services().get_feature(feature='priceToBook', tik=tik_))
            pe = float(Yahoo_Services().get_feature(feature='forwardPE', tik=tik_))
            market_cap = Yahoo_Services.get_market_cap(tik_)

            DB_Services().update(db='tb_company', feature='pb_ratio', data=(pb, tik))
            DB_Services().update(db='tb_company', feature='pe_ratio', data=(pe, tik))
            DB_Services().update(db='tb_company', feature='market_cap', data=(market_cap, tik))

            logger.info(f'{tik_} pe/pb info updated')
        except Exception as e:
            logger.debug(f'{e}')
            logger.info(f'Cant get access to the pe/pb info info of  {tik_}')

    def update_operation(self, tickers):
        """Updates Kinds of dynamic attributes of tb_company"""
        ''' SQL '''
        for tik in tickers:  # Traverse all SP500 tickers and get their marketCap
            logger.info(f'updating {tik}')
            self.update_cap_yahoo(tik)
            self.update_pe_pb_yahoo(tik)
            logger.info(f'updating {tik} done')
