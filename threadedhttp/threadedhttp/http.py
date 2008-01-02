# -*- coding: utf-8  -*-
""" Thread-safe cookie-eating Http library based on httplib2 """

#
# (C) Merlijn van Deen, 2007
#
# Indicated parts (C) Joe Gregorio et al, 2006 
# Distributed under the terms of the MIT license
#
__version__ = '$Id$'
__docformat__ = 'epytext'

import logging

# easy_install safeguarded dependencies
import pkg_resources
pkg_resources.require("httplib2")
import httplib2

# local package imports
from cookiejar import LockableCookieJar
from connectionpool import ConnectionPool
from dummy import DummyRequest, DummyResponse

class Http(httplib2.Http):
    """ Subclass of httplib2.Http that uses a `LockableCookieJar` to store cookies.
        Overrides httplib2s internal redirect support to prevent cookies 
        being eaten by the wrong sites.
    """
    def __init__(self, *args, **kwargs):
        """ @param cookiejar: (optional) CookieJar to use. A new one will be used when not supplied.
            @param connection_pool: (optional) Connection pool to use. A new one will be used when not supplied.
            @param max_redirects: (optional) The maximum number of redirects to follow. 5 is default.
        """
        self.cookiejar = kwargs.pop('cookiejar', LockableCookieJar())
        self.connection_pool = kwargs.pop('connection_pool', ConnectionPool())
        self.max_redirects = kwargs.pop('max_redirects', 5)
        httplib2.Http.__init__(self, *args, **kwargs)

    def request(self, uri, method="GET", body=None, headers=None, max_redirects=None, connection_type=None):
        """ Starts an HTTP request.
            @param uri: The uri to retrieve
            @param method: (optional) The HTTP method to use. Default is 'GET'
            @param body: (optional) The request body. Default is no body.
            @param headers: (optional) Additional headers to send. Defaults include 
                            C{connection: keep-alive}, C{user-agent} and C{content-type}.
            @param max_redirects: (optional) The maximum number of redirects to use for this request.
                                  The class instances max_redirects is default
            @param connection_type: (optional) ?
            @returns: (response, content) tuple
        """ 
        if max_redirects is None:
            max_redirects = self.max_redirects
        if headers is None:
            headers = {}
        # Prepare headers
        headers.pop('cookie', None)
        req = DummyRequest(uri, headers)
        self.cookiejar.lock.acquire()
        try:
            self.cookiejar.add_cookie_header(req)
        finally:
            self.cookiejar.lock.release()
        headers = req.headers
        
        # Wikimedia squids: add connection: keep-alive to request headers unless overridden
        headers['connection'] = headers.pop('connection', 'keep-alive')
        
        # determine connection pool key and fetch connection
        (scheme, authority, request_uri, defrag_uri) = httplib2.urlnorm(httplib2.iri2uri(uri))
        conn_key = scheme+":"+authority
        
        connection = self.connection_pool.pop_connection(conn_key)
        if connection is not None:
            self.connections[conn_key] = connection
        
        # Redirect hack: we want to regulate redirects
        follow_redirects = self.follow_redirects
        #print 'follow_redirects: %r %r' % (self.follow_redirects, follow_redirects)
        self.follow_redirects = False
        #print 'follow_redirects: %r %r' % (self.follow_redirects, follow_redirects)
        logging.debug('%r' % ((uri, method, headers, max_redirects, connection_type),))
        (response, content) = httplib2.Http.request(self, uri, method, body, headers, max_redirects, connection_type)
        #print 'follow_redirects: %r %r' % (self.follow_redirects, follow_redirects)
        self.follow_redirects = follow_redirects
        #print 'follow_redirects: %r %r' % (self.follow_redirects, follow_redirects)
        
        
        # return connection to pool
        self.connection_pool.push_connection(conn_key, self.connections[conn_key])
        del self.connections[conn_key]
                
        # First write cookies 
        self.cookiejar.lock.acquire()
        try:           
            self.cookiejar.extract_cookies(DummyResponse(response), req)
        finally:
            self.cookiejar.lock.release()
        
        # Check for possible redirects
        redirectable_response = ((response.status == 303) or
                                 (response.status in [300, 301, 302, 307] and method in ["GET", "HEAD"]))
        if self.follow_redirects and (max_redirects > 0) and redirectable_response:
            (response, content) = self._follow_redirect(uri, method, body, headers, response, content, max_redirects)
        return (response, content)
    
    # The _follow_redirect function is based on the redirect handling in the
    # _request function of httplib2. The original function is (C) Joe Gregorio et al, 2006
    # and licensed under the MIT license. Other contributers include
    # Thomas Broyer (t.broyer@ltgt.net), James Antill, Xavier Verges Farrero, 
    # Jonathan Feinberg, Blair Zajac, Sam Ruby and Louis Nyffenegger (httplib2.__contributers__)
    def _follow_redirect(self, uri, method, body, headers, response, content, max_redirects):
        """ Internal function to follow a redirect recieved by L{request} """
        (scheme, authority, absolute_uri, defrag_uri) = httplib2.urlnorm(httplib2.iri2uri(uri))
        if self.cache:
            cachekey = defrag_uri
        else:
            cachekey = None

        # Pick out the location header and basically start from the beginning
        # remembering first to strip the ETag header and decrement our 'depth'
        if not response.has_key('location') and response.status != 300:
            raise httplib2.RedirectMissingLocation("Redirected but the response is missing a Location: header.", response, content)
        # Fix-up relative redirects (which violate an RFC 2616 MUST)
        if response.has_key('location'):
            location = response['location']
            (scheme, authority, path, query, fragment) = httplib2.parse_uri(location)
            if authority == None:
                response['location'] = httplib2.urlparse.urljoin(uri, location)
                logging.debug('Relative redirect: changed [%s] to [%s]' % (location, response['location']))
        if response.status == 301 and method in ["GET", "HEAD"]:
            response['-x-permanent-redirect-url'] = response['location']
            if not response.has_key('content-location'):
                response['content-location'] = absolute_uri 
            httplib2._updateCache(headers, response, content, self.cache, cachekey)
        
        headers.pop('if-none-match', None)
        headers.pop('if-modified-since', None)
        
        if response.has_key('location'):
            location = response['location']
            redirect_method = ((response.status == 303) and (method not in ["GET", "HEAD"])) and "GET" or method
            return self.request(location, redirect_method, body=body, headers = headers, max_redirects = max_redirects - 1)
        else:
            raise httplib2.RedirectLimit("Redirected more times than redirection_limit allows.", response, content)