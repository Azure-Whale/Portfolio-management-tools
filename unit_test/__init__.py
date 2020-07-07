#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    : __init__.py
@Time    : 6/25/2020 2:00 PM
@Author  : Kazuo
@Email   : azurewhale1127@gmail.com
@Software: PyCharm
'''


class Solution:
    def minCost(self, costs: List[List[int]]) -> int:
        prev = None
        total_cost = 0
        for i in range(len(costs)):
            print(costs[i])
            temp = min([(i,v) for i,v in enumerate(costs[i]) if i!=prev],key = lambda t: t[1])
            total_cost += temp[0] # temp[0] is the cost
            prev = temp[1]
        return total_cost