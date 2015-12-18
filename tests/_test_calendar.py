# -*- coding: utf-8 -*-
import unittest
import pandas as pd

from agd_tools.calendar.periods import (AnnualDay, OneDayPeriod, MultiPeriod,
    IntervalPeriod)
from agd_tools.calendar.France import Premier_Janvier

__author__ = "Alexis"


four_years = pd.date_range('1/1/2012','31/12/2015', freq='D')
four_years_of_hours = pd.date_range('1/1/2012','31/12/2015', freq='H')


class TestCalendar(unittest.TestCase):

    def _generic_test(self, period, value_for_four_years):
        test_annual = period.build(four_years)
        self.assertEqual(sum(test_annual), value_for_four_years)
        test_hours = period.build(four_years_of_hours)
        self.assertEqual(sum(test_hours), 24*value_for_four_years)

    def test_length(self):
        test_annual = Premier_Janvier.build(four_years)
        test_annual_year = Premier_Janvier.build(four_years_of_hours)
        self.assertEqual(len(test_annual), len(four_years))
        self.assertEqual(len(test_annual_year), len(four_years_of_hours))

    def test_annual(self):
        self._generic_test(Premier_Janvier, 4)

        bissextile = AnnualDay('trick', 29, 2)
        self._generic_test(bissextile, 1)


    def test_punctual(self):
        puntual = OneDayPeriod('punctual', '12/12/2012')
        self._generic_test(puntual, 1)

    def test_interval(self):
        year_interval = IntervalPeriod('a_year', '01/01/2013', '02/01/2014')
        self._generic_test(year_interval, 366)
        test_interval_hours = year_interval.build(four_years_of_hours)
        selected_list = four_years_of_hours[test_interval_hours].tolist()
        self.assertEqual(selected_list[0], pd.datetime(2013,1,1,0))
        self.assertEqual(selected_list[-1], pd.datetime(2014,1,1,23))


if __name__ == '__main__':
    unittest.main()


