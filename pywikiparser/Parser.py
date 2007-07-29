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
            
    def expecttext(self):
    	data = self.lex.peek()
    	if data[0] in [Tokens.TEXT, Tokens.WHITESPACE]:
    		return self.lex.next()
    	elif data[0] in [Tokens.EQUAL_SIGN,	Tokens.APOSTROPHE,	Tokens.ASTERISK,
    	                 Tokens.COLON,      Tokens.SEMICOLON,	Tokens.HASH]:
    		data = self.lex.next()
    		return (data[0], data[0].__doc__[0]*data[1])
    	else:
    		raise ParseError('%r is not parsable as text data' % (data[0],))

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
    
    # Special functions that directly access the storage tree
        
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
    
    # Functions that return the input directly
    
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

    def parseASTERISK(self):
        token = self.expect(Tokens.ASTERISK)
        return ['*'*token[1]]
        
    def parseCOLON(self):
        token = self.expect(Tokens.COLON)
        return [':'*token[1]]
        
    def parseSEMICOLON(self):
        token = self.expect(Tokens.SEMICOLON)
        return [';'*token[1]]
        
    def parseHASH(self):
        token = self.expect(Tokens.HASH)
        return ['#'*token[1]]

    def parseTAB_NEWLINE(self):
        token = self.expect(Tokens.TAB_NEWLINE)
        return ['|-']

    def parseTAB_CLOSE(self):
        token = self.expect(Tokens.TAB_CLOSE)
        return ['|}']
        


    # True parser callers

    def parseWHITESPACE(self):
    	# Todo: 
        return self.parseTEXT()

    def parseTEXT(self):
        text = ''
        while(True):
        	try:
        		text += self.expect([Tokens.TEXT, Tokens.WHITESPACE])[1]
        	except ParseError: break

        if text:
            return [text]
        else:
            return []

    def parseSQRE_OPEN(self):
        try:
            return self.parseWikilink()
        except ParseError: pass

        self.lex.undo()
        try:
            return self.parseExternallink()
        except ParseError: pass
        
        self.lex.undo()
        token = self.expect(Tokens.SQRE_OPEN)
        return ['['*token[1]]
        
    def parseCURL_OPEN(self):
        try:
            return self.parseTemplateparam()
        except ParseError: pass
        
        self.lex.undo()
        try:
            return self.parseTemplate()
        except ParseError: pass

        self.lex.undo()
        token = self.expect(Tokens.CURL_OPEN)
        return ['{'*token[1]]
                
    def parseANGL_OPEN(self):
        try:
            return self.parseHTML()
        except ParseError: pass
        
        self.lex.undo()
        token = self.expect(Tokens.ANGL_OPEN)
        return ['<'*token[1]]

    def parseTAB_OPEN(self):
        try:
            return self.parseWikitable()
        except ParseError: pass
        
        self.lex.undo()
        token = self.expect(Tokens.TAB_OPEN)
        return ['{|']
    
    titlere = re.compile(r"[^\^\]#<>\[\|\{\}\n]*$")   
    def parseWikilink(self):
    	retval = dom.Element('')
    	pre = self.expect(Tokens.SQRE_OPEN)[1]-2
    	
    	if pre < 0:
    		raise ParseError("Not enough opening brackets")
    	elif pre > 0:
    		retval.append('['*pre)
    	
    	title = ''
    	while(True):
    		try:
    			data = self.expecttext()[1]
    			print data
    		except ParseError: break
    		if not self.titlere.match(data):
    			raise ParseError("Illegal page title")
    		else:
    			title += data
    	
    	link = retval.appendElement('wikilink')
    	link.appendElement('url').append(title)
    	
    	aft = self.expect(Tokens.SQRE_CLOSE)[1]-2  
    	if aft < 0:
    		raise ParseError("Not enough closing brackets")
    	elif aft > 0:
    		self.lex.push((Tokens.SQRE_CLOSE, aft))
    	 			
    	return retval
    		
        
    def parseExternallink(self):
        raise ParseError("Needs implementation")
    
    def parseTemplateparam(self):
        raise ParseError("Needs implementation")
        
    def parseTemplate(self):
        raise ParseError("Needs implementation")
        
    def parseHTML(self):
        raise ParseError("Needs implementation")
        
    def parseWikitable(self):
    	raise ParseError("Needs implementation")
    	