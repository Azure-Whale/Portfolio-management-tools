#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : Main.py
@Time    : 6/2/2020 2:33 PM
@Author  : Kazuo
@Email   : azurewhale1127@gmail.com
@Software: PyCharm
"""

from db_sp500 import DBsp500
from Useful_tools.Import_Tools import ReadAndLoad
from Services.Calculation_services import Return
from Useful_tools.Export_Tools import *
from Services.Log_services import *
from configures.Parameter_setting import *


def Init():
    """"Built Tables"""
    db = DBsp500()  # Connect to the database
    """Init DB"""
    if init:
        logger = logging.getLogger(__file__)
        logger.warning('Database Init Starts')
        db.tb_company_init(update=True)  # Built company table to store some basic info based on wiki data
        db.tb_daily_init(init_start,
                         init_end)  # Built daily table to store daily performance for selected companies
        # based on yahoo data
        logger.warning('Database Init Over')
    """Calculate by owned data"""

    '''1.Load portfolio'''
    df_portfolio = ReadAndLoad(input_path=portfolio_path, output_path=portfolio_path).get_portfolio(portfolio_path)
    return df_portfolio


def Process(df_portfolio):
    '''2.Main info'''
    Cap_Re = Return(df_portfolio, weight_mod='Cap Weight')
    re, income = Cap_Re.get_profits(start_date=start, end_date=end, ticker=None)
    risk = Cap_Re.get_risks(start_date=start, end_date=end, ticker=None)
    cp_re, cp_income = Cap_Re.get_profits(start_date=start, end_date=end, ticker='AMZN')
    cp_risk = Cap_Re.get_risks(start_date=start, end_date=end, ticker='AMZN')

    '''3.Sub info'''
    weights_distribution = Cap_Re.get_weights_distribution()
    sector_distributions = Cap_Re.get_sector_distributions()
    company_cluster = Cap_Re.get_company_cluster('import/PE&PB.xlsx')

    res = [re, income, risk, cp_re, cp_income, cp_risk, weights_distribution, sector_distributions, company_cluster]
    return res


def export(results):
    export_portfolio_return(results[0])  # re
    export_portfolio_income(results[1])  # income
    export_compare_return(portfolio=results[0], compare_target=results[3], tik='AMZN')  # re and cp_re
    export_risk_curve(results[2])  # risk
    export_weights(results[6])  # weights_distribution
    export_sector_distribution(results[7])  # sector_distributions
    export_table(results[8])  # company_cluster


def main():
    df = Init()
    results = Process(df)
    export(results)


main()
