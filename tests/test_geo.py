#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from agd_tools import geo

__author__ = "Michel"

class TestGeoMethods(unittest.TestCase):

    def test_geo2carto(self):
        phi_deg = 48.853
        lambd_deg = 2.35

        x, y = geo.geo2carto(phi_deg, lambd_deg)

        self.assertTrue(abs(x-652308.4894330197) < 1e-3)
        self.assertTrue(abs(y-6861619.296403129) < 1e-3)

    def test_carto2geo(self):
        x = 652308.4894330197
        y = 6861619.296403129

        phi_deg, lambd_deg = geo.carto2geo(x, y)

        self.assertTrue(abs(phi_deg-48.853) < 1e-10)
        self.assertTrue(abs(lambd_deg-2.35) < 1e-10)

    def test_distance_geo(self):
        phi_a_deg = 48.853
        lambd_a_deg = 2.35
        phi_b_deg = 43.3
        lambd_b_deg = 5.4

        dist = geo.distance_geo(phi_a_deg, lambd_a_deg, phi_b_deg, lambd_b_deg)

        self.assertTrue(abs(dist-660643.0802253289) < 0.2)

    def test_distance_carto(self):
        x_a = 652308.4894330197
        y_a = 6861619.296403129
        x_b = 894831.6918943021
        y_b = 6247506.768682495

        dist = geo.distance_carto(x_a, y_a, x_b, y_b)

        self.assertTrue(abs(dist-660643.0802253289) < 0.2)

if __name__ == '__main__':
    unittest.main()
