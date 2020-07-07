#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    : Calculation_services.py
@Time    : 6/17/2020 9:59 PM
@Author  : Kazuo
@Email   : azurewhale1127@gmail.com
@Software: PyCharm
'''

import pandas as pd
from datetime import datetime
import datetime
import statistics

'''package'''
from Services.Table_services import table_services
from enum import Enum
from Services.Log_services import *

logger = logging.getLogger(__file__)


class Return:

    def __init__(self, portfolio_df, weight_mod='Cap Weight'):
        """Init"""
        self.portfolio = portfolio_df
        '''Results'''
        self.quantity = None
        self.weight_mod = weight_mod

    def get_weight_mod(self):
        weight_mod = self.weight_mod
        while weight_mod not in ['Cap Weight', 'Auto', 'Even']:
            weight_mod = input('Please re input available mode, Choose from Cap Weight, Auto, Even')
        return weight_mod

    @staticmethod
    def get_profits_rate(tik, start_date, end_date):
        """ Calculate return rate for specific ticker in a period"""
        try:
            start_profit = table_services().fetch_one(db='tb_daily', feature='adj_close', tik=tik, date=start_date)
            end_profit = table_services().fetch_one(db='tb_daily', feature='adj_close', tik=tik, date=end_date)
            print(tik, start_profit, end_profit)
        except TypeError:
            logger.warning(f'We dont find adj_close data for {tik},  check the db later')
            return None
        if end_profit and start_profit:
            profit_rate = (end_profit / start_profit) - 1
            return profit_rate
        else:
            logger.warning(f'We dont find complete adj_close data for {tik},  check the db later')
            return None

    def profit_unit(self, start_date, end_date, ticker, investment=1000000):
        """ Calculate the profits of all tiks in import between 2 days"""
        logger.info(f'Show the profits from {start_date} to {end_date}:')
        weight_mod = self.get_weight_mod()  # Check current weight mod availability

        income = 0  # how much return we had now
        total_weight = 100  # Record exactly how much weight we pay for our import as some of them are not available

        if ticker:  # if ticker does exist then only return the case of this ticker
            prof_rate = self.get_profits_rate(ticker, start_date, end_date)
            if not prof_rate:  # if there is no prof_data for that
                prof_rate = 0
            income = investment * (1 + prof_rate)
            return income, prof_rate
        else:
            for index, row in self.portfolio.iterrows():  # update basic info like market_cap & Sector
                tik = row['Ticker']
                inv_weight = None
                if not weight_mod:
                    print('set to default mod -- Cap Weight')
                    weight_mod = 'Cap Weight'
                if weight_mod == 'Cap Weight':  # Default mod is cap weight
                    inv_weight = row['Cap Weight'] * 100
                elif weight_mod == 'Auto':
                    inv_weight = row['Weight']  # even mod
                elif weight_mod == 'Even':
                    inv_weight = 100 / len(self.portfolio)

                prof_rate = self.get_profits_rate(tik, start_date, end_date)

                if not prof_rate:  # if there is no data for calculation of this ticket on that day
                    prof_rate = 0
                    total_weight -= inv_weight

                show1 = round(prof_rate, 4)
                logger.info(f'The profits from {tik} is {show1}')
                # log.write(f'The profits from {tik} is {show1}\n')
                temp = investment * (inv_weight / 100) * (1 + prof_rate)
                income += temp

            if total_weight > 0:  # if there are some ticker don't have any data, then invest all on the rest of them
                income *= (100 / total_weight)
            re = (income / investment) - 1

            return income, re

    def get_profits(self, start_date, end_date, ticker, investment=1000000):
        """Get profits from one day to another day"""
        print('Calculating..')
        step = datetime.timedelta(1)
        start_date = start_date + step
        '''Init'''
        return_movements = []
        income_movements = []
        while start_date != end_date:
            last_day = start_date - step
            '''Do Calculation'''
            if not ticker:  # portfolio mod
                income, profit_rate = self.profit_unit(last_day, start_date, None, investment=investment,
                                                       )  # profit between a day
            else:
                income, profit_rate = self.profit_unit(last_day, start_date, ticker, investment=investment,
                                                       )  # profit between a day
            '''Process'''
            investment = income  # Income becomes investment for next turn
            income = round(income, 5)
            profit_rate = round(profit_rate, 5)
            '''Records changes of profit and gain'''
            return_movements.append([profit_rate, start_date])
            income_movements.append([income, start_date])
            '''Continue'''
            start_date += step
        print('Calculation Done..')
        return return_movements, income_movements

    def get_risks(self, start_date, end_date, ticker, investment=1000000):
        risks = []
        profit_movements, income_movements = self.get_profits(start_date, end_date, ticker, investment=investment)
        for i in range(len(profit_movements) - 1):
            profits = [profit for profit, date in
                       profit_movements[i:]]  # get the profits movements starts from that day
            risk = statistics.stdev(profits)
            dates = profit_movements[i][1]  # get the date of the first day
            risks.append((risk, dates))
        if risks:
            return risks
        else:
            return None

    def get_sector_distributions(self):
        refer = ['Energy',
                 'Materials',
                 'Industrials',
                 'Consumer Discretionary',
                 'Consumer Staples',
                 'Health Care',
                 'Financials',
                 'Information Technology',
                 'Telecommunication Services',
                 'Utilities',
                 'Real Estate']
        values = [0] * 11
        res = [[k, v] for k, v in zip(refer, values)]

        if self.weight_mod == 'Cap Weight':
            invest_weight = self.portfolio.groupby("Sector")["Cap Weight"].sum()
            labels = invest_weight.index.values
            sizes = invest_weight.values

        else:
            invest_weight = self.portfolio.groupby("Sector")["Weight"].sum()
            labels = invest_weight.index.values
            sizes = invest_weight.values

        for l, w in zip(labels, sizes):
            for item in res:
                if item[0] == l:
                    item[1] = w

        return res

    def get_weights_distribution(self):
        '''Invest Weight Pie plot'''
        if self.weight_mod == 'Auto':
            invest_weight = self.portfolio.groupby("Sector")["Weight"].sum()
            labels = invest_weight.index.values
            sizes = invest_weight.values

        ''' Which weight? '''
        if self.weight_mod == 'Cap Weight':
            invest_weight = self.portfolio.groupby("Sector")["Cap Weight"].sum()
            labels = invest_weight.index.values
            sizes = invest_weight.values

        else:
            '''Modify it into even later'''
            invest_weight = self.portfolio.groupby("Sector")["Weight"].sum()
            labels = invest_weight.index.values
            sizes = invest_weight.values

        return [[label, size] for label, size in zip(labels, sizes)]

    def get_company_cluster(self, table_path='import/PE&PB.xlsx'):
        tickers = self.portfolio['Ticker']  # tickers in import
        # temp = Services.fetch_all(db='tb_company', feature='Market Cap', cursor=cursor)

        '''Market Cap threshold'''
        cap = table_services.fetch_all(db='tb_company', feature='market_cap')
        max_cap = max(cap)[0]  # upper
        min_cap = min(cap)[0]  # lower
        divde_cap = (1 / 3) * (max_cap - min_cap)

        class CompanySize(Enum):
            SMALL = min_cap + divde_cap
            MID = min_cap + 2 * divde_cap
            LARGE = max_cap

        print(CompanySize.SMALL.value, CompanySize.MID.value, CompanySize.LARGE.value)

        # print(min_cap+divde_cap,min_cap+2*divde_cap,max_cap)
        # 1/3 small 2/3 mid 3/3 large
        '''PE & PB threshold'''
        pb = table_services.fetch_all(db='tb_company', feature='pb_ratio')
        pe = table_services.fetch_all(db='tb_company', feature='pe_ratio')
        max_pb_pe = (max(pb)[0] + max(pe)[0]) / 2
        min_pb_pe = (min(pb)[0] + min(pe)[0]) / 2
        devide_pe_pb = (1 / 3) * (max_pb_pe - min_pb_pe)

        class CompanyGrowth(Enum):
            Value = min_pb_pe + devide_pe_pb
            Core = min_pb_pe + 2 * devide_pe_pb
            Growth = max_pb_pe

        print(CompanyGrowth.Value.value, CompanyGrowth.Core.value, CompanyGrowth.Growth.value)

        df = pd.DataFrame(0, columns=['Small', 'Mid', 'Large'], index=['Value', 'Core', 'Growth'])

        for tik in tickers:
            print(tik)
            pb = table_services.fetch_one(db='tb_company', feature='pb_ratio', tik=tik)
            pe = table_services.fetch_one(db='tb_company', feature='pe_ratio', tik=tik)
            cap = table_services.fetch_one(db='tb_company', feature='market_cap', tik=tik)
            if pe and pb and cap:
                eb = (1 / 2) * (pe + pb)
                logger.info(f"{tik}: cap: {cap} pe and pb: {eb}")
            else:
                logger.info(f"No data was found for {tik} ")
                continue

            if cap < CompanySize.SMALL.value and eb < CompanyGrowth.Value.value:
                df.loc['Value', 'Small'] += self.portfolio[self.portfolio['Ticker'] == tik][
                    'Cap Weight'].values
            if CompanySize.SMALL.value < cap < CompanySize.MID.value and eb > CompanyGrowth.Value.value:
                df.loc['Value', 'Mid'] += self.portfolio[self.portfolio['Ticker'] == tik][
                    'Cap Weight'].values
            if CompanySize.MID.value < cap and eb < CompanyGrowth.Value.value:
                df.loc['Value', 'Large'] += self.portfolio[self.portfolio['Ticker'] == tik][
                    'Cap Weight'].values

            if cap < CompanySize.SMALL.value and CompanyGrowth.Value.value < eb < CompanyGrowth.Core.value:
                df.loc['Core', 'Small'] += self.portfolio[self.portfolio['Ticker'] == tik][
                    'Cap Weight'].values
            if CompanySize.SMALL.value < cap < CompanySize.MID.value and CompanyGrowth.Value.value < eb < CompanyGrowth.Core.value:
                df.loc['Core', 'Mid'] += self.portfolio[self.portfolio['Ticker'] == tik][
                    'Cap Weight'].values
            if CompanySize.MID.value < cap and CompanyGrowth.Value.value < eb < CompanyGrowth.Core.value:
                df.loc['Core', 'Large'] += self.portfolio[self.portfolio['Ticker'] == tik][
                    'Cap Weight'].values

            if cap < CompanySize.SMALL.value and eb > CompanyGrowth.Core.value:
                df.loc['Growth', 'Small'] += self.portfolio[self.portfolio['Ticker'] == tik][
                    'Cap Weight'].values
            if CompanySize.SMALL.value < cap < CompanySize.MID.value and eb > CompanyGrowth.Core.value:
                df.loc['Growth', 'Mid'] += self.portfolio[self.portfolio['Ticker'] == tik][
                    'Cap Weight'].values
            if CompanySize.MID.value < cap and eb > CompanyGrowth.Core.value:
                df.loc['Growth', 'Large'] += self.portfolio[self.portfolio['Ticker'] == tik][
                    'Cap Weight'].values

        return df
