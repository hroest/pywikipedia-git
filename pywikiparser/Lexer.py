# -*- coding: utf-8  -*-
""" Mediawiki wikitext lexer """
#
# (C) 2007 Merlijn 'valhallasw' van Deen
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id$'

import re

class Token:
    TEXT        = 258       #       Text
    SQRE_OPEN   = 259       # [     Square bracket open
    SQRE_CLOSE  = 260       # ]     Square bracket close
    PIPE        = 261       # |     Pipe symbol
    EQUAL_SIGN  = 262       # =     Equal sign
    APOSTROPHE  = 263       # '     Apostrophe
    CURL_OPEN   = 264       # {     Curly bracket open
    CURL_CLOSE  = 265       # }     Curly bracket close
    ANGL_OPEN   = 266       # <     Angular bracket open
    ANGL_CLOSE  = 267       # >     Angular bracket close
    NEWPAR      = 268       # \n\n  New paragraph
    TAB_OPEN    = 269       # {|    Table opening symbol
    TAB_NEWLINE = 270       # |-    Table new row symbol
    TAB_CLOSE   = 271       # |}    Table closing symbol
    WHITESPACE  = 272       #       Whitespace with max 1 newline
    EOF         = 273       #       End of file

class Lexer:
    """ Lexer class for mediawiki wikitext. Used by the Parser module
    
    >>> l = Lexer('Test with [[wikilink|description]], {{template|parameter\\'s|{{nested}}=booh}}, \n\n new paragraphs, <html>, {| tables |- |}')
    >>> gen = l.lexer()
    >>> [token for token in gen]
    [(258, 'Test'), (272, ' '), (258, 'with'), (272, ' '), (259, 2), (258, 'wikilink'), (261, None), (258, 'description'), (260, 2), (258, ','), (272, ' '), (264, 2), (258, 'template'), (261, None), (258, 'parameter'), (263, 1), (258, 's'), (261, None), (264, 2), (258, 'nested'), (265, 2), (262, 1), (258, 'booh'), (265, 2), (258, ','), (268, ' \n\n '), (258, 'new'), (272, ' '), (258, 'paragraphs,'), (272, ' '), (266, 1), (258, 'html'), (267, 1), (258, ','), (272, ' '), (264, 1), (261, None), (272, ' '), (258, 'tables'), (272, ' '), (270, None), (258, '-'), (271, None), (273, None)]
    """
    
    def __init__(self, string):
        self.data = (a for a in string)
    
    def lexer(self):
        text = ''
        try:
            c = self.getchar()
            while True:
                if (c in ('[', ']', '{', '}', '<', '>', '=', '\'')):
                    if text:
                        yield (Token.TEXT, text)
                        text = ''
                    num = 1
                    try:
                        t = self.getchar()
                        while (t == c):
                            num += 1
                            t = self.getchar()
                            
                    finally:
                        if   (c == '['): yield (Token.SQRE_OPEN,  num)
                        elif (c == ']'): yield (Token.SQRE_CLOSE, num)
                        elif (c == '{'): yield (Token.CURL_OPEN,  num)
                        elif (c == '}'): yield (Token.CURL_CLOSE, num)
                        elif (c == '<'): yield (Token.ANGL_OPEN,  num)
                        elif (c == '>'): yield (Token.ANGL_CLOSE, num)
                        elif (c == '='): yield (Token.EQUAL_SIGN, num)
                        elif (c == '\''): yield(Token.APOSTROPHE, num)
                    c = t
                elif (c == '|'):
                    if text:
                        yield (Token.TEXT, text)
                        text = ''
                    try:
                        t = self.getchar()
                    except StopIteration:
                        yield (Token.PIPE, None)
                        raise
                    
                    if (t == '-'):
                        yield (Token.TAB_NEWLINE, None)
                        c = self.getchar()
                    elif (t == '}'):
                        yield (Token.TAB_CLOSE, None)
                        c = self.getchar()
                    else: 
                        yield (Token.PIPE, None)
                    c = t
                elif re.match('\s', c): # whitespace eater pro (TM)
                    if text:
                        yield (Token.TEXT, text)
                        text = ''
                    ws = ''
                    try:
                        while re.match('\s', c):
                            ws += c
                            c = self.getchar()   #eat up remaining whitespace
                    finally:
                        if (ws.count('\n') > 1):
                            yield (Token.NEWPAR, ws)
                        else:
                            yield (Token.WHITESPACE, ws)
                else:
                    text = text + c
                    c = self.getchar()
        except StopIteration: pass
        if text:
            yield (Token.TEXT, text)
        yield (Token.EOF, None)

    def getchar(self): 
        return self.data.next()