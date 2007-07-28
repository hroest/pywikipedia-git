# -*- coding: utf-8  -*-
""" Mediawiki wikitext parser """
#
# (C) 2007 Merlijn 'valhallasw' van Deen
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id$'

# 

import re
import warnings

import ObjectTree as dom

from Lexer import Lexer, Token


# System loosely based on 'the dragon book':
# Compilers, Principles, Techniques and Tools, Aho, Sethi, Ullman, 1st edition, 1986

class ParseError(Exception):
    """ booh """

class parser:
    def __init__(self, string):
        self.wikipwn = [a for a in lexer(string).lexer()]
        self.counter = 0
    
    def expect(self, types, values=None):
        #print 'Expect: %s %s' % (types, values)
        token = self.wikipwn[self.counter]
        if (token[0] not in types):
            if values:
                raise ParseError("Expected one of (%r, %r), got %r" % (types, values, token))
            else:
                raise ParseError("Expected one of (%r), got %r" % (types, token))
        if values:
            if (token[1] not in values):
                raise ParseError("Expected one of (%r, %r), got %r" % (types, values, token))
        self.counter += 1
        return token

    def parsetext(self):
        data = ''
        try:
            while(True): data += self.expect([lexer.TEXT, lexer.WHITESPACE])[1]
        except ParseError, e: pass
        
        k = dom.Element('parsetext')
        k.append(data)
        return k
    
    def parseurl(self):
        pre = self.expect([lexer.SQRE_OPEN])[1]-1
        url = self.expect([lexer.TEXT])[1]
        # checkurl, raise ParseError
        ws = ''
        try:
            ws = self.expect([lexer.WHITESPACE])[1]
        except ParseError: pass

        if '\n' in ws:
            raise ParseError('No newlines allowed in external links')
            
        desc = ''
        try:
            while(True): desc += self.expect([lexer.TEXT, lexer.WHITESPACE])[1]
        except ParseError, e: pass
        
        aft = self.expect([lexer.SQRE_CLOSE])[1]-1
        
        root = dom.Element('parseurl')
        root.append('['*pre)
        extlink = root.appendElement('externallink')
        extlink.appendElement('url').append(url)
        if len(desc) > 0:
            extlink.appendElement('description').append(desc)
        root.append(']'*aft)
        
        return root
    
    def parsewikilink(self):
        pre = self.expect([lexer.SQRE_OPEN])[1]-2
        if (pre < 0): raise ParseError('Not a wiki link')
        
        page = ''
        try:
            while(True): page += self.expect([lexer.TEXT, lexer.WHITESPACE])[1]
        except ParseError,e: pass
        # if not re.match(...): raise ParseError

        root = dom.Element('parsewikilink')
        root.append('['*pre)
        pagelink = root.appendElement('pagelink')
        pagelink.appendElement('title').append(page)
        print 'wikilink: %s' % page
        try:
            while(True):
                root.append(self.parseparameter(breaktokens=[lexer.SQRE_CLOSE]))
        except ParseError, e: pass
        print 'result: %r' % (root,)
        aft = self.expect([lexer.SQRE_CLOSE])[1]-2
        if (aft < 0):
            raise ParseError('Not a wiki link')
            
        root.append(']'*aft)
        return root
    
    def parseparameter(self, breaktokens=None):
        if breaktokens:
            breaktokens.append(lexer.PIPE)
        else:
            breaktokens = [lexer.PIPE]
        try:
            while(True): self.expect([lexer.WHITESPACE]) #eat whitespace
        except ParseError: pass
        self.expect([lexer.PIPE])
        #now we can expect anything except a loose pipe.
        data = self.parse(breaktokens=breaktokens)
        return dom.Element('parameter', {}, data)
        
    def parseone(self, breaktokens=[]):
        token = self.wikipwn[self.counter]
        if (token[0] == lexer.EOF) or (token[0] in breaktokens):
            raise StopIteration
            
        if (token[0] == lexer.TEXT or token[0] == lexer.WHITESPACE): #text
            try: return self.parsetext();
            except ParseError, e: pass
            
        if (token[0] == lexer.SQRE_OPEN): #wikilink or external link
            begin = self.counter
            try: return self.parsewikilink();
            except ParseError, e: pass
            self.counter = begin
            try: return self.parseurl();
            except ParseError, e: pass
            self.counter = begin
            return ('[' * self.expect([lexer.SQRE_OPEN])[1])
            
        if (token[0] == lexer.SQRE_CLOSE):
            return ']'*self.expect([lexer.SQRE_CLOSE])[1]
        
        if (token[0] == lexer.PIPE):
            self.expect([lexer.PIPE])
            return '|'
            
        if (token[0] == lexer.CURL_OPEN):
            #parse_template
            warnings.warn("Not implemented yet. Returning string")
            return '{'*self.expect([lexer.CURL_OPEN])[1]
            
        if (token[0] == lexer.CURL_CLOSE):
            return '}'*self.expect([lexer.CURL_CLOSE])[1]
        
        if (token[0] == lexer.ANGL_OPEN):
            #parse html
            warnings.warn("Not implemented yet. Returning string")
            return '<'*self.expect([lexer.ANGL_OPEN])[1]
        
        if (token[0] == lexer.ANGL_CLOSE):
            return '>'*self.expect([lexer.ANGL_CLOSE])[1]
            
        if (token[0] == lexer.NEWPAR):
            self.expect([lexer.NEWPAR])
            return '\n\n'
            
        if (token[0] == lexer.TAB_OPEN):
            # parse wikitable
            warnings.warn("Not implemented yet. Returning string")
            self.expect([lexer.TAB_OPEN])
            return '(|'
            
        if (token[0] == lexer.TAB_NEWLINE):
            self.expect([lexer.TAB_NEWLINE])
            return '|-'
            
        if (token[0] == lexer.TAB_CLOSE):
            self.expect([lexer.TAB_CLOSE])
            return '|}'
            
        if (token[0] == lexer.WHITESPACE):
            return self.expect([lexer.WHITESPACE])[1]
            
        if (token[0] == lexer.EQUAL_SIGN):
            return '='*self.expect([lexer.EQUAL_SIGN])[1]
        
        if (token[0] == lexer.APOSTROPHE):
            return '\''*self.expect([lexer.APOSTROPHE])[1]
        
        else:
            raise Exception, 'ZOMG THIS CANNOT HAPPEN'     
            
    def parseonegenerator(self, *args, **kwargs):
        while(True):
            yield self.parseone(*args, **kwargs)
            
    def parse(self, *args, **kwargs):
        root = dom.Element('wikipage')
        for data in self.parseonegenerator(*args, **kwargs):
            root.extend(data)
        return root

            
        
    