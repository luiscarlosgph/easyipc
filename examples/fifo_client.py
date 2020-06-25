#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
@brief Example of use of the easyipc.FifoIPC class as a client.
       The only difference between server and client has to be
       the order of the FIFO names.
# @author Luis C. Garcia Peraza Herrera (luiscarlos.gph@gmail.com).abs
# @date   20 June 2020.
"""

import socket
import struct
import numpy as np
import sys
import time

# My imports
import easyipc

def main():
    tic = time.time()
    
    # Create IPC object for communications, you can use whatever
    # names you fancy for the PIPE names, as long as they are
    # specified to the server in reverse order
    ipc = easyipc.FifoIPC('/tmp/haha', '/tmp/hihi')

    # Send a dictionary to the server
    dic = {'Hello': 'This is a test'}
    sys.stdout.write('[INFO] Sending a dictionary to the server... ')
    ipc.send_whatever(dic)
    sys.stdout.write("[OK]\n")

    # Wait for the dictionary to come back from the server
    sys.stdout.write('[INFO] Waiting for the server to send the dictionary back... ')
    received = False
    dic_back = None
    while not received:
        dic_back = ipc.recv_whatever() 
        if dic_back is not None:
            received = True
    sys.stdout.write("[OK]\n")
    
    # Send numpy array to server
    sys.stdout.write('[INFO] Sending a numpy.ndarray to the server... ')
    data = np.random.rand(32, 3, 1080, 1920).astype(np.float32)
    ipc.send_ndarray(data)
    
    # Wait for the array to come back from the server
    sys.stdout.write('[INFO] Waiting for the server to send the array back... ')
    received = False
    data_back = None
    while not received:
        data_back = ipc.recv_ndarray(data.shape, np.float32) 
        if data_back is not None:
            received = True
    sys.stdout.write("[OK]\n")
    
if __name__ == "__main__":
    print('')
    main()
    print('')
