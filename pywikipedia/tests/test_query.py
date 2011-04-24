#!/usr/bin/python
# -*- coding: utf-8  -*-

"""Unit tests for userlib.py"""
__version__ = '$Id: test_userlib.py 9043 2011-03-13 10:25:08Z xqt $'

import unittest
import tests.test_pywiki

import query


class PyWikiQueryTestCase(tests.test_pywiki.PyWikiTestCase):

    def assertEqualQueryResult(self, params, expectedresult):
        data = query.GetData(params, self.site)
        self.assertEqual(data[u'query'], expectedresult)

    def test_basic(self):
        params = {
            'action': 'query',
            'list': 'users',
            'usprop': ['registration'],
            'ususers': u'Example',
        }
        expectedresult = {u'users': [
        {
            u'userid': 215131,
            u'name': u'Example',
            u'registration': u'2005-03-19T00:17:19Z'
        }
        ]}
        self.assertEqualQueryResult(params, expectedresult)

    def test_titles_multi(self):
        params = {
            'action': 'query',
            'list': 'users',
            'usprop': ['registration'],
            'ususers': u'Example|Example2',
        }
        expectedresult = {u'users': [
        {
            u'userid': 215131,
            u'name': u'Example',
            u'registration': u'2005-03-19T00:17:19Z'
        },
        {
            u'userid': 5176706,
            u'name': u'Example2',
            u'registration': u'2007-08-26T02:13:33Z'
        },
        ]}
        self.assertEqualQueryResult(params, expectedresult)

    def test_titles_list(self):
        params = {
            'action': 'query',
            'list': 'users',
            'usprop': ['registration'],
            'ususers': [u'Example', u'Example2'],
        }
        expectedresult = {u'users': [
        {
            u'userid': 215131,
            u'name': u'Example',
            u'registration': u'2005-03-19T00:17:19Z'
        },
        {
            u'userid': 5176706,
            u'name': u'Example2',
            u'registration': u'2007-08-26T02:13:33Z'
        },
        ]}
        self.assertEqualQueryResult(params, expectedresult)

if __name__ == "__main__":
    unittest.main()
