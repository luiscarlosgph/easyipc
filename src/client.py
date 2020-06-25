#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import struct
import numpy as np
import time

# My imports
import easyipc


""" 
@brief Example of use of the easyipc.DatagramIPC class as a server.
       The only difference between server and client has to be
       the order of the PIPE names.
"""
print('Running DatagramIPC client tests... ')
count = 0
maxcount = 20
eps = 1e-10
ipc = easyipc.DatagramIPC(host='localhost', port=6987)
data = None
while count < maxcount:
    # Send ping
    tic = time.time()
    batch = np.random.rand(32, 3, 1080, 1920).astype(np.float32)
    ipc.send_ndarray(batch)
    count +=1

    # Wait for pong
    reply = False
    while not reply:
        data = ipc.recv_ndarray(batch.shape, np.float32) 
        if data is not None:
            #print(data)
            reply = True
    toc = time.time()
    print('Elapsed round trip:', toc - tic)
    assert(np.sum(data - batch) < eps)
print('[OK]')

""" 
@brief Example of use of the easyipc.PipeIPC class as a server.
       The only difference between server and client has to be
       the order of the PIPE names.
"""
print('Running PipeIPC client tests... ')
count = 0
maxcount = 20
eps = 1e-10
ipc = easyipc.PipeIPC('jaja', 'jiji')
data = None
while count < maxcount:
    # Send ping
    tic = time.time()
    batch = np.random.rand(32, 3, 1080, 1920).astype(np.float32)
    ipc.send_ndarray(batch)
    count +=1

    # Wait for pong
    reply = False
    while not reply:
        data = ipc.recv_ndarray(batch.shape, np.float32) 
        if data is not None:
            #print(data)
            reply = True
    toc = time.time()
    print('Elapsed round trip:', toc - tic)
    assert(np.sum(data - batch) < eps)
print('[OK]')
