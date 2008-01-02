# -*- coding: utf-8  -*-
""" Dummy classes for CookieJar <-> httplib2 communication """

#
# (C) Metaweb Technologies, Inc., 2007
#
# Distributed under the terms of the license included below,
# which is compatible with use in a MIT licensed project.
#

__version__ = '$Id$'

# ========================================================================
# Copyright (c) 2007, Metaweb Technologies, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY METAWEB TECHNOLOGIES AND CONTRIBUTORS
# ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL METAWEB
# TECHNOLOGIES OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ========================================================================

import logging
import urllib
import re
import cookielib

class DummyRequest(object):
    """Simulated urllib2.Request object for httplib2
       implements only what's necessary for cookielib.CookieJar to work
    """
    def __init__(self, url, headers=None):
        self.url = url
        self.headers = headers
        self.origin_req_host = cookielib.request_host(self)
        self.type, r = urllib.splittype(url)
        self.host, r = urllib.splithost(r)
        if self.host:
            self.host = urllib.unquote(self.host)

    def get_full_url(self):
        return self.url

    def get_origin_req_host(self):
        # TODO to match urllib2 this should be different for redirects
        return self.origin_req_host

    def get_type(self):
        return self.type

    def get_host(self):
        return self.host

    def get_header(self, key, default=None):
        return self.headers.get(key.lower(), default)

    def has_header(self, key):
        return key in self.headers

    def add_unredirected_header(self, key, val):
        # TODO this header should not be sent on redirect
        self.headers[key.lower()] = val

    def is_unverifiable(self):
        # TODO to match urllib2, this should be set to True when the
        #  request is the result of a redirect
        return False

class DummyResponse(object):
    """Simulated urllib2.Request object for httplib2
       implements only what's necessary for cookielib.CookieJar to work
    """
    def __init__(self, response):
        self.response = response

    def info(self):
        return DummyMessage(self.response)

class DummyMessage(object):
    """Simulated mimetools.Message object for httplib2
       implements only what's necessary for cookielib.CookieJar to work
    """
    def __init__(self, response):
        self.response = response

    def getheaders(self, k):
        k = k.lower()
        #v = self.response.get(k.lower(), None)
        if k not in self.response:
            return []
        #return self.response[k].split(re.compile(',\\s*'))

        # httplib2 joins multiple values for the same header
        #  using ','.  but the netscape cookie format uses ','
        #  as part of the expires= date format.  so we have
        #  to split carefully here - header.split(',') won't do it.
        HEADERVAL= re.compile(r'\s*(([^,]|(,\s*\d))+)')
        return [h[0] for h in HEADERVAL.findall(self.response[k])]