#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    : Log_services.py
@Time    : 6/23/2020 10:19 AM
@Author  : Kazuo
@Email   : azurewhale1127@gmail.com
@Software: PyCharm
'''

import logging

# set up logging to file - see previous section for more details
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename= 'C:/Users/Night/Desktop/github_projects/SP500/logs/Portfolio_Analysis.log',
                    filemode='w')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

