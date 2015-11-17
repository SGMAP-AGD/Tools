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


def _l_diversity(x):
    nb_distinct_without_na = x.nunique(dropna=True)
    # each na can be considered as a distinct value
    nb_of_na = sum(x.isnull())
    return nb_distinct_without_na + nb_of_na


def get_diversities(df, groupby, column):
    """
        Return the diversity level of a column in a dataframe.

        A simple implementation of distinct l-diversity.

        This implementation takes None values as distinct modalities.

        You should replace all invalid, unknown and false rows by None
        before using this function

        Aggarwal, Charu C.; Yu, Philip S. (2008):
        "A General Survey of Privacy"
        http://charuaggarwal.net/generalsurvey.pdf
        Springer. ISBN 978-0-387-70991-8.

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
    grp = df.groupby(groupby)
    res = grp[column].agg({'l_diversity' : _l_diversity })
    return res


def get_l(df, groupby, column):
    return min(get_diversities(df, groupby, column)['l_diversity'])


def diversity_distribution(df, groupby, column):
    diversity = get_diversities(df, groupby, column)['l_diversity']
    return diversity.value_counts().sort_index()


def less_diverse_groups(df, groupby, column):
    grp = df.groupby(groupby)
    res = grp[column].agg({'l_diversity' : _l_diversity })
    diversity = res['l_diversity']
    select = diversity[diversity == min(diversity)]
    results = []
    for group_index in select.index:
        results += [grp.get_group(group_index)]
    return results

