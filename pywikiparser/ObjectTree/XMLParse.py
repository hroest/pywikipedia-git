# -*- coding: utf-8  -*-
"""
Simple object tree system for python.
This module contains the XML parser
"""
#
# (C) 2007 Merlijn 'valhallasw' van Deen
#
# Distributed under the terms of the MIT license.
#
__version__ = u'$Id$'

import warnings
import xml.sax

import Element

class XMLParser(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.root = Element('root')
        self.currentNode = self.root
        
    def startElement(self, name, attrs):
        self.currentNode = self.currentNode.appendElement(name, dict(attrs.items()))
            
    def endElement(self, name):
        if self.currentNode.name == name:
            self.currentNode = self.currentNode.parent
        else:
            warnings.warn("Parse warning: recieved </%s>, expected </%s>." % (name, self.currentNode.name))

    def characters(self, data):
        self.currentNode.append(data)

def parseText(data):
    """ Parses XML Text data to an object tree.
    Examples:
    >>> text = '<root>Hello, <bold>this</bold> is a test! <link rel="blah" /></root>'
    >>> tree = parseText(text)
    >>> tree
    <'root' element: {} [u'Hello, ', <'bold' element: {} [u'this']>, u' is a test! ', <'link' element: {u'rel': u'blah'} []>]>
    >>> tree.toxml()
    u'<root>Hello, <bold>this</bold> is a test! <link rel="blah"/></root>'
    
    >>> parseText("<root><nonclosed></root>")
    Traceback (most recent call last):
      ...
    SAXParseException: <unknown>:1:19: mismatched tag
    """
    handler = XMLParser()
    xml.sax.parseString(data, handler)
    return handler.root[0]