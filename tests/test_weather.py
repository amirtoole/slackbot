#!/usr/bin/env python
# vim: set expandtab ts=4 sw=4:

# Copyright (C) 2011 Ian Gable
# You may distribute under the terms of either the GNU General Public
# License or the Apache v2 License, as specified in the README file.

# This is a testing version of the weatherca CLI. It's used mostly for
# experimentation with new features. Don't expect it to work.

## Auth.: Ian Gable

## Modified by Amir Toole for Python 3 compatiblity

import sys
import unittest
from optparse import OptionParser

from utils.weather import City, CityIndex


class MyTestCase(unittest.TestCase):
    def test_weather(self):
        parser = OptionParser(usage="%prog -c CITY -q QUANTITY", version="%prog 1.0.0")

        parser.add_option("-c", "--city", dest="city",
                          help="The City you want information about", metavar="CITY")
        parser.add_option("-q", "--quantity", dest="quantity",
                          help="the particular quatity toy want to know", metavar="QUANTITY")
        parser.add_option("-l", "--list", action="store_true", dest="list",
                          help="Show a list of the available cities")
        (options, args) = parser.parse_args()

        quantity = "currentConditions/temperature"

        cityindex = CityIndex()

        city = "Calgary"

        if options.quantity:
            quantity = options.quantity

        if cityindex.is_city(city):
            cityObject = City(cityindex.data_url(city))
            if not options.quantity:
                print("No requested quantity given, using temperature")
                print(quantity + " is: " + cityObject.get_quantity(quantity))


if __name__ == '__main__':
    unittest.main()
