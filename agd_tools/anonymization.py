#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd

__author__ = "Paul"


def get_k(df, groupby):
    """
        Return the k-anonymity level of a df, grouped by the specified columns.

        :param df: The dataframe to get k from
        :param groupby: The columns to group by
        :type df: pandas.DataFrame
        :type groupby: Array
        :return: k-anonymity
        :rtype: int
    """
    size_group = df.groupby(groupby).size()
    return min(size_group)


def get_distinct_l(df, column, groupby):
    """
        Return the l-diversity level of a column, grouped by another column.

        A simple implementation of distinct l-diversity.
        Aggarwal, Charu C.; Yu, Philip S. (2008):
        "A General Survey of Privacy"
        http://charuaggarwal.net/generalsurvey.pdf
        Springer. ISBN 978-0-387-70991-8.
        This implementation takes None values as distinct modalities.
        You should replace all invalid, unknown and false rows by None
        before using this function

        :param df: The dataframe to get l from
        :param column: The sensible data column
        :param groupby: The columns to group by
        :type df: pandas.DataFrame
        :type column: string
        :type groupby: Array
        :return: l-diversity
        :rtype: int

        :Example:

        >>> iris = pd.read_csv("tests/iris.csv")
        >>> l_diversity = anonymization.get_distinct_l(iris,
                                                       groupby=['Name'],
                                                       column='PetalLength')
    """
    group_diversities = []
    for name, group in df.groupby(groupby):
        value_counts = group[column].value_counts()
        diversity = len(value_counts) + len(group[column]) - sum(value_counts)
        group_diversities.append(diversity)
    return min(group_diversities)
