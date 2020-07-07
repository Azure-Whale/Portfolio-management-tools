#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    : test_db.py
@Time    : 6/24/2020 10:27 PM
@Author  : Kazuo
@Email   : azurewhale1127@gmail.com
@Software: PyCharm
'''

from Useful_tools.Import_Tools import ReadAndLoad
import unittest


class TestCalc(unittest.TestCase):

    def test_ReadAndLoad(self):
        portfolio_path = r'C:\Users\Night\Desktop\github_projects\SP500\import\test_Portfolio.xlsx'
        portfolio = ReadAndLoad(input_path=portfolio_path, output_path=portfolio_path).get_portfolio(portfolio_path)
        port = False
        if portfolio:
            port = True
        self.assertTrue(port)


if __name__ == '__main__':
    unittest.main()
