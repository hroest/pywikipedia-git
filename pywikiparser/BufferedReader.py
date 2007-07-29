class BufferedReader(object):
    def __init__(self, generator):
        self.inbuffer = []
        self.outbuffer = []
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
    
    def peek(self):
        if len(self.outbuffer) <= self.counter+1:
            data = self.generator.next()
            self.inbuffer.append(data)
            self.outbuffer.append(data)
        return self.outbuffer[self.counter+1]
    
    def _generator(self):
        while(True):
            self.counter += 1
            if len(self.outbuffer) <= self.counter:
                data = self.generator.next()
                self.inbuffer.append(data)
                self.outbuffer.append(data)
            yield self.outbuffer[self.counter]
    
    def commit(self):
        self.inbuffer = self.inbuffer[self.counter+1:]
        self.outbuffer = self.outbuffer[self.counter+1:]
        self.counter = -1
        self.gen = self._generator()
        
    def undo(self):
        self.outbuffer = self.inbuffer[:]
        self.counter = -1
        self.gen = self._generator()
                
    def push(self, data):
        self.outbuffer.append(data)
        self.gen = self._generator()