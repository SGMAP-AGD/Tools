# -*- coding: utf-8 -*-
"""
Created on Sun May 17 10:59:14 2015

@author: Flogeek
"""
import numpy as np
import pandas as pd

import logging
import time
import datetime
from operator import itemgetter


from collections import Counter
from sklearn.feature_selection import VarianceThreshold
from sklearn.base import TransformerMixin

# Logger #

# -- Initialise logging
def init_logging(log_file_path):
    logging.basicConfig(format='%(message)s', level=logging.INFO, filename=log_file_path)
    logger = logging.getLogger(__name__)


# -- Formated current timestamp
def current_timestamp():
    ts = time.time()
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


# -- Log message with timestamp
def log_info(message):
    ts = time.time()
    logger.info(message + " " + current_timestamp())

############################
#  Preprocessing function  #
############################

# Missing values #
# -- Imputation

class DataFrameImputer(TransformerMixin):
    def __init__(self):
        """Impute missing values.
        Columns of dtype object ('O') are imputed with the most frequent value
        in column.

        Columns of other types are imputed with mean of column.
        """
    def fit(self, X, y=None):
        self.fill = pd.Series([X[col].value_counts().index[0]
            if X[col].dtype == np.dtype('O') else X[col].median() for col in X],
            index=X.columns)
        return self

    def transform(self, X, y=None):
        return X.fillna(self.fill)


# Features function #
# -- get dummies, concat and delete feature

def feature_to_dummy(df, column, drop=False):
    ''' take a serie from a dataframe,
        convert it to dummy and name it like feature_value
        - df is a dataframe
        - column is the name of the column to be transformed
        - if drop is true, the serie is removed from dataframe'''
    tmp = pd.get_dummies(df[column], prefix=column, prefix_sep='_')
    df = pd.concat([df, tmp], axis=1, join_axes=[df.index])
    if drop:
        del df[column]
    return df


def feature_selection(train_instances):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('Crossvalidation started... ')
    selector = VarianceThreshold()
    selector.fit(train_instances)
    logger.info('Number of features used... ' +
                str(Counter(selector.get_support())[True]))
    logger.info('Number of features ignored... ' +
                str(Counter(selector.get_support())[False]))
    return selector


# Basic operations #
def calculate_age_fromyear(year, today=None):
    ''' Calcule l'age en fonction du birthday et de la date d'aujourd'hui
    ou d'une date définie'''
    if today is None:
        today = datetime.date.today()
        age = today.year - int(year)
    else:
        try:
            int(year)
        except ValueError:  # year est parfois 'NC' (non communiqué)
            age = np.nan

    return age


def variation_rate(serie):
    '''returns a basic variation rate y(t) - y(t-1)
    from pandas Series
    '''
    v_rate = serie - serie.shift(1)
    return v_rate


def compute_interactions(df, interacting_feature_name):
    """role: compute interactions between a specific feature
             and other features of the df
       parameters: -DataFrame Pandas containing all the features with whom
                    you want to generate interactions.
                   -string, the name of the feature you want to generate
                    interactions with others.
       returns: - a matrix of the shape [n_row,  2*n_col - 1]
       """

    assert interacting_feature_name in df.columns.tolist()
    other_features_col = df.drop(str(interacting_feature_name),
                                 axis=1).columns.tolist()
    other_features_mat = df.drop(str(interacting_feature_name),
                                 axis=1).as_matrix()

    interacting_feature = df[str(interacting_feature_name)].as_matrix()
    n_other_features = other_features_mat.shape[1]

    res = df.copy()
    for feature in range(0, n_other_features):
        prod = interacting_feature * other_features_mat[:, feature]
        res = np.column_stack((res, prod))

    new_cols = [interacting_feature_name + '_cross_' +
                col for col in other_features_col]
    res_cols = df.columns.tolist() + new_cols
    df_res = pd.DataFrame(res, columns=res_cols)
    return df_res

###################
# Scikit function #
###################


# -- grid_search
def report_grid(grid_scores, n_top=3):
    '''return the 3 best models : score & std(score) on CV samples'''
    top_scores = sorted(grid_scores, key=itemgetter(1), reverse=True)[:n_top]
    for i, score in enumerate(top_scores):
        print("Model with rank: {0}".format(i + 1))
        print("Mean validation score: {0:.3f} (std: {1:.3f})".format(
              score.mean_validation_score,
              np.std(score.cv_validation_scores)))
        print("Parameters: {0}".format(score.parameters))
        print("")


###############
#     geo     #
###############

def point_in_poly(x, y, poly):
    """Determine if a point is inside a given polygon or not
    Polygon is a list of (x,y) pairs. This function
    returns True or False.  The algorithm is called
    the "Ray Casting Method".
    """
    n = len(poly)
    inside = False
    p1x, p1y = poly[0]
    for i in range(n+1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside
