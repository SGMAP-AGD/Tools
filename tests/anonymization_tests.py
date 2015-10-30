#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import pandas as pd

from agd_tools import anonymization

__author__ = "Paul"


class TestAnonymisationMethods(unittest.TestCase):

    def test_get_k(self):
        iris = pd.read_csv("https://raw.github.com/pydata"
                           "/pandas/master/pandas/tests/data/iris.csv")
        iris_anonymized = iris[['Name']]
        k = anonymization.get_k(iris_anonymized)
        self.assertEqual(k, 3)

if __name__ == '__main__':
    unittest.main()
