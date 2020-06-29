#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
@brief Example of use of the easyipc.Pipe class as a client.
       The only difference between server and client has to be
       the order of the FIFO names.
# @author Luis C. Garcia Peraza Herrera (luiscarlos.gph@gmail.com).abs
# @date   20 June 2020.
"""

import socket
import struct
import numpy as np
import sys

# My imports
import easyipc

def main():
    # Create IPC object for communications, you can use whatever
    # names you fancy for the PIPE names, as long as they are
    # specified to the server in reverse order
    ipc = easyipc.Pipe('haha')
    ipc.connect()

    # Send a dictionary to the server
    dic = {'Hello': 'This is an example.'}
    sys.stdout.write('[INFO] Sending a dictionary to the server... ')
    sys.stdout.flush()
    ipc.send_whatever(dic)
    sys.stdout.write("[OK]\n")

    # Wait for the dictionary to come back from the server
    sys.stdout.write('[INFO] Waiting for the server to send the dictionary back... ')
    sys.stdout.flush()
    dic_back = None
    while dic_back is None:
        dic_back = ipc.recv_whatever(blocking=False)
    sys.stdout.write("[OK]\n")
    
    # Send numpy array to server
    sys.stdout.write('[INFO] Sending a numpy.ndarray to the server... ')
    sys.stdout.flush()
    data = np.random.rand(32, 3, 1700, 1700).astype(np.float32)
    ipc.send_array(data)
    sys.stdout.write("[OK]\n")
    
    # Wait for the array to come back from the server
    sys.stdout.write('[INFO] Waiting for the server to send the array back... ')
    sys.stdout.flush()
    data_back = None
    while data_back is None:
        data_back = ipc.recv_array(blocking=False) 
    sys.stdout.write("[OK]\n")
    
if __name__ == "__main__":
    print('')
    main()
    print('')
