#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@brief   Easy-to-use IPC module. Check the examples in 'server.py' and 'client.py'.
@details You can send any object serializable by pickle and a bit more efficiently
         numpy.ndarray objects. DatagramIPC is implemented using UDP, and it is 
         usually slower that the one implemented with FIFOs, FifoIPC.
@author  Luis C. Garcia Peraza Herrera (luiscarlos.gph@gmail.com).
@date    24 June 2020.
"""

import socket
import struct
import numpy as np
import atexit
import pickle
import os
import stat
import select

class BaseIPC:
    lensize_dict = {4: '>I', 8: '>Q'}

    def recv_whatever(self):
        raise NotImplemented()


    def send_whatever(self, data):
        raise NotImplemented()
    

    def recv_ndarray(self):
        raise NotImplemented()


    def send_ndarray(self, data):
        raise NotImplemented()


    def cleanup(self): # Should be called automatically, use atexit module for this
        raise NotImplemented()

'''
class DatagramIPC(BaseIPC):

    def __init__(self, host='localhost', port=6987, bufsize=1024, lensize=8, compression=None):
        self.address = (host, port)
        self.bufsize = bufsize
        self.lensize = lensize
        self.compression = compression
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.is_server = False
        self.client_address = None
        try:
            self.sock.bind(self.address)
            self.is_server = True
        except:
            # If we cannot bind is because we are the client, 
            self.sock.connect(self.address)
        atexit.register(self.cleanup)
    

    def cleanup(self):
        self.sock.close() 
    

    def _recvall(self):
        # Receive the first package which carries the length (in bytes) of 
        # the data
        buf = None
        try:
            if self.is_server:
                # 0x40 means non-blocking
                buf, self.client_address = self.sock.recvfrom(self.bufsize, 
                                                              0x40) 
            else:
                buf = self.sock.recv(self.bufsize, 0x40) 
        except socket.error:
            return None
        
        # Read total message length in bytes
        msglen = struct.unpack(BaseIPC.lensize_dict[self.lensize], buf[:self.lensize])[0]

        # Read all the datagrams we need
        data = bytearray(buf[self.lensize:])
        while len(data) < msglen:
            dgsize = min(self.bufsize, msglen - len(data))
            dg = self.sock.recv(dgsize)
            data.extend(dg)
        return data


    def _sendall(self, data):
        msg = struct.pack(BaseIPC.lensize_dict[self.lensize], len(data)) + data
        sent = 0
        while sent < len(msg):
            dgsize = min(self.bufsize, len(msg) - sent)
            if self.is_server:
                self.sock.sendto(msg[sent:sent + dgsize], self.client_address)
            else:
                self.sock.sendall(msg[sent:sent + dgsize])
            sent += self.bufsize


    def recv_whatever(self):
        data = self._recvall()
        return pickle.loads(data) if data else data


    def send_whatever(self, data):
        data_bytes = pickle.dumps(data)
        return self._sendall(data_bytes)
    

    def recv_ndarray(self, shape, dtype):
        data = None
        data_bytes = self._recvall()
        if data_bytes is not None:
            data = np.frombuffer(data_bytes, dtype=dtype).reshape(shape)
        return data


    def send_ndarray(self, data):
        data_bytes = data.tobytes()
        return self._sendall(data_bytes)
'''


class FifoIPC(BaseIPC):
    
    def __init__(self, read_pipe_name, write_pipe_name, lensize=8):
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
        # Create PIPEs if they do not exist already 
        if os.path.exists(read_pipe_name):
            if not stat.S_ISFIFO(os.stat(read_pipe_name).st_mode):
                raise ValueError('Read pipe ' + read_pipe_name + ' exists, but it is not a PIPE.')
        else:
            os.mkfifo(read_pipe_name)
        if os.path.exists(write_pipe_name):
            if not stat.S_ISFIFO(os.stat(write_pipe_name).st_mode):
                raise ValueError('Read pipe ' + write_pipe_name + ' exists, but it is not a PIPE.')
        else:
            os.mkfifo(write_pipe_name)

        # Open PIPEs
        self.read_pipe = os.open(read_pipe_name, os.O_RDONLY | os.O_NONBLOCK)
        self.write_pipe = os.open(write_pipe_name, os.O_RDWR)
        
        # Create polling object for the reading PIPE 
        self.lensize = lensize 
        self.poll = select.poll()
        self.poll.register(self.read_pipe, select.POLLIN) 

        # Register the method cleanup so that it is called on destruction
        atexit.register(self.cleanup)


    def cleanup(self):
        os.close(self.read_pipe)
        os.close(self.write_pipe)


    def recv_whatever(self):
        """ @brief This methods uses pickle, so whatever object serialisable by pickle is good."""
        msg = None

        # If there is something available...
        if (self.read_pipe, select.POLLIN) in self.poll.poll(1):
            # Read the header containing the size of the message
            raw_msglen = os.read(self.read_pipe, self.lensize)
            msglen = struct.unpack(BaseIPC.lensize_dict[self.lensize], raw_msglen)[0]

            # Now we block until we can read the actual message
            while (self.read_pipe, select.POLLIN) not in self.poll.poll(1):
                continue
            
            # Read the actual message
            data_bytes = os.read(self.read_pipe, msglen)

            # Quick integrity check
            if len(data_bytes) != msglen:
                raise IOError('Message received has a different size than expected.')
            
            msg = pickle.loads(data_bytes)

        return msg


    def send_whatever(self, data):
        """ @brief This methods uses pickle, so whatever object serialisable by pickle is good."""
        data_bytes = pickle.dumps(data)
        msglen = struct.pack(BaseIPC.lensize_dict[self.lensize], len(data_bytes))
        os.write(self.write_pipe, msglen)
        os.write(self.write_pipe, data_bytes)


    def recv_ndarray(self, shape, dtype):
        """ 
        @brief      Pickle is quite slow for large numpy arrays, so we have this dedicated method.
        @param[in]  shape  Shape of the array you expect. Speed comes at a price, the tostring() 
                           method of numpy does not encode shape or dtype.
        @param[in]  dtype  Numpy.ndarray datatype (e.g. np.float32).
        @returns    either None (nothing was read) or a numpy.ndarray.
        """
        data = None

        if (self.read_pipe, select.POLLIN) in self.poll.poll(1):
            # Read the header containing the size of the message
            raw_msglen = os.read(self.read_pipe, self.lensize)
            msglen = struct.unpack(BaseIPC.lensize_dict[self.lensize], raw_msglen)[0]

            # Now we block until we can read the data
            while (self.read_pipe, select.POLLIN) not in self.poll.poll(1):
                continue
            
            # Read the data
            data_bytes = os.read(self.read_pipe, msglen)

            # Quick integrity check 
            if msglen != len(data_bytes):
                raise IOError('The amount of data read is different than expected.')

            data = np.fromstring(data_bytes, dtype=dtype).reshape(shape)

        return data


    def send_ndarray(self, data):
        """ 
        @brief      Pickle is quite slow for large numpy arrays, so we have this dedicated method.
        @param[in]  data  Numpy.ndarray.
        @returns    nothing.
        """
        data_bytes = data.tostring()
        msglen = struct.pack(BaseIPC.lensize_dict[self.lensize], len(data_bytes))
        os.write(self.write_pipe, msglen)
        nbw = os.write(self.write_pipe, data_bytes)
        if len(data_bytes) != nbw:
            raise IOError('The amount of data written is different than what it should be.')


if __name__ == "__main__":
    raise RuntimeError('The EasyIPC module is not a script and such not be executed as such.')
