#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
@brief Example of use of the easyipc.PipeIPC class as a client.
       The only difference between server and client has to be
       the order of the PIPE names.
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
    ipc = easyipc.PipeIPC('haha', 'hihi')

    # Send a dictionary to the server
    sys.stdout.write('[INFO] Sending a dictionary to the server... ')
    dic = {'Hello': 'This is a test'}
    tic_send = time.time()
    ipc.send_whatever(dic)
    toc_send = time.time()
    sys.stdout.write("Took " + str(toc_send - tic_send) + " seconds.\n")

    # Wait for the dictionary to come back from the server
    sys.stdout.write('[INFO] Waiting for the server to send the dictionary back... ')
    received = False
    dic_back = None
    tic_recv = time.time()
    while not received:
        dic_back = ipc.recv_whatever() 
        if dic_back is not None:
            received = True
    toc_recv = time.time()
    sys.stdout.write("Took " + str(toc_recv - tic_recv) + " seconds.\n")
    
    toc = time.time()
    print('[INFO] Elapsed round trip:', toc - tic)
    
    # Check that the dictionary we recived back is the same one we sent
    if dic_back['Hello'] == 'This is a test':
        sys.stdout.write("[OK]\n")
    else
        raise ValueError('[ERROR] We received something different.')
    
    tic = time.time()

    # Send numpy array to server
    sys.stdout.write('[INFO] Sending a numpy.ndarray to the server... ')
    data = np.random.rand(32, 3, 1080, 1920).astype(np.float32)
    tic_send = time.time()
    ipc.send_ndarray(data)
    toc_send = time.time()
    sys.stdout.write("Took " + str(toc_send - tic_send) + " seconds.\n")
    
    # Wait for the array to come back from the server
    sys.stdout.write('[INFO] Waiting for the server to send the array back... ')
    received = False
    data_back = None
    tic_recv = time.time()
    while not received:
        data_back = ipc.recv_ndarray(batch.shape, np.float32) 
        if data_back is not None:
            received = True
    toc_recv = time.time()
    sys.stdout.write("Took " + str(toc_recv - tic_recv) + " seconds.\n")
    
    toc = time.time()
    print('[INFO] Elapsed round trip:', toc - tic)
    
    # Check that the array we recived back is the same one we sent
    sys.stdout.write('[INFO] Checking that the array we received back is the same we sent... ')
    eps = 1e-10
    if np.sum(data - batch) < eps:
        sys.stdout.write("[OK]\n")
    else
        raise ValueError('[ERROR] We received something different.')

if __name__ == "__main__":
    print('')
    main()
    print('')
