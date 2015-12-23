#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import pandas as pd
import configparser
import os

from agd_tools import pg

__author__ = "Paul"


class TestPGToolsMethods(unittest.TestCase):
    """Tests should be independant (so they can be run in parallel,
    easily debugged). For convenience this is not yet the case.
    """

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

    def test_1_export_table(self):
        table_name = "iris_unittest"
        iris = pd.read_csv("tests/iris.csv")
        pg.export_df(df=iris, table_name=table_name)
        results = pg.execute_sql("SELECT COUNT(relname) " +
                                 "FROM pg_class WHERE relname='" +
                                 table_name + "'")
        self.assertEqual(1, results['count'][0])

    def test_2_import_df(self):
        table_name = "iris_unittest"
        iris1 = pg.import_df(table_name)
        iris2 = pd.read_csv("tests/iris.csv")

        size1 = len(iris1)
        size2 = len(iris2)
        self.assertEqual(size1, size2)

    def test_3_drop_table(self):
        config = configparser.ConfigParser()
        config.read(os.path.dirname(
            os.path.dirname(os.path.realpath(__file__))) +
            "/agd_tools/config.ini"
        )
        schema = config["PostgreSQL"]["schema"]

        table_name = "iris_unittest"
        drop = pg.execute_sql("DROP TABLE " + schema + "." + table_name + "",
            commit=True)
        results = pg.execute_sql("SELECT COUNT(relname) "
                                 "FROM pg_class WHERE relname='"
                                 "" + table_name + "'")
        self.assertEqual(0, results['count'][0])

if __name__ == '__main__':
    unittest.main()
