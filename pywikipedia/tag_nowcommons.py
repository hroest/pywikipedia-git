#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
Bot tag tag files available at Commons with the Nowcommons template.
"""
#
# (C) Multichill, 2011
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id$'
#

import sys, re, urllib
import wikipedia as pywikibot
import pagegenerators
import image
#FIXME: Move these lists to commons_lib.py
from imagetransfer import nowCommonsTemplate
from nowcommons import nowCommons
from pywikibot import i18n

def main(args):
    generator = None;
    always = False

    # Load a lot of default generators
    genFactory = pagegenerators.GeneratorFactory()

    for arg in pywikibot.handleArgs():
        genFactory.handleArg(arg)


    generator = genFactory.getCombinedGenerator()
    if not generator:
        raise add_text.NoEnoughData('You have to specify the generator you want to use for the script!')

    pregenerator = pagegenerators.PreloadingGenerator(generator)

    for page in pregenerator:
        if page.exists() and (page.namespace() == 6) and \
            (not page.isRedirectPage()):
            imagepage = pywikibot.ImagePage(page.site(), page.title())
            foundNowCommons = False
            for template in imagepage.templates():
                #FIXME: Move the templates list to a lib.
                if template in pywikibot.translate(imagepage.site(), nowCommons):
                    foundNowCommons = True
            if foundNowCommons:
                pywikibot.output(u'The file %s is already tagged with NowCommons' % imagepage.title())
            else:
                imagehash = imagepage.getHash()
                commons = pywikibot.getSite(u'commons', u'commons')
                duplicates = commons.getFilesFromAnHash(imagehash)
                if duplicates:
                    duplicate = duplicates.pop()
                    pywikibot.output(u'Found duplicate image at %s' % duplicate)
                    comment = i18n.twtranslate(imagepage.site(), 'commons-file-now-available', {'localfile' : imagepage.titleWithoutNamespace(), 'commonsfile' : duplicate})
                    template = pywikibot.translate(imagepage.site(), nowCommonsTemplate)
                    newtext = imagepage.get() + template % (duplicate,)
                    pywikibot.showDiff(imagepage.get(), newtext)
                    imagepage.put(newtext, comment)


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    finally:
        pywikibot.stopme()
