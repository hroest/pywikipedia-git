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
    def __init__(self, name, description):
        self.name = name
        self.__doc__ = description
        
    def __repr__(self):
        return '<T_%s>' % (self.name,)

class Tokens: 
    tokens = [
               ('TEXT',        '      Text data'),
               ('SQRE_OPEN',   '[     Square bracket open'),
               ('SQRE_CLOSE',  ']     Square bracket close'),
               ('PIPE',        '|     Pipe symbol'),
               ('EQUAL_SIGN',  '=     Equal sign'),
               ('APOSTROPHE',  '\'     Apostrophe'),
               ('STAR',        '*     Star sign'),
               ('COLON',       ':     Colon'),
               ('SEMICOLON',   ';     Semicolon'),
               ('HASH',        '#     Hash symbol'),
               ('CURL_OPEN',   '{     Curly bracket open'),
               ('CURL_CLOSE',  '}     Curly bracket close'),
               ('ANGL_OPEN',   '<     Angular bracket open'),
               ('ANGL_CLOSE',  '>     Angular bracket close'),
               ('NEWPAR',      '\n\n  New paragraph'),
               ('TAB_OPEN',    '{|    Table opening symbol'),
               ('TAB_NEWLINE', '|-    Table new row symbol'),
               ('TAB_CLOSE',   '|}    Table closing symbol'),
               ('WHITESPACE',  '      Whitespace with max 1 newline'),
               ('EOF',         '      End of file')
             ]
    for token in tokens:
        exec("%s = Token(%r,%r)" % (token[0], token[0], token[1]), globals(), locals())

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
                if (c in ('[', ']', '{', '}', '<', '>', '=', '\'', '*', ':', ';', '#')):
                    if text:
                        yield (Tokens.TEXT, text)
                        text = ''
                    num = 1
                    try:
                        t = self.getchar()
                        while (t == c):
                            num += 1
                            t = self.getchar()
                            
                    finally:
                        if   (c == '['): yield (Tokens.SQRE_OPEN,  num)
                        elif (c == ']'): yield (Tokens.SQRE_CLOSE, num)
                        elif (c == '{'): yield (Tokens.CURL_OPEN,  num)
                        elif (c == '}'): yield (Tokens.CURL_CLOSE, num)
                        elif (c == '<'): yield (Tokens.ANGL_OPEN,  num)
                        elif (c == '>'): yield (Tokens.ANGL_CLOSE, num)
                        elif (c == '='): yield (Tokens.EQUAL_SIGN, num)
                        elif (c == '\''): yield(Tokens.APOSTROPHE, num)
                        elif (c == '*'): yield (Tokens.STAR,       num)
                        elif (c == ':'): yield (Tokens.COLON,      num)
                        elif (c == ';'): yield (Tokens.SEMICOLON,  num)
                        elif (c == '#'): yield (Tokens.HASH,       num)
                    c = t
                elif (c == '|'):
                    if text:
                        yield (Tokens.TEXT, text)
                        text = ''
                    try:
                        t = self.getchar()
                    except StopIteration:
                        yield (Tokens.PIPE, None)
                        raise
                    
                    if (t == '-'):
                        yield (Tokens.TAB_NEWLINE, None)
                        c = self.getchar()
                    elif (t == '}'):
                        yield (Tokens.TAB_CLOSE, None)
                        c = self.getchar()
                    else:
                        num = 1
                        while (t == c):
                            num += 1
                            t = self.getchar()
                        yield (Tokens.PIPE, num)
                    c = t
                elif re.match('\s', c): # whitespace eater pro (TM)
                    if text:
                        yield (Tokens.TEXT, text)
                        text = ''
                    ws = ''
                    try:
                        while re.match('\s', c):
                            ws += c
                            c = self.getchar()   #eat up remaining whitespace
                    finally:
                        if (ws.count('\n') > 1):
                            yield (Tokens.NEWPAR, ws)
                        else:
                            yield (Tokens.WHITESPACE, ws)
                else:
                    text = text + c
                    c = self.getchar()
        except StopIteration: pass
        if text:
            yield (Tokens.TEXT, text)
        yield (Tokens.EOF, None)

    def getchar(self): 
        return self.data.next()