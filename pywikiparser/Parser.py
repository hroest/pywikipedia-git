# -*- coding: utf-8  -*-
""" Mediawiki wikitext parser """
#
# (C) 2007 Merlijn 'valhallasw' van Deen
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id$'

import warnings
import re

import ObjectTree as dom
from BufferedReader import BufferedReader

from Lexer import Lexer, Tokens

_debug = False

def dbgmsg(text):
    if _debug:
        print 'debug> ' + text

class ParseError(Exception):
    """ Parsing Error """

class Parser:
    def __init__(self, data, debug = False):
        global _debug
        _debug = debug

        self.lex = BufferedReader(Lexer(data).lexer())
        
    def expect(self, tokens):
        if not isinstance(tokens, list):
            tokens = [tokens,]
           
        data = self.lex.peek()
        if data[0] in tokens:
            return self.lex.next()[1]
        else:
            raise ParseError('%r is not one of %r' % (data[0], tokens))

    def eat(self, tokens):
        data = ''
        try:
            while(True):
                data += self.expect(tokens)
        except ParseError:
            return data
                
    def parse(self, breaktoken=[]):
        self.root = dom.Element('wikipage')
        self.par = self.root.appendElement('p')
        self.italic = False
        self.bold = False
        
        restore = self.lex.getrestore()
        
        try:
            while(True):
                token = self.lex.peek()
                if token[0] in breaktoken:
                    break

                node = self.parsetoken(token, restore)
                dbgmsg("Adding %r (was %r)" % (node,token))
                self.par.extend(node)
                restore = self.lex.commit(restore)
                
        except StopIteration: pass
        return self.root

    def parsetoken(self, token, restore):
        # The function to call is parser<token>
        exec("data = self.parse%s(restore)" % token[0].name, globals(), locals())
        return data
        
    def parseEOF(self, restore):
        token = self.expect(Tokens.EOF)
        raise StopIteration
    
    # Special functions that directly access the storage tree
        
    def parseNEWPAR(self, restore):
        token = self.expect(Tokens.NEWPAR)
        self.par = self.root.appendElement('p')
        self.bold = False
        self.italic = False
        return []
                
    def parseAPOSTROPHE(self, restore):
        num = len(self.eat(Tokens.APOSTROPHE))
        
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
        
        dbgmsg('bold: %r>%r italic: %r>%r' % (self.bold, newbold, self.italic, newitalic))
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
    
    # Functions that return the input directly
    
    def parseSQRE_CLOSE(self, restore):
        return self.expect(Tokens.SQRE_CLOSE)
        
    def parsePIPE(self, restore):
        return self.expect(Tokens.PIPE)
        
    def parseEQUAL_SIGN(self, restore):
        return self.expect(Tokens.EQUAL_SIGN)
        
    def parseCURL_CLOSE(self, restore):
        return self.expect(Tokens.CURL_CLOSE)

    def parseANGL_CLOSE(self, restore):
        return self.expect(Tokens.ANGL_CLOSE)

    def parseASTERISK(self, restore):
        return self.expect(Tokens.ASTERISK)
        
    def parseCOLON(self, restore):
        return self.expect(Tokens.COLON)
        
    def parseSEMICOLON(self, restore):
        return self.expect(Tokens.SEMICOLON)
        
    def parseHASH(self, restore):
        return self.expect(Tokens.HASH)

    def parseTAB_NEWLINE(self, restore):
        return self.expect(Tokens.TAB_NEWLINE)

    def parseTAB_CLOSE(self, restore):
        return self.expect(Tokens.TAB_CLOSE)
 
    # True parser callers

    def parseWHITESPACE(self, restore):
    	# Todo: 
        return self.parseTEXT(restore)

    def parseTEXT(self, restore):
        text = self.eat([Tokens.TEXT, Tokens.WHITESPACE])

        if text:
            return [text]
        else:
            return []

    def parseSQRE_OPEN(self, restore):
        try:
            return self.parseWikilink()
        except ParseError: pass

        self.lex.undo(restore)
        try:
            return self.parseExternallink()
        except ParseError: pass
        
        self.lex.undo(restore)
        return self.expect(Tokens.SQRE_OPEN)
        
    def parseCURL_OPEN(self, restore):
        try:
            return self.parseTemplateparam()
        except ParseError: pass
        
        self.lex.undo(restore)
        try:
            return self.parseTemplate()
        except ParseError: pass

        self.lex.undo(restore)
        return self.expect(Tokens.CURL_OPEN)
                
    def parseANGL_OPEN(self, restore):
        try:
            return self.parseHTML()
        except ParseError: pass
        
        self.lex.undo(restore)
        return self.expect(Tokens.ANGL_OPEN)

    def parseTAB_OPEN(self, restore):
        try:
            return self.parseWikitable()
        except ParseError: pass
        
        self.lex.undo(restore)
        return self.expect(Tokens.TAB_OPEN)
    
    def parseWikilink(self):
    	retval = dom.Element('')
    	self.expect(Tokens.SQRE_OPEN)
    	self.expect(Tokens.SQRE_OPEN)
    	
    	pre = self.eat(Tokens.SQRE_OPEN)
        if pre:
            retval.append(pre)

        wikilink = retval.appendElement('wikilink')
        # get page title    	
        title = wikilink.appendElement('title')

        #parse title
        title.extend(self.parseTitle(Tokens.SQRE_CLOSE))
        
        self.expect(Tokens.SQRE_CLOSE)
        self.expect(Tokens.SQRE_CLOSE)
        
        return retval
        
        
                
#    	while( titlere.match(next) ):
#    	    title += next
#    	    next = self.lex.peek()
#        
#
#    	    else:
#    	        break
#    	    while(True):
#    	        param = .Element('parameter')
#    	        parampiece = self.parse([Tokens.SQRE_CLOSE, Tokens.PIPE])
#    	        param.extend(parampiece)
#    	        if (self.lex.peek( )[0] == Tokens.SQRE_CLOSE) and
#    	           (self.lex.peek(2)[0] != Tokens.SQRE_CLOSE):   # \][^\]]: a single ]
#    	           param.append('[')
#    	           continue
#    	        else:
#    	            break
#    	    
#    	           
#    	             
#        	    breaktoken = self.lex.peek()
#        	    if breaktoken[0] == Tokens.PIPE:
#    	            break
#    	        elif breaktoken[0] == Tokens.SQRE_CLOSE:
#    	            next = self.lex.peek(2)
#    	            if next[0] == Tokens.SQRE_CLOSE:
#    	                
#        self.expect(Tokens.SQRE_CLOSE)    	
#        self.expect(Tokens.SQRE_CLOSE)
#    	return retval
#    		
        
    def parseExternallink(self):
        raise ParseError("Needs implementation")
    
    def parseTemplateparam(self):
        raise ParseError("Needs implementation")
        
    def parseTemplate(self):
        retval = dom.Element('')
        self.expect(Tokens.CURL_OPEN)
        self.expect(Tokens.CURL_OPEN)
        pre = self.eat(Tokens.CURL_OPEN)
        dbgmsg('pre: ' + pre)
        if pre:
            retval.append(pre)

        wikilink = retval.appendElement('template')
        # get page title    	
        title = wikilink.appendElement('title')
        title.extend(self.parseTitle(Tokens.CURL_CLOSE))
 
        self.expect(Tokens.CURL_CLOSE)
        self.expect(Tokens.CURL_CLOSE)

        return retval
       
        
    def parseHTML(self):
        raise ParseError("Needs implementation")
        
    def parseWikitable(self):
        raise ParseError("Needs implementation")
    
    titlere = re.compile(r"[^\^\]<>\[\|\{\}\n]*$")   	
    def parseTitle(self, closetoken):
        title = dom.Element('title')
        while(True):
            next = self.lex.peek()
            if next[0] == closetoken or next[0] == Tokens.PIPE:
                break
            elif next[0] == Tokens.CURL_OPEN: # allow templates to expand
                restore = self.lex.getrestore()
                data = self.parseCURL_OPEN(restore)
                dbgmsg('Parsed template: %r' % (data,))
                for item in data:
                    if isinstance(item, basestring):
                        if not self.titlere.match(item):
                            raise ParseError('illegal wiki link')
                title.extend(data)
            else:
                next = self.lex.next()
                if not self.titlere.match(next[1]):
                    raise ParseError('illegal wiki link')
                title.append(next[1])
        return title
