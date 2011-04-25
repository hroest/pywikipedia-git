#!/usr/bin/python
# -*- coding: utf-8  -*-

"""Unit tests for pywikibot/textlib.py"""
__version__ = '$Id$'

import unittest
import tests.test_pywiki

import wikipedia as pywikibot
import pywikibot.textlib as textlib
import catlib


class PyWikiTextLibTestCase(tests.test_pywiki.PyWikiTestCase):

    result1 = '[[Category:Cat1]]\r\n[[Category:Cat2]]\r\n'

    def test_categoryFormat_raw(self):
        self.assertEqual(self.result1,
                         textlib.categoryFormat(['[[Category:Cat1]]',
                                                 '[[Category:Cat2]]'],
                                                self.site))

    def test_categoryFormat_bare(self):
        self.assertEqual(self.result1,
                         textlib.categoryFormat(['Cat1', 'Cat2'], self.site))

    def test_categoryFormat_Category(self):
        data = [catlib.Category(self.site, 'Category:Cat1'),
                catlib.Category(self.site, 'Category:Cat2')]
        self.assertEqual(self.result1, textlib.categoryFormat(data, self.site))

    def test_categoryFormat_Page(self):
        data = [pywikibot.Page(self.site, 'Category:Cat1'),
                pywikibot.Page(self.site, 'Category:Cat2')]
        self.assertEqual(self.result1, textlib.categoryFormat(data, self.site))

if __name__ == "__main__":
    unittest.main()
