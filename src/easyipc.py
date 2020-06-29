#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@brief   Easy-to-use IPC module. Check the examples in 'server.py' and 'client.py'.
@details You can send any object serializable by pickle and a bit more efficiently
         numpy.ndarray objects. DatagramIPC is implemented using UDP, and it is 
         usually slower that the one implemented with FIFOs, Pipe.
@author  Luis C. Garcia Peraza Herrera (luiscarlos.gph@gmail.com).
@date    24 June 2020.
"""

import socket
import struct
import numpy as np
import atexit
import pickle
import os
import os.path
import stat
import select
import tempfile


class BaseIPC:
    lensize_dict = {4: '>I', 8: '>Q'}

    def recv_whatever(self):
        raise NotImplemented()


    def send_whatever(self, data):
        raise NotImplemented()
    

    def recv_array(self):
        raise NotImplemented()


    def send_array(self, data):
        raise NotImplemented()


    def cleanup(self): # Should be called automatically, use atexit module for this
        raise NotImplemented()


class Pipe(BaseIPC):
    
    #def __init__(self, read_pipe_name, write_pipe_name, lensize=8):
    def __init__(self, pipe_name, lensize=8, header_len=128):
        """
        @brief      Easy to use wrapper for full-duplex IPC among two processes.
        @details    Two PIPEs are used for the task. They have to be inverted between
                    client and server. If one process calls this constructor 
                    __init__('pipe1', 'pipe2') the other process should call this
                    constructor __init__('pipe2', 'pipe1').

        @param[in]  read_pipe_name   String with the name of the input FIFO.
        @param[in]  write_pipe_name  String with the name of the output FIFO.
        @param[in]  lensize          Number of bytes that will be used to store the
                                     size of the data (in bytes). This means you can 
                                     send packages of data of upto 2^64 bytes. That
                                     is a lot of data.
        @returns    nothing.
        """
        self.pipe_name = pipe_name
        self.lensize = lensize 
        self.header_len = header_len
        self.listening = False
        self.connected = False
        self.read_pipe = None
        self.write_pipe = None

        # Register the method cleanup so that it is called on destruction
        atexit.register(self.cleanup)

    @staticmethod
    def mkpipe(name):
        if os.path.exists(name):
            if not stat.S_ISFIFO(os.stat(name).st_mode):
                raise ValueError('Path ' + name + ' exists, but it is not a PIPE.')
        else:
            os.mkfifo(name)


    def listen(self):
        """
        @brief Blocks until a client is connected.
        """
        self.listening = True
        
        # Compile the pipe paths
        self.write_pipe_name = os.path.join(tempfile.gettempdir(), '.' + self.pipe_name + '_client')
        self.read_pipe_name = os.path.join(tempfile.gettempdir(), '.' + self.pipe_name + '_server')

        # Create pipes
        Pipe.mkpipe(self.write_pipe_name)
        Pipe.mkpipe(self.read_pipe_name)

        # Open pipes
        self.read_pipe = os.open(self.read_pipe_name, os.O_RDONLY)
        self.write_pipe = os.open(self.write_pipe_name, os.O_WRONLY)

        # Create polling object for the reading pipe
        self.poll = select.poll()
        self.poll.register(self.read_pipe, select.POLLIN) 


    def connect(self):
        """
        @brief Blocks until a server starts listening.
        """
        self.connected = True
        
        # Put together the names of the I/O pipes
        self.write_pipe_name = os.path.join(tempfile.gettempdir(), '.' + self.pipe_name + '_server')
        self.read_pipe_name = os.path.join(tempfile.gettempdir(), '.' + self.pipe_name + '_client')
        
        # Create pipes 
        Pipe.mkpipe(self.write_pipe_name)
        Pipe.mkpipe(self.read_pipe_name)

        # Open pipes 
        self.write_pipe = os.open(self.write_pipe_name, os.O_WRONLY)
        self.read_pipe = os.open(self.read_pipe_name, os.O_RDONLY)

        # Create polling object for the reading pipe
        self.poll = select.poll()
        self.poll.register(self.read_pipe, select.POLLIN) 


    def cleanup(self):
        if self.listening or self.connected:
            os.close(self.read_pipe)
            os.close(self.write_pipe)


    def recv_whatever(self, blocking=True):
        """ 
        @brief    This methods uses pickle, so whatever object serialisable by pickle is good.
        @details  This is a blocking operation. 
        @returns  whhatever object sent from the other end or None if there is 
                  nothing available to be read and we are in non-blocking mode.
        """
        if not blocking and (self.read_pipe, select.POLLIN) not in self.poll.poll(1):
            return None

        # Read header containing the size of the message
        raw_length = os.read(self.read_pipe, self.lensize)
        length = struct.unpack(BaseIPC.lensize_dict[self.lensize], raw_length)[0]

        # Read the actual message
        body = os.read(self.read_pipe, length)

        # Quick integrity check
        if length != len(body):
            raise IOError('Message received has a different size than expected.')
        
        return pickle.loads(body)


    def send_whatever(self, data):
        """ 
        @brief    This methods uses pickle, so whatever object serialisable by pickle is good.
        @details  This is a blocking operation. It blocks when the pipe is full.
                  A pipe has a limited capacity (typically 16 pages). This method will block 
                  until data has been read and there is space again.
        @returns  nothing.
        """
        body = pickle.dumps(data)
        length = struct.pack(BaseIPC.lensize_dict[self.lensize], len(body))
        os.write(self.write_pipe, length)
        os.write(self.write_pipe, body)


    def recv_array(self, blocking=True):
        """ 
        @brief      Pickle is quite slow for large numpy arrays, so we have this dedicated method.
        @details    This is a blocking operation (if there is no data available).
        @returns    a numpy.ndarray. If blocking is False and there is nothing to be read, it
                    quickly returns None.
        """
        if not blocking and (self.read_pipe, select.POLLIN) not in self.poll.poll(1):
            return None

        # Read length 
        raw_length = os.read(self.read_pipe, self.lensize)
        length = struct.unpack(BaseIPC.lensize_dict[self.lensize], raw_length)[0]
        
        # Read header 
        header = os.read(self.read_pipe, self.header_len) 
        header_len = struct.unpack(BaseIPC.lensize_dict[self.lensize], header[:self.lensize])[0]
        header_info = eval(header[self.lensize:self.lensize + header_len].decode('ascii'))

        # Read body
        body = os.read(self.read_pipe, length - self.header_len)
        data = np.frombuffer(body, dtype=header_info['dtype']).reshape(header_info['shape'])

        # Quick integrity check 
        if length - len(header) != len(body):
            raise IOError('The amount of data read is different than expected.')

        return data


    def send_array(self, data):
        """ 
        @brief      Pickle is quite slow for large numpy arrays, so we have this dedicated method.

        @details    This is a blocking operation. It blocks when the pipe is full.
                    A pipe has a limited capacity (typically 16 pages). This method will block 
                    until data has been read and there is space again.

                    Message structure: [ length | header | body ]

                    length: self.lensize bytes
                    header: 128 bytes
                    body  : whatever 'length' says minus the 64 of the header
    
        @param[in]  data  Numpy.ndarray.
        @returns    nothing.
        """
        # Generate the bytes of the array
        body = data.tobytes()
        
        # Generate the bytes of the length
        length = struct.pack(BaseIPC.lensize_dict[self.lensize], len(body) + self.header_len)

        # Generate the bytes of the header
        header_info = str({'shape': data.shape, 'dtype': data.dtype.name}).encode('ascii')
        header = bytearray(self.header_len)
        header[:self.lensize] = struct.pack(BaseIPC.lensize_dict[self.lensize], len(header_info))
        header[self.lensize:self.lensize + len(header_info)] = header_info

        # Send length, header, and body 
        os.write(self.write_pipe, length)
        os.write(self.write_pipe, header)
        os.write(self.write_pipe, body)
        

if __name__ == "__main__":
    raise RuntimeError('The EasyIPC module is not a script and such not be executed as such.')
