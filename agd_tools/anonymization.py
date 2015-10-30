#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd

__author__ = "Paul"


def get_k(df, columns="all"):

    if(columns == "all"):
        """ Get all columns for aggregation """
        columns = df.columns.values

    len_columns = len(columns)
    if(len_columns == 1):
        """ pandas grouby function does not take single element lists """
        columns = columns[0]

    dfgb = df.groupby(columns)

    k = len(dfgb)
    return k
