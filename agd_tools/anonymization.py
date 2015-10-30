#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd

__author__ = "Paul"


def get_k(df, columns = None):
    ''' k here refers to the k-anonymity'''
    # by default, use all columns for aggregation
    if columns is None:
        columns = df.columns

    # pandas grouby function does not take single element lists
    if len(columns) == 1:
        columns = columns[0]

    size_group = df.groupby(columns).size()
    return min(size_group)