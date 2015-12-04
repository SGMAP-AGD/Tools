# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 17:03:10 2015

@author: Alexis

TODO use unittest
"""

import pandas as pd

from agd_tools.calendar.periods import (AnnualDay, PunctualPeriod, MultiPeriod,
    IntervalPeriod)
from agd_tools.calendar.France import Premier_Janvier

four_years = pd.date_range('1/1/2012','31/12/2015', freq='D')
four_years_of_hours = pd.date_range('1/1/2012','31/12/2015', freq='H')

test_annual = Premier_Janvier.build(four_years)
test_annual_year = Premier_Janvier.build(four_years_of_hours)
assert len(test_annual) == len(four_years)
assert len(test_annual_year) == len(four_years_of_hours)
assert sum(test_annual) == 4
assert sum(test_annual_year) == 4*24


test_annual = AnnualDay('trick', 29, 2).build(four_years)
assert len(test_annual) == len(four_years)
assert sum(test_annual) == 1 # :)

test_date = PunctualPeriod('12', '12/12/2012').build(four_years)
assert len(test_annual) == len(four_years)
assert sum(test_annual) == 1

test_interval = IntervalPeriod('a_year', '01/01/2013', '02/01/2014').build(four_years)
test_interval_hours = IntervalPeriod('a_year', '01/01/2013', '02/01/2014').build(four_years_of_hours)
assert len(test_interval) == len(four_years)
assert sum(test_interval) == 366
assert sum(test_interval) == 366*12
selected_list = four_years_of_hours[test_interval_hours].tolist()
assert selected_list[0] == pd.datetime(2013,1,1,0)
assert selected_list[-1] == pd.datetime(2014,1,1,23)


test_date = PunctualPeriod('punctual', '12/12/2012').build(four_years)
assert len(test_annual) == len(four_years)
assert sum(test_annual) == 1


