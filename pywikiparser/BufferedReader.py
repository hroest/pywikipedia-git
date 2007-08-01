class BufferedReader(object):
    """ Buffered reader. Usage:
    
    >>> reader = BufferedReader((i for i in range(10)))
    >>> restore = reader.getrestore()
    >>> restore
    -1
    >>> reader.next()
    0
    >>> reader.next()
    1
    >>> reader.undo(-1)
    >>> reader.next()
    0
    >>> restore = reader.commit(-1)
    >>> restore
    -1
    >>> reader.next()
    1
    >>> reader.getrestore()
    0
    >>> reader.next()
    2
    >>> reader.undo(0)
    >>> reader.next()
    2
    >>> reader.commit(0)
    1
    >>> reader.undo(1)
    >>> reader.next()
    3
    >>> reader.undo(-1)
    >>> reader.next()
    1
    """
    
    def __init__(self, generator):
        self.buffer = []
        self.counter = -1
        self.generator = generator
        self.gen = self._generator()
        
        self.gi_frame       = self.gen.gi_frame
        self.gi_running     = self.gen.gi_running
        self.__doc__        = "Buffered Generator. Added functions are commit() (clear buffer), undo (reset read pointer) and push (push data on the output buffer)"
        
    def __hash__(self, *args, **kwargs):
        return self.gen.__hash__(*args, **kwargs)
        
    def __iter__(self, *args, **kwargs):
        return self.gen.__iter__(*args, **kwargs)
        
    def __reduce__(self, *args, **kwargs):
        return self.gen.__reduce__(*args, **kwargs)
        
    def __reduce_ex__(self, *args, **kwargs):
        return self.gen.__reduce_ex__(*args, **kwargs)
        
    def __repr__(self, *args, **kwargs):
        return 'Buffered version of %s' % (self.gen.__repr__(*args, **kwargs),)
        
    def __str__(self, *args, **kwargs):
        return 'Buffered version of %s' % (self.gen.__str__(*args, **kwargs))
    
    def next(self, *args, **kwargs):
        return self.gen.next(*args, **kwargs)  
    
    def peek(self, num=1):
        if len(self.buffer) <= self.counter+num:
            data = self.generator.next()
            self.buffer.append(data)
        return self.buffer[self.counter+num]
    
    def _generator(self):
        while(True):
            self.counter += 1
            if len(self.buffer) <= self.counter:
                data = self.generator.next()
                self.buffer.append(data)
            yield self.buffer[self.counter]
    
    def getrestore(self):
        return self.counter
    
    def commit(self, counter):
        if counter == -1:
            # clear memory
            self.buffer = self.buffer[self.counter+1:]
            self.counter = -1
        
        self.gen = self._generator()
        return self.counter
        
    def undo(self, counter):
        self.counter = counter
        self.gen = self._generator()
        
if __name__ == "__main__":
    import doctest
    doctest.testmod()