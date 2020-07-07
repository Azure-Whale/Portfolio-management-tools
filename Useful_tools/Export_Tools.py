#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    : Export_Tools.py
@Time    : 6/18/2020 1:24 PM
@Author  : Kazuo
@Email   : azurewhale1127@gmail.com
@Software: PyCharm
'''
import pandas as pd
from Services.Log_services import *
loggger = logging.getLogger(__file__)
def export_portfolio_return(list, file_name='profit_portfolio'):
    if list is not None:
        df = pd.DataFrame(list)
        df.columns = ['Return', 'Dates']
        df.to_csv(f'tables/{file_name}.csv', index=False)
    else:
        loggger.debug(f"Data not found for {file_name}.csv")


def export_portfolio_income(list, file_name='income_portfolio'):
    if list is not None:
        df = pd.DataFrame(list)
        df.columns = ['Income', 'Dates']
        df.to_csv(f'tables/{file_name}.csv', index=False)
    else:
        loggger.debug(f"Data not found for {file_name}.csv")


def export_compare_return(portfolio, compare_target, tik):
    if portfolio and compare_target:
        df = pd.DataFrame(portfolio)
        df2 = pd.DataFrame(compare_target)
        df.columns = ['Profit_Rate', 'Dates']
        df = df.set_index('Dates')
        df2.columns = [tik, 'Dates']
        df2 = df2.set_index('Dates')
        df = pd.concat([df, df2[tik]], axis=1, sort=False)
        df.to_csv('tables/compare_portfolio_return.csv')
        df2.to_csv(f'tables/compare_{tik}_return.csv')
    else:
        loggger.debug(f"Data not found for compare_{tik}_return.csv'")


def export_risk_curve(list, file_name='risk_curve'):
    if list:
        df = pd.DataFrame(list)
        df.columns = ['risk', 'Dates']
        df.set_index('Dates')
        df[['Dates', 'risk']].to_csv(f'tables/{file_name}.csv', index=False)
    else:
        loggger.debug(f"Data not found for {file_name}.csv")


def export_table(df, file_name='Company_Category'):
    if df is not None:
        df.to_csv(f'tables/{file_name}.csv')
    else:
        loggger.debug(f"Data not found for {file_name}")


def export_weights(list, file_name='weight_distribution'):
    if list is not None:
        df = pd.DataFrame(list)
        df.columns = ['labels', 'weights']
        df.to_csv(f'tables/{file_name}.csv', index=False)
    else:
        loggger.debug(f"Data not found for {file_name}")


def export_sector_distribution(list, file_name='sector_distribution'):
    if list is not None:
        df = pd.DataFrame(list)
        df.columns = ['labels', 'sizes']
        df.to_csv(f'tables/{file_name}.csv', index=False)
    else:
        loggger.debug(f"Data not found for {file_name}")
