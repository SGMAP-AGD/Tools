#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import pandas as pd

from agd_tools import pg

__author__ = "Paul"


class TestPGToolsMethods(unittest.TestCase):

    def test_conn_string(self):
        conn_string = pg.get_conn_string(host="localhost",
                                         dbname="postgres",
                                         user="username",
                                         password="commonpassword",
                                         client_encoding="some-" +
                                         "exotic-encoding")
        expected_string = "host='localhost' " + \
                          "dbname='postgres' " + \
                          "user='username' " + \
                          "password='commonpassword' " + \
                          "client_encoding='some-exotic-encoding'"
        self.assertEqual(conn_string, expected_string)

    def test_export_table(self):
        table_name = "iris_unittest"
        iris = pd.read_csv("tests/iris.csv")
        pg.export_df(df=iris, table_name=table_name)
        results = pg.execute_sql("SELECT COUNT(relname) " +
                                 "FROM pg_class WHERE relname='" +
                                 table_name + "'")
        self.assertEqual(1, results['count'][0])

    def test_import_table(self):
        table_name = "iris_unittest"
        iris = pg.import_table(table_name)
        size_table = pg.execute_sql("SELECT COUNT(*) "
                                    "FROM " + table_name)
        size_df = len(iris)
        self.assertEqual(size_df, size_table['count'][0])

    def test_drop_table(self):
        table_name = "iris_unittest"
        drop = pg.execute_sql("DROP TABLE " + table_name + "", commit=True)
        results = pg.execute_sql("SELECT COUNT(relname) "
                                 "FROM pg_class WHERE relname='"
                                 "" + table_name + "'")
        self.assertEqual(0, results['count'][0])

if __name__ == '__main__':
    unittest.main()
