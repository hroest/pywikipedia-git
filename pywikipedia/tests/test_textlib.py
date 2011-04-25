#!/usr/bin/python
# -*- coding: utf-8  -*-

"""Unit tests for pywikibot/textlib.py"""
__version__ = '$Id$'

import unittest
from tests.test_pywiki import PyWikiTestCase

import wikipedia as pywikibot
import pywikibot.textlib as textlib
import catlib


class PyWikiTextLibTestCase(PyWikiTestCase):

    result1 = '[[Category:Cat1]]\r\n[[Category:Cat2]]\r\n'

    def setUp(self):
        self.site = pywikibot.getSite('en', 'wikipedia')
        self.data = [catlib.Category(self.site, 'Category:Cat1'),
                     catlib.Category(self.site, 'Category:Cat2')]

    def test_categoryFormat_raw(self):
        self.assertEqual(self.result1,
                         textlib.categoryFormat(['[[Category:Cat1]]',
                                                 '[[Category:Cat2]]'],
                                                self.site))

    def test_categoryFormat_bare(self):
        self.assertEqual(self.result1,
                         textlib.categoryFormat(['Cat1', 'Cat2'], self.site))

    def test_categoryFormat_Category(self):
        self.assertEqual(self.result1,
                         textlib.categoryFormat(self.data, self.site))

    def test_categoryFormat_Page(self):
        data = [pywikibot.Page(self.site, 'Category:Cat1'),
                pywikibot.Page(self.site, 'Category:Cat2')]
        self.assertEqual(self.result1, textlib.categoryFormat(self.data,
                                                              self.site))

    def assertEqualCategoryRoundtrip(self, text, catcount):
        cats = textlib.getCategoryLinks(text)
        self.assertEqual(len(cats), catcount)
        self.assertEqual(text, textlib.replaceCategoryLinks(text,
                                                            cats,
                                                            site = self.site))

    def test_replaceCategoryLinks(self):
        self.assertEqualCategoryRoundtrip(self.result1,2)

    def test_replaceCategoryLinks1(self):
        result = 'Blah\r\n\r\n[[Category:Cat1]]\r\n[[Category:Cat2]]\r\n'
        self.assertEqualCategoryRoundtrip(result,2)

    def test_replaceCategoryLinks2(self):
        result = 'Blah\r\n\r\n[[Category:Cat1]]\r\n[[Category:Cat2]]\r\n\r\n[[fr:Test]]\r\n'
        self.assertEqualCategoryRoundtrip(result,2)

if __name__ == "__main__":
    unittest.main()
