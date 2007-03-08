#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
Bot page moves to another title.

Command-line arguments:

    -file          Work on all pages listed in a text file.
                   Argument can also be given as "-file:filename".

    -cat           Work on all pages which are in a specific category.
                   Argument can also be given as "-cat:categoryname".

    -ref           Work on all pages that link to a certain page.
                   Argument can also be given as "-ref:referredpagetitle".

    -links         Work on all pages that are linked from a certain page.
                   Argument can also be given as "-link:linkingpagetitle".

    -link          same as -links (deprecated)

    -start         Work on all pages on the home wiki, starting at the named page.
                   
    -from -to      The page to move from and the page to move to.

    -new           Work on the most recent new pages on the wiki.

    -del           Argument can be given also together with other arguments,
                   its functionality is delete old page that was moved.
                   For example: "movepages.py pagetitle -del".

    -prefix        Move pages by adding a namespace prefix to the names of the pages.
                   (Will remove the old namespace prefix if any)
                   Argument can also be given as "-prefix:namespace:".

    -always        Don't prompt to make changes, just do them.

Single page use:   movepages.py pagetitle1 pagetitle2 ...

"""
#
# (C) Leonardo Gregianin, 2006
# (C) Andreas J. Schwab, 2007
#
# Distributed under the terms of the MIT license.
#

__version__='$Id$'

import wikipedia, pagegenerators, catlib, config
import sys

summary={
    'en': u'Pagemove by bot',
    'he': u'העברת דף באמצעות בוט',
    'pt': u'Página movida por bot',
    'pl': u'Przeniesienie artykułu przez robota',
    'de': u'Seite durch Bot verschoben',
    'fr': u'Page renommée par bot',
    'el': u'Μετακίνηση σελίδων με bot'
}

deletesummary={
    'en': u'Delete page by bot',
    'pt': u'Página apagada por bot',
    'de': u'Seite durch Bot gelöscht',
    'pl': u'Usunięcie artykułu przez robota',
    'fr': u'Page supprimée par bot',
    'el': u'Διαγραφή σελίδων με bot'
}

class MovePagesBot:
    def __init__(self, generator, prefix, delete, always):
        self.generator = generator
        self.prefix = prefix
        self.delete = delete
        self.always = always

        
    def moveOne(self,page,pagemove,delete):
        try:
            msg = wikipedia.translate(wikipedia.getSite(), summary)
            wikipedia.output(u'Moving page %s' % page.title())
            wikipedia.output(u'to page %s' % pagemove)
            page.move(pagemove, msg, throttle=True)
            if delete == True:
                deletemsg = wikipedia.translate(wikipedia.getSite(), deletesummary)
                page.delete(deletemsg)
        except wikipedia.NoPage:
            wikipedia.output('Page %s does not exist!' % page.title())
        except wikipedia.IsRedirectPage:
            wikipedia.output('Page %s is a redirect; skipping.' % page.title())
        except wikipedia.LockedPage:
            wikipedia.output('Page %s is locked!' % page.title())
            
    def treat(self,page):
        pagetitle = page.title()
        wikipedia.output(u'\n>>>> %s <<<<' % pagetitle)
        if self.prefix:
            pagetitle = page.titleWithoutNamespace()
            pagemove = (u'%s%s' % (self.prefix, pagetitle))
            if self.always == False:
                ask2 = wikipedia.input(u'Change the page title to "%s"? [(Y)es, (N)o, (Q)uit]' % pagemove)
                if ask2 in ['y', 'Y']:
                    self.moveOne(page,pagemove,self.delete)
                elif ask2 in ['q', 'Q']:
                    sys.exit()
                elif ask2 in ['n', 'N']:
                    pass
                else:
                    self.treat(page)
            else:
                self.moveOne(page,pagemove,self.delete)
        elif self.appendAll == False:
            ask = wikipedia.input('What do you want to do: (c)hange page name, (a)ppend to page name, (n)ext page or (q)uit?')
            if ask in ['c', 'C']:
                pagemove = wikipedia.input(u'New page name:')
                self.moveOne(page,pagemove,self.delete)
            elif ask in ['a', 'A']:
                self.pagestart = wikipedia.input(u'Append This to the start:')
                self.pageend = wikipedia.input(u'Append This to the end:')
                if page.title() == page.titleWithoutNamespace():
                    pagemove = (u'%s%s%s' % (self.pagestart, page.title(), self.pageend))
                else:                                             
                    ask2 = wikipedia.input(u'Do you want to remove the namespace prefix "%s:"? [(Y)es, (N)o]'% page.site().namespace(page.namespace()))
                    if ask2 in ['y', 'Y']:
                        pagemove = (u'%s%s%s' % (self.pagestart, page. titleWithoutNamespace(), self.pageend))
                    else:                                             
                        pagemove = (u'%s%s%s' % (self.pagestart, page.title(), self.pageend))
                ask2 = wikipedia.input(u'Change the page title to "%s"? [(Y)es, (N)o, (A)ll, (Q)uit]' % pagemove)
                if ask2 in ['y', 'Y']:
                    self.moveOne(page,pagemove,self.delete)
                elif ask2 in ['a', 'A']:
                    self.appendAll = True
                    self.moveOne(page,pagemove,self.delete)
                elif ask2 in ['q', 'Q']:
                    sys.exit()
                elif ask2 in ['n', 'N']:
                    pass
                else:
                    self.treat(page)
            elif ask in ['n', 'N']:
                pass
            elif ask in ['q', 'Q']:
                sys.exit()
            else:
                self.treat(page)
        else:
            pagemove = (u'%s%s%s' % (self.pagestart, page.title(), self.pageend))
            if self.always == False:
                ask2 = wikipedia.input(u'Change the page title to "%s"? [(Y)es, (N)o, (Q)uit]' % pagemove)
                if ask2 in ['y', 'Y']:
                    self.moveOne(page,pagemove,self.delete)
                elif ask2 in ['q', 'Q']:
                    sys.exit()
                elif ask2 in ['n', 'N']:
                    pass
                else:
                    self.treat(page)
            else:
                self.moveOne(page,pagemove,self.delete)

    def run(self):
        self.appendAll = False
        for page in self.generator:
            self.treat(page)

def main():
    singlepage = []
    gen = cat = ref = link = start = prefix = None
    FromName = ToName = None
    delete = False
    always = False
    
    for arg in wikipedia.handleArgs():
        if arg.startswith('-file'):
            if len(arg) == len('-file'):
                fileName = wikipedia.input(u'Enter name of file to move pages from:')
            else:
                fileName = arg[len('-file:'):]
            gen = pagegenerators.TextfilePageGenerator(fileName)
        elif arg.startswith('-cat'):
            if len(arg) == 4:
                cat = wikipedia.input(u'Please enter the category name:')
            else:
                cat = arg[5:]
            categ = catlib.Category(wikipedia.getSite(), 'Category:%s'%cat)
            gen = pagegenerators.CategorizedPageGenerator(categ)
        elif arg.startswith('-ref'):
            if len(arg) == 4:
                ref = wikipedia.input(u'Links to which page should be processed?')
            else:
                ref = arg[5:]
            refer = wikipedia.Page(wikipedia.getSite(), ref)
            gen = pagegenerators.ReferringPageGenerator(refer)
        elif arg.startswith('-link'): # either -links or -link
            if len(arg) == 5:
                link = wikipedia.input(u'Links from which page should be processed?')
            elif arg.startswith('-links'):
                if len(arg) == 6:
                    link = wikipedia.input(u'Links from which page should be processed?')
                else:
                    link = arg[7:]
            else:
                link = arg[6:]
            links = wikipedia.Page(wikipedia.getSite(), link)
            gen = pagegenerators.LinkedPageGenerator(links)
        elif arg.startswith('-start'):
            if len(arg) == 6:
                start = wikipedia.input(u'Which page to start from:')
            else:
                start = arg[7:]
            startp = wikipedia.Page(wikipedia.getSite(), start)
            gen = pagegenerators.AllpagesPageGenerator(startp.titleWithoutNamespace(),namespace=startp.namespace())
        elif arg.startswith('-new'):
            gen = pagegenerators.NewpagesPageGenerator(config.special_page_limit)
        elif arg == '-del':
            delete = True
        elif arg == '-always':
            always = True
        elif arg.startswith('-from:'):
            oldName = arg[len('-from:'):]
            FromName = True
        elif arg.startswith('-to:'):
            newName = arg[len('-to:'):]
            ToName = True
        elif arg.startswith('-prefix'):
            if len(arg) == len('-prefix'):
                prefix = wikipedia.input(u'Input the prefix:')
            else:
                prefix = arg[8:]
        else:
            singlepage.append(wikipedia.Page(wikipedia.getSite(), arg))

    if singlepage:
        gen = iter(singlepage)
    if ((FromName and ToName) == True):
        wikipedia.output(u'Do you want to move %s to %s?' % (oldName, newName))
        page = wikipedia.Page(wikipedia.getSite(), oldName)
        bot = MovePagesBot(None, prefix, delete, always)
        bot.moveOne(page,newName,delete)
    elif gen:
        preloadingGen = pagegenerators.PreloadingGenerator(gen)
        bot = MovePagesBot(preloadingGen, prefix, delete, always)
        bot.run()
    else:
        wikipedia.showHelp('movepages')
                
if __name__ == '__main__':
    try:
        main()
    finally:
        wikipedia.stopme()

 	  	 
