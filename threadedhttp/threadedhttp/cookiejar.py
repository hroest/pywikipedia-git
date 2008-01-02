# -*- coding: utf-8  -*-
""" Lockable CookieJar and FileCookieJar """

#
# (C) Merlijn van Deen, 2007
#
# Distributed under the terms of the MIT license
#

__version__ = '$Id$'
__docformat__ = 'epytext'

import logging
import threading
import cookielib

class LockableCookieJar(cookielib.CookieJar):
    """ CookieJar with integrated Lock object """
    def __init__(self, *args, **kwargs):
        cookielib.CookieJar.__init__(self, *args, **kwargs)
        self.lock = threading.Lock()
        
class LockableFileCookieJar(cookielib.FileCookieJar):
    """ CookieJar with integrated Lock object """
    def __init__(self, *args, **kwargs):
        cookielib.FileCookieJar.__init__(self, *args, **kwargs)
        self.lock = threading.Lock()
