#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
@brief    This script creates a FIFO client/server pair and times
          the time it takes to send 1GB of data among each other.
# @author Luis C. Garcia Peraza Herrera (luiscarlos.gph@gmail.com).abs
# @date   20 June 2020.
"""

import socket
import struct
import numpy as np
import sys
import time
import os

# My imports
import easyipc

def main():
    # Create a 1GB numpy.ndarray 
    shape = (32, 3, 1700, 1700)
    dtype = np.float32
    
    # Launch client and server
    newpid = os.fork()
    if newpid == 0:
        sys.stdout.write("Sending a 1GB numpy.ndarray... \n")
        sys.stdout.flush()

        # Create client
        client_ipc = easyipc.FifoIPC('haha')
        client_ipc.connect()

        # Create a random numpy array
        data = np.random.rand(*shape).astype(dtype)
        
        tic = time.time()
        
        # Ping
        client_ipc.send_ndarray(data)
        
        # Wait for the data to come back
        data_back = client_ipc.recv_ndarray(shape, dtype)

        toc = time.time()

        # Report
        sys.stdout.write("Round trip of a 1GB numpy.ndarray done in " + str(toc - tic) + " seconds.\n")

    else:
        server_ipc = easyipc.FifoIPC('haha')
        server_ipc.listen()

        # Wait for data to come in
        data_received = server_ipc.recv_ndarray(shape, dtype)

        # Pong
        server_ipc.send_ndarray(data_received)

    
if __name__ == "__main__":
    print('')
    main()
