#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    : Parameter_setting.py
@Time    : 6/24/2020 5:34 PM
@Author  : Kazuo
@Email   : azurewhale1127@gmail.com
@Software: PyCharm
'''

from datetime import datetime


"""Hyper parameters"""
'''Init DB date range'''
datetime_object = datetime.strptime('2020-05-10', '%Y-%m-%d')
init_start = datetime_object.date()
datetime_object = datetime.strptime('2020-05-20', '%Y-%m-%d')
init_end = datetime_object.date()
'''Calculate Date range'''
datetime_object = datetime.strptime('2020-04-29', '%Y-%m-%d')
start = datetime_object.date()
datetime_object = datetime.strptime('2020-05-20', '%Y-%m-%d')
end = datetime_object.date()
# Investment inforamtion
investment = 1000000
portfolio_path = 'import/portfolio.xlsx'
# db set
init = False