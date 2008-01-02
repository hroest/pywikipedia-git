# -*- coding: utf-8  -*-
""" Module containing HttpRequest wrapper class and HttpProcessor thread class """

#
# (C) Merlijn van Deen, 2007
#
# Distributed under the terms of the MIT license
#
__version__ = '$Id$'
__docformat__ = 'epytext'

import logging
import threading

from http import Http

class HttpRequest(object):
    """ Object wrapper for HTTP requests that need to block the requesters thread.
        Usage:
        >>> request = HttpRequest('http://www.google.com')
        >>> queue.put(request)
        >>> request.lock.acquire()
        >>> print request.data
        
        C{request.lock.acquire()} will block until the data is available.
    """
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.data = None
        self.lock = threading.Semaphore(0)

class HttpProcessor(threading.Thread):
    """ Thread object to spawn multiple HTTP connection threads """
    def __init__(self, queue, cookiejar, connection_pool):
        """ @param queue: The C{Queue.Queue} object that contains L{HttpRequest} objects.
            @param cookiejar: The C{LockableCookieJar} cookie object to share among requests.
            @param connection_pool: The C{ConnectionPool} object which contains connections to share among requests.
        """
        threading.Thread.__init__(self)
        self.queue = queue
        self.http = Http(cookiejar=cookiejar, connection_pool=connection_pool)
        
    def run(self):
        # The Queue item is expected to either an HttpRequest object
        # or None (to shut down the thread)
        logging.debug('Thread started, waiting for requests.')
        while (True):
            item = self.queue.get()
            if item is None:
                logging.debug('Shutting down thread.')
                return
            try:
                item.data = self.http.request(*item.args, **item.kwargs)
            finally:
                if item.lock:
                    item.lock.release()