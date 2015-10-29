#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import configparser

import pandas as pd

from agd_tools import ssh

__author__ = "Paul"

""" Read config file """
config = configparser.ConfigParser()
config.read("config.ini")


class TestSSHMethods(unittest.TestCase):

    def test_get_connect(self):
        ssh.get_connect()

    def test_export_df(self):
        iris = pd.read_csv("https://raw.github.com/pydata"
                           "/pandas/master/pandas/tests/data/iris.csv")
        remotepath = "/home/" + config["SSH"]["username"] + "/" + "iris.csv"
        ssh.export_df(iris, remotepath)

    def test_import_csv(self):
        path = "/home/" + config["SSH"]["username"]
        filename = "iris.csv"
        iris = ssh.import_csv(path, filename)
        df_len_is_s1 = len(iris) > 10
        self.assertEqual(df_len_is_s1, True)

    def test_remove_file(self):
        path = "/home/" + config["SSH"]["username"]
        filename = "iris.csv"
        remotepath = path + "/" + filename
        ssh.remove_file(remotepath)
        with self.assertRaises(FileNotFoundError):
            ssh.import_csv(path, filename)


if __name__ == '__main__':
    unittest.main()
