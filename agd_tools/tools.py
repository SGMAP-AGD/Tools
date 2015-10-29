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

def feature_to_dummy(df, feature, drop):
    ''' take a feature from a dataframe, convert it to dummy and name it like feature_value'''
    v_drop = drop
    tmp = pd.get_dummies(df[feature], prefix=feature, prefix_sep='_')
    df = pd.concat([df, tmp], axis=1, join_axes=[df.index])
    if v_drop is True:
        del df[feature]
    else:
        pass
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


# Others #
def calculate_age_fromyear(year, today=None):
    ''' Calcule l'age en fonction du birthday et de la date d'aujourd'hui
    ou d'une date définie'''
    if today is None:
        today = date.today()
        age = today.year - int(year)
    else:
        try:
            int(year)
        except ValueError:  # year est parfois 'NC' (non communiqué)
            age = np.nan

    return age


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
