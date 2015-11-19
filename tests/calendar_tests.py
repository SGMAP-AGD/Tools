# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 17:03:10 2015

@author: Alexis

TODO use unittest
"""

import pandas as pd

from agd_tools import calendar

four_years = pd.date_range('1/1/2012','31/12/2015', freq='D')
four_years_of_hours = pd.date_range('1/1/2012','31/12/2015', freq='H')

test_annual = calendar.Premier_Janvier.build(four_years)
test_annual_year = calendar.Premier_Janvier.build(four_years_of_hours)
assert len(test_annual) == len(four_years)
assert len(test_annual_year) == len(four_years_of_hours)
assert sum(test_annual) == 4
assert sum(test_annual_year) == 4*24


test_annual = calendar.AnnualDay(29,2).build(four_years)
assert len(test_annual) == len(four_years)
assert sum(test_annual) == 1 # :)

test_date = calendar.PunctualPeriod('12/12/2012').build(four_years)
assert len(test_annual) == len(four_years)
assert sum(test_annual) == 1

test_interval = calendar.IntervalPeriod('01/01/2012', '02/01/2013').build(four_years)
assert len(test_interval) == len(four_years)
assert sum(test_interval) == 366

test_date = calendar.PunctualPeriod('12/12/2012').build(four_years)
assert len(test_annual) == len(four_years)
assert sum(test_annual) == 1
