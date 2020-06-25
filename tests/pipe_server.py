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
print('Running DatagramIPC server... ')
count = 0
maxcount = 20
ipc = easyipc.DatagramIPC(host='localhost', port=6987)
data = None
while count < maxcount:
    # Wait for ping
    reply = False
    while not reply:
        data = ipc.recv_ndarray((32, 3, 108, 192), np.float32) 
        if data is not None:
            #print(data)
            reply = True

    # Send pong
    ipc.send_ndarray(data)
    count += 1
print('[OK]')


""" 
@brief Example of use of the easyipc.PipeIPC class as a server.
       The only difference between server and client has to be
       the order of the PIPE names.
"""
print('Running PipeIPC server... ')
count = 0
maxcount = 20
ipc = easyipc.PipeIPC('hihi', 'haha')
data = None
while count < maxcount:
    # Wait for ping
    reply = False
    while not reply:
        data = ipc.recv_ndarray((32, 3, 1080, 1920), np.float32) 
        if data is not None:
            #print(data)
            reply = True

    # Send pong
    ipc.send_ndarray(data)
    count += 1
print('[OK]')

