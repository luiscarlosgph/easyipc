#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
@brief Example of use of the easyipc.FifoIPC class as a server.
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
    # Create IPC communications object
    sys.stdout.write('[INFO] Waiting for something to arrive... ')
    sys.stdout.flush()
    ipc = easyipc.FifoIPC('haha')
    ipc.listen()

    # Receive dictionary from the client 
    dic = None
    received = False
    while not received:
        dic = ipc.recv_whatever()
        if dic is not None:
            received = True
    sys.stdout.write("[OK]\n")
    sys.stdout.write("[INFO] We got this: ")
    print(dic)

    # Send dictionary back
    sys.stdout.write("[INFO] We are going to send it back to the client... ")
    sys.stdout.flush()
    ipc.send_whatever(dic)
    print("[OK]\n")

    # Receive numpy array from the client
    sys.stdout.write('[INFO] Waiting for an array to arrive... ')
    sys.stdout.flush()
    data = None
    received = False
    shape = (32, 3, 1080, 1920)
    dtype = np.float32
    while not received:
        data = ipc.recv_ndarray(shape, dtype)
        if data is not None:
            received = True
    sys.stdout.write("[OK]\n")
    sys.stdout.write('[INFO] We got an array of shape: ')
    print(data.shape)

    # Send array back
    sys.stdout.write("[INFO] We are going to send it back to the client... ")
    sys.stdout.flush()
    ipc.send_ndarray(data)
    print("[OK]\n")

if __name__ == "__main__":
    print('')
    main()
