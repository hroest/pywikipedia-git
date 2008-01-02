# -*- coding: utf-8  -*-
""" Thread safe connection pools to share connections between threads. """

#
# (C) Merlijn van Deen, 2007
#
# Distributed under the terms of the MIT license
#

__version__ = '$Id$'
__docformat__ = 'epytext'

import logging
import threading

class ConnectionList(list):
    """ List with BoundedSemaphore """
    def __init__(self, maxnum, *args, **kwargs):
        """ @param maxnum: BoundedSemaphores counter initialisation (maximum number of acquires)"""
        list.__init__(self, *args, **kwargs)
        self.max = threading.BoundedSemaphore(maxnum)

class ConnectionPool(object):
    def __init__(self, max_connections=25, max_connections_per_host=5):
        """ @param max_connections: Global maximum number of connections for this pool
            @param max_connections_per_host: maximum number of connections per host
        """
        self.max_connections_per_host = max_connections_per_host
        self.global_max = threading.BoundedSemaphore(max_connections)
        self.lock = threading.Lock()
        self.connections = [None] * max_connections # fill known connections witn Nones
        self.clists = {}         # 'id': (semaphore, lock, [connection1, connection2])
        logging.log(1,'<%r>: initialized' % self)
        
    def __del__(self):
        """ Destructor to close all connections in the pool.
            Not completely thread-safe, as connections *could* return just
            after this function. Make sure the pool is destructed only when
            it is no longer in use!"""
        self.lock.acquire() #prevents any connections from returning into the pool
        try:
            for connection in self.connections:
                if connection is not None:
                    connection.close()
            del self.connections
            del self.clists
        finally:
            self.lock.release()
        
    def pop_connection(self, identifier):
        """ Gets a connection from identifiers connection pool
            @param identifier The pool identifier
            @returns A connection object if found, None otherwise
        """
        logging.log(1,'<%r>: acquiring global_max...' % self)
        self.global_max.acquire()
        logging.log(1,'<%r>: global_max acquired' % self)
        try:
            self.lock.acquire()
            if identifier not in self.clists:
                self.clists[identifier] = ConnectionList(self.max_connections_per_host)
            clist = self.clists[identifier]
            self.lock.release()
            logging.log(1,'<%r>: acquiring clist.max...' % self)
            if not clist.max.acquire(False): # acquire local lock, releasing global lock when waiting
                logging.log(1,'<%r>: ...failed' % self)
                self.global_max.release()
                logging.log(logging.DEBUG,'<%r>: No host connections available, global_max released.' % self)
                clist.max.acquire()
                self.global_max.acquire()
            try:
                logging.log(1,'<%r>: ...acquired' % self)
                # we hebben nu zowel toestemming voor een global als voor een local connection
                # kijk eerst of er zo'n verbinding bestaat
                self.lock.acquire()
                try:
                    if len(clist) > 0:
                        connection = clist.pop()
                        logging.log(1,'<%r>: using cached connection' % self)
                        return connection
                    else:
                        # pop the oldest connection from the connection stack
                        old_connection = self.connections.pop(0)
                        logging.log(1,'<%r>: popped %r to make place for new connection' % (self,old_connection))
                        if old_connection is not None:
                            old_connection.close()
                            for slist in self.clists.itervalues():
                                if old_connection in clist:
                                    clist.remove(old_connection)
                                    break # a connection is in max one clist
                        return None
                finally:
                    self.lock.release()
            except Exception, e:
                logging.log(20,'<%r>: Exception raised level 2 | %r' % (self, e))
                clist.max.release()            
                raise
        except Exception, e:
            logging.log(20,'<%r>: Exception raised level 1 | %r' % (self, e))
            self.global_max.release()
            raise
        
    def push_connection(self, identifier, connection):
        """ Gets a connection from identifiers connection pool
            @param identifier The pool identifier
            @returns A connection object if found, None otherwise
        """
        self.lock.acquire()
        try:
            clist = self.clists[identifier]
            clist.append(connection)
            if connection not in self.connections:
                self.connections.append(connection)
            clist.max.release()
            self.global_max.release()
            logging.log(1, 'clist.max and global_max += 1')
        finally:
            self.lock.release()

class BasicConnectionPool(object):
    """ A thread-safe connection pool """
    def __init__(self, maxnum=5):
        """ @param maxnum: Maximum number of connections per identifier.
                           The pool drops excessive connections added.
        """
        self.connections = {}
        self.lock = threading.Lock()
        self.maxnum = maxnum
    
    def __del__(self):
        """ Destructor to close all connections in the pool """
        self.lock.acquire()
        try:
            for connection in self.connections:
                connection.close()
            
        finally:
            self.lock.release()
            
    def __repr__(self):
        return self.connections.__repr__()
        
    def pop_connection(self, identifier):
        """ Gets a connection from identifiers connection pool
            @param identifier: The pool identifier
            @returns: A connection object if found, None otherwise
        """
        self.lock.acquire()
        try:
            if identifier in self.connections:
                if len(self.connections[identifier]) > 0:
                    return self.connections[identifier].pop()
            return None
        finally:
            self.lock.release()
            
    def push_connection(self, identifier, connection):
        """ Adds a connection to identifiers connection pool
            @param identifier: The pool identifier
            @param connection: The connection to add to the pool
        """
        self.lock.acquire()
        try:
            if identifier not in self.connections:
                self.connections[identifier] = []
            
            if len(self.connections[identifier]) == self.maxnum:
                logging.debug('closing %s connection %r' % (identifier, connection))
                connection.close()
                del connection
            else:
                self.connections[identifier].append(connection)
        finally:
            self.lock.release()