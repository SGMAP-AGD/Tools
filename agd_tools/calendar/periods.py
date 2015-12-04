# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 12:01:08 2015

Ce fichier se décompose en deux parties.
La première crée des objets utiles qui permette d'ajouter facilement des éléments
temporel à une analyse.
La seconde crée des évenements standard.

TODO: add a name attribute in period object and use it in build_period_dummies


@author: Alexis
"""

import pandas as pd


def check_is_date(date):
    # TODO: assert date is a date
    return not isinstance(date, list) and not isinstance(date, tuple)


class Period(object):

    def __init(self, name, zone):
        self.name = name
        self.zone = zone

    def build(self):
        raise NotImplementedError


def guess_Period_type(obj, name, zone):
    ''' chaque periode est associée à un format pour l'instant
        cette fonction retourne l'objet correspondant:
        - PunctualPeriod
        - AnnualPeriod
        - IntervalPeriod
    '''
    if check_is_date(obj):
        return PunctualPeriod(name, obj, zone)
    else:
        assert isinstance(obj, list) or isinstance(obj, tuple)
        if len(obj) == 1:
            return  PunctualPeriod(name, obj[0], zone)
        if len(obj) == 2:
            return  IntervalPeriod(name, obj[0], obj[1], zone)
        if len(obj) > 2:
            raise Exception('Impossible de déterminer un objet ' +
                'de type Period correspondant à ', obj
                )


class PunctualPeriod(Period):
    def __init__(self, name, date, zone=None, dayfirst=False):
        assert check_is_date(date)
        self.name = name
        self.date = date
        self.zone = zone

    def build(self, date, zone=None):
        date_condition = (date == self.date)
        date_condition = pd.Series(date_condition, name=self.name)
        if self.zone is not None:
            if zone is not None:
                return date_condition*(zone == self.zone)
        else:
            return date_condition


class IntervalPeriod(Period):
    '''following python stadard, start is included in the period, end is not'''
    def __init__(self, name, start, end, zone=None, dayfirst=False):
        assert check_is_date(start)
        assert check_is_date(end)
        self.name = name
        self.start = start
        self.end = end
        self.zone = zone

    def build(self, date, zone=None):
        import pdb; pdb.set_trace()
        date_condition = (date >= self.start) & (date < self.end)
        date_condition = pd.Series(date_condition, name=self.name)
        if self.zone is not None:
            if zone is not None:
                return date_condition*(zone == self.zone)
        return date_condition

class AnnualDay(Period):
    def __init__(self, name, day, month, zone=None, dayfirst=False):
        self.name = name
        self.day = day
        self.month = month
        self.zone = zone

    def build(self, date, zone=None):
        date_condition = (date.day == self.day) & (date.month == self.month)
        date_condition = pd.Series(date_condition, name=self.name)
        if self.zone is not None:
            if zone is not None:
                return date_condition*(zone == self.zone)
            else:
                print("il y a une condition de localisation. Sans varaible " +
                'de position, on la suppose vérifiée')
        return date_condition


class MultiPeriod(Period):
    ''' a Period with multiple condition
        Be aware that if there is a zone, it should be the same for
        all periods
    '''
    def __init__(self, name, list_of_periods, zone=None, dayfirst=False):
        assert isinstance(list_of_periods, list)
        self.name = name
        self.periods = []
        for period in list_of_periods:
            if isinstance(period, Period):
                self.periods += period
            else:
                self.periods.append(guess_Period_type(period, name, zone))

        zone = self.periods[0].zone
        assert all([x.zone == zone for x in self.periods])

    def build(self, date, zone=None):
        condition = pd.Series(False, range(len(date)), name=self.name)
        for period in self.periods:
            condition = condition | period.build(date, zone)
        return condition


def build_period_dummies(df, list_of_periods,
                         date_column=None, zone_column=None):
    ''' Calculate period based dummies-features
        - df is a pandas data_frame
        - list_of_date is a list of objects used to defined period and dummy
        - date_column is the column of reference. It's from that column than
            the dummies will be build.
            If None, the Index is used.
            In both case, it's supposed to be DatetimeIndex compatible
        - zone_columns is the columns containing the geographical information
           More work could be done on that point since the zone could have
           various aspect and could be different for each period
    '''
    if not isinstance(list_of_periods, list):
        assert isinstance(list_of_periods, Period)
        list_of_periods = [list_of_periods]
    assert isinstance(list_of_periods, list)
    for period in list_of_periods:
        assert isinstance(period, Period)

    if date_column is None:
        date = df.index
    else:
        date = df[date_column]

    date = pd.DatetimeIndex(date)
    if zone_column is not None:
        zone = df[zone_column]
    else:
        zone = None

    for period in list_of_periods:
        df[period.name] = period.build(date, zone).values

    return df

#    # -- Jours particuliers
#    ts['dayofmonth'] = date.day
#    ts['dayofweek'] = date.dayofweek
#    ts['weekend'] = (ts.dayofweek.isin([5, 6])).astype('int')


