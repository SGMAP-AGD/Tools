# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 12:01:08 2015

Ce fichier se décompose en deux parties.
La première crée des objets utiles qui permette d'ajouter facilement des éléments
temporel à une analyse.
La seconde crée des évenements standard.

TODO: add a name attribute in period object and use it in build_period_dummies


@author: Flo, Alexis
"""

import pandas as pd

# --  Données calendaires : 2012, 2013 et 2014 / vacances zone C
class Period(object):

    def build(self):
        raise NotImplementedError


def check_is_date(date):
    # TODO: assert date is a date
    return not isinstance(date, list) and not isinstance(date, tuple)


def guess_Period_type(obj, zone):
    ''' chaque periode est associée à un format pour l'instant
        cette fonction retourne l'objet correspondant:
        - PunctualPeriod
        - AnnualPeriod
        - IntervalPeriod
    '''
    if check_is_date(obj):
        return PunctualPeriod(obj, zone)
    else:
        assert isinstance(obj, list) or isinstance(obj, tuple)
        if len(obj) == 1:
            return  PunctualPeriod(obj[0], zone)
        if len(obj) == 2:
            return  IntervalPeriod(obj[0], obj[1], zone)
        if len(obj) > 2:
            raise Exception('Impossible de déterminer un objet ' + 
                'de type Period correspondant à ', obj
                )    


class PunctualPeriod(Period):
    def __init__(self, date, zone=None):        
        assert check_is_date(date)
        self.date = date
        self.zone = zone

    def build(self, date, zone=None):
        date_condition = (date == self.date)
        if self.zone is not None:
            assert zone is not None
            return date_condition*(zone == self.zone)
        else:
            return date_condition
    

class IntervalPeriod(Period):
    '''following python stadard, start is included in the period, end is not'''
    def __init__(self, start, end, zone=None):
        assert check_is_date(start)
        assert check_is_date(end)
        self.start = start
        self.end = end
        self.zone = zone

    def build(self, date, zone=None):
        date_condition = (date >= self.start) & (date < self.end)
        if self.zone is not None:
            assert zone is not None
            return date_condition*(zone == self.zone)
        else:
            return date_condition

class AnnualDay(Period):
    def __init__(self, day, month, zone=None):
        self.day = day
        self.month = month
        self.zone = zone
        
    def build(self, date, zone=None):
        date_condition = (date.day == self.day) & (date.month == self.month)
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
    def __init__(self, list_of_periods, zone=None):
        assert isinstance(list_of_periods, list)
        self.periods = []
        for period in list_of_periods:
            if isinstance(period, Period):
                self.periods += period
            else:
                self.periods.append(guess_Period_type(period, zone))

        zone = self.periods[0].zone
        assert all([x.zone == zone for x in self.periods])    

    def build(self, date, zone=None):
        condition = pd.Series(False, len(date))
        for point in self.points:
            condition = condition | point.build(date, zone)
        return condition
        
        
def build_period_dummies(df, list_of_periods,
                         date_columns=None, zone_column=None):
    ''' Calculate period based dummies-features
        - df is a pandas data_frame
        - list_of_date is a list of objects used to defined period and dummy
        - date_columns is the column of reference. It's from that column than
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

    if date_columns is None:
        date = df.index
    else:
        date = df[date_columns]

    date = pd.DatetimeIndex(date)
    if zone_column is not None:
        zone = df[zone_column]
    else:
        zone = None
    
    count = 0
    for period in list_of_periods:
        df['period' + str(count)] = period.build(date, zone)
    
#    if(date_col is not None):
#        if any(date_col in col for col in ts.columns):
#            ts.set_index(date_col, inplace=True)
#        else:
#            raise Exception('The column \'date_col\' you entered is not in the DataFrame')
#
#    if(type(date) != pd.DatetimeIndex):
#        raise Exception('date_col column must be in the pd.DateTimeIndex format')
    return df
#
#    # -- Jours particuliers
#    ts['dayofmonth'] = date.day
#    ts['dayofweek'] = date.dayofweek
#    ts['weekend'] = (ts.dayofweek.isin([5, 6])).astype('int')
#
#    # -- Saisons (TODO or not)
#
#    # -- Vacances scolaires (2012) - Zone C
#    vac_toussain = ((date >= '2012-10-27') & (date < '2012-11-13')) + ((date >= '2013-10-19') & (date < '2013-11-04')) + ((date >= '2014-10-18') & (date < '2014-11-03'))
#    vac_noel = ((date >= '2012-12-22') & (date < '2013-01-08')) + ((date >= '2013-12-21') & (date < '2014-01-06')) + ((date >= '2014-12-20') & (date < '2015-01-05'))
#    vac_hiver = ((date >= '2013-03-02') & (date < '2013-03-18')) + ((date >= '2014-02-15') & (date < '2014-03-03')) + ((date >= '2015-02-21') & (date < '2015-03-09'))
#    vac_printemps = ((date >= '2013-04-27') & (date < '2013-05-13')) + ((date >= '2014-04-12') & (date < '2014-04-28')) + ((date >= '2015-04-25') & (date < '2015-05-11'))
#    vac_ete = ((date >= '2013-07-06') & (date < '2014-09-03')) + ((date >= '2014-07-05') & (date < '2015-09-02')) + ((date >= '2015-07-03') & (date < '2015-09-01'))
#
#    ts['vacances'] = (vac_toussain + vac_noel + vac_hiver + vac_printemps + vac_ete).astype('int')
#
#    # -- Fêtes nationales / jours fériés
#
#    dates_jours_feries =['2012-09-01', '2013-09-01', '2014-09-01'] + ['2012-09-11', '2013-09-11', '2014-09-11'] + \
#                         ['2012-12-25', '2013-12-25', '2014-12-25'] + ['2012-12-31', '2013-12-31', '2014-12-31']
Premier_Janvier = AnnualDay(1,1)
Premier_Mai = AnnualDay(1,5)
Huit_Mai = AnnualDay(8,5)
Lundi_de_Paques = MultiPeriod(['2012-04-09', '2013-04-01', '2014-04-21', '2015-04-06'])
Jeudi_Ascension = MultiPeriod(['2012-05-17', '2013-05-19', '2014-05-29', '2015-05-14'])
Lundi_Pentecote = MultiPeriod(['2012-05-28', '2013-05-20', '2014-05-29', '2015-05-25'])
Quatorze_Juillet = AnnualDay(14,7)
Assomption = AnnualDay(15,8)
Tousaint = AnnualDay(1,11)
Onze_Novembre = AnnualDay(11,11)
Noel = AnnualDay(25,12)
Fete_Musique = AnnualDay(21,6)
Nuit_Blanche = None # TODO:

vac_toussain = MultiPeriod([('2012-10-27','2012-11-13'), ('2013-10-19','2013-11-04'),('2014-10-18','2014-11-03')])
vac_noel = MultiPeriod([('2012-12-22','2013-01-08'),('2013-12-21','2014-01-06'),('2014-12-20','2015-01-05')])
vac_hiver = MultiPeriod([('2013-03-02','2013-03-18'),('2014-02-15','2014-03-03'),('2015-02-21','2015-03-09')])
vac_printemps = MultiPeriod([('2013-04-27','2013-05-13'),('2014-04-12','2014-04-28'),('2015-04-25','2015-05-11')])
vac_ete = MultiPeriod([('2013-07-06','2014-09-03'),('2014-07-05','2015-09-02'),('2015-07-03','2015-09-01')])
