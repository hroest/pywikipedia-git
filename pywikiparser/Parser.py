# -*- coding: utf-8  -*-
""" Mediawiki wikitext parser """
#
# (C) 2007 Merlijn 'valhallasw' van Deen
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id$'

import warnings

import ObjectTree as dom
from BufferedReader import BufferedReader

from Lexer import Lexer, Tokens

class ParseError(Exception):
    """ Parsing Error """

class Parser:
    def __init__(self, data):
        self.lex = BufferedReader(Lexer(data).lexer())
        
    def expect(self, tokens):
        if not isinstance(tokens, list):
            tokens = [tokens,]
           
        data = self.lex.peek()
        if data[0] in tokens:
            return self.lex.next()
        else:
            raise ParseError('%r is not one of %r' % (data[0], tokens))

    def parse(self, breaktoken=[]):
        self.root = dom.Element('wikipage')
        self.par = self.root.appendElement('p')
        self.italic = False
        self.bold = False
        try:
            while(True):
                token = self.lex.peek()
                if token[0] in breaktoken:
                    break

                node = self.parsetoken(token)
                print "Adding %r (was %r)" % (node,token)
                self.par.extend(node)
                self.lex.commit()
                
        except StopIteration: pass
        return self.root
        
    def parsetoken(self, token):
        # The function to call is parser<token>
        exec("data = self.parse%s()" % token[0].name, globals(), locals())
        return data
        
    def parseEOF(self):
        token = self.expect(Tokens.EOF)
        raise StopIteration
        
    def parseNEWPAR(self):
        token = self.expect(Tokens.NEWPAR)
        self.par = self.root.appendElement('p')
        self.bold = False
        self.italic = False
        return []
                
    def parseAPOSTROPHE(self):
        token = self.expect(Tokens.APOSTROPHE)
        num = token[1]
        
        #prepare length
        if (num == 1):
            self.par.append('\'')
        elif (num == 4):
            self.par.append('\'')
            num = 3
        elif (num > 5):
            self.par.append('\'' * (num-5))
            num = 5
        
        # determine changes
        newitalic = self.italic
        newbold  = self.bold
        
        if num == 2: #toggle italic
            newitalic = not self.italic
        elif num == 3: #toggle bold
            newbold  = not self.bold
        elif num == 5: #toggle both
            newitalic = not self.italic
            newbold = not self.bold
        
        print 'bold: %r>%r italic: %r>%r' % (self.bold, newbold, self.italic, newitalic)
        if self.italic and not newitalic:
            if self.par.name == 'i' or not newbold:
                self.par = self.par.parent
            else:
                self.par = self.par.parent.parent.appendElement('b')
            self.italic = False
        if self.bold and not newbold:
            if self.par.name == 'b' or not newitalic:
                self.par = self.par.parent
            else:
                self.par = self.par.parent.parent.appendElement('i')
            self.bold = False
        if not self.italic and newitalic:
            self.par = self.par.appendElement('i')
            self.italic = True
        if not self.bold and newbold:
            self.par = self.par.appendElement('b')   
            self.bold = True
        return []     
    
    def parseSQRE_CLOSE(self):
        token = self.expect(Tokens.SQRE_CLOSE)
        return [']'*token[1]]
        
    def parsePIPE(self):
        token = self.expect(Tokens.PIPE)
        return ['|'*token[1]]
        
    def parseEQUAL_SIGN(self):
        token = self.expect(Tokens.EQUAL_SIGN)
        return ['='*token[1]]
        
    def parseCURL_CLOSE(self):
        token = self.expect(Tokens.CURL_CLOSE)
        return ['}'*token[1]]

    def parseANGL_CLOSE(self):
        token = self.expect(Tokens.ANGL_CLOSE)
        return ['>'*token[1]]

    def parseTAB_NEWLINE(self):
        token = self.expect(Tokens.TAB_NEWLINE)
        return ['|-']

    def parseTAB_CLOSE(self):
        token = self.expect(Tokens.TAB_CLOSE)
        return ['|}']

    def parseWHITESPACE(self):
        return self.parseTEXT()

    def parseTEXT(self):
        text = ''
        try:
            while(True):
                text += self.expect([Tokens.TEXT, Tokens.WHITESPACE])[1]
        except ParseError: pass
        if text:
            return [text]
        else:
            return []

    def parseSQRE_OPEN(self):
        token = self.expect(Tokens.SQRE_OPEN)
    def parseCURL_OPEN(self):
        token = self.expect(Tokens.CURL_OPEN)
    def parseANGL_OPEN(self):
        token = self.expect(Tokens.ANGL_OPEN)
    def parseTAB_OPEN(self):
        token = self.expect(Tokens.TAB_OPEN)



        
             