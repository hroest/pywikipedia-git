# -*- coding: utf-8  -*-
"""
Simple object tree system for python.
This module contains the Element class
"""
#
# (C) 2007 Merlijn 'valhallasw' van Deen
#
# Distributed under the terms of the MIT license.
#
__version__ = u'$Id$'

class Element(list):
    """
    Element in the element tree. Usage examples:
    
    >>> book = Element(u'book', {u'title': u'Wikitext Parsing', u'authors': u'valhallasw'})
    >>> chapter = Element(u'chapter', {u'title': u'Wikitext'})
    >>> section = chapter.appendElement(u'section', {u'title': u'Basic principles of wikitext'})
    >>> book.append(chapter)
    >>> section.append(u'Wikitext was created as a way to implement formatting in plain text files, in a user friendly way. ....')
    >>> book.toxml()
    u'<book authors="valhallasw" title="Wikitext Parsing"><chapter title="Wikitext"><section title="Basic principles of wikitext">Wikitext was created as a way to implement formatting in plain text files, in a user friendly way. ....</section></chapter></book>'
    >>> print book.toxml(True, symbol=u'    ')
    <book authors="valhallasw" title="Wikitext Parsing">
        <chapter title="Wikitext">
            <section title="Basic principles of wikitext">
                Wikitext was created as a way to implement formatting in plain text files, in a user friendly way. ....
            </section>
        </chapter>
    </book>
    """
    
    def __init__(self, element_name, element_attributes={}, contents=[]):
        self.name = element_name
        self.attributes = element_attributes
        self.parent = None
        for item in contents:
            self.append(item)
        
    def toxml(self, pretty=False, level=1, symbol=u'\t'):
        retval = u'<%s' % (self.name,)
        for (attribute, value) in self.attributes.iteritems():
            retval += u' %s="%s"' % (attribute, xmlify(value))
        if len(self) == 0:
            retval += u'/>'
            return retval
        retval += u'>'
        if pretty:
            for subelement in self:
                if isinstance(subelement, unicode):
                    retval += u'\n' + symbol*level + xmlify(subelement)
                else:
                    retval += u'\n' + symbol*level + subelement.toxml(pretty, level+1, symbol)
            retval += u'\n' + symbol*(level-1) + '</%s>' % (self.name,)
        else:        
            for subelement in self:
                if isinstance(subelement, unicode):
                    retval += xmlify(subelement)
                elif isinstance(subelement, str):
                    print "THIS SHOULD NOT HAPPEN: String '%s' found!" % subelement
                    retval += xmlify(subelement)
                else:
                    retval += subelement.toxml(pretty, level+1, symbol)
            retval += u'</%s>' % (self.name,)
        return retval
        
    def __repr__(self):
        return u"<'%s' element: %r %s>" % (self.name, self.attributes, list.__repr__(self))
        
    def append(self, arg):
        if isinstance(arg, basestring):
            if len(arg) == 0:   #don't attach empty strings
                return
            try:
                if isinstance(self[-1], unicode):  #we convert to unicode!
                    self[-1] += unicode(arg)
                else:
                    list.append(self, unicode(arg))
            except IndexError:
                list.append(self, unicode(arg))
        elif isinstance(arg, Element):
            list.append(self, arg)
            arg.parent = self
        else:
            raise TypeError(u'Argument is of %r; expected <type \'BaseElement\'>.' % (type(arg),))
    
    def extend(self, list):
        for item in list:
            self.append(item)
        
    def appendElement(self, *args, **kwargs):
        element = Element(*args, **kwargs)
        self.append(element)
        return element
        
def xmlify(data):
    """
    >>> xmlify(u'mooh&<>\\'"')
    u'mooh&amp;&lt;&gt;&apos;&quot;'
    """
    data = data.replace(u'&', u'&amp;')
    data = data.replace(u'<', u'&lt;')
    data = data.replace(u'>', u'&gt;')
    data = data.replace(u"'", u'&apos;')
    data = data.replace(u'"', u'&quot;')
    return data

def _test(*args, **kwargs):
    import doctest
    doctest.testmod(*args, **kwargs)
    
if __name__ == "__main__":
    _test()