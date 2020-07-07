#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    : Database_services.py
@Time    : 6/23/2020 10:07 AM
@Author  : Kazuo
@Email   : azurewhale1127@gmail.com
@Software: PyCharm
'''

import psycopg2
from configparser import ConfigParser
from Services.Log_services import *

logger = logging.getLogger(__file__)

def config(filename='configures/db_config.ini', section='postgresDB'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        logger.debug('Failed to read db configure info')
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


class DB_Services:
    def __init__(self):
        self.conn, self.cursor = self.conn_db()

    @staticmethod
    def conn_db():
        """Connect to postgresql"""
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cursor = conn.cursor()
        except Exception as e:
            logger.info('Database failed to connected')
            raise e
        return conn, cursor

    def disconn_db(self):
        if self.conn is not None:
            self.cursor.close()
            self.conn.close()

    def query_execution(self, query):
        """Normal query"""
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        return res

    def query_by_ticker(self, query, ticker):
        """Query by given ticker"""
        try:
            self.cursor.execute(query, (ticker,))
            res = self.cursor.fetchone()[0]
            return res
        except Exception as e:
            logger.info(f'{e}')
            logger.info(f'Failed to execute {query}')
            raise e
        finally:
            self.disconn_db()

    def query_by_date(self, query, date, ticker):
        """Query by given date info"""
        try:
            self.cursor.execute(query, (date, ticker))
            res = self.cursor.fetchone()[0]
            return res
        except Exception as e:
            logger.info(f'{e}')
            logger.info(f'Failed to execute {query}')
            return None
        finally:
            self.disconn_db()

    def insert(self, query, data):
        """Normal insert"""
        try:
            self.cursor.execute(query, data)
            return 1
        except Exception as e:
            logger.info(f'{e}')
            logger.info(f'Failed to execute {query}')
            return 0
        finally:
            self.disconn_db()

    def update(self, db, feature, data):
        """Normal update"""
        query = f"""Update {db} set {feature} = %s where ticker = %s"""
        try:
            self.cursor.execute(query, data)
            return 1
        except Exception as e:
            logger.info(f'{e}')
            logger.info(f'Failed to execute {query}')
            return 0
        finally:
            self.disconn_db()
