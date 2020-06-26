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
    shape = (32, 3, 17, 17)
    dtype = np.float32
    data = np.random.rand(*shape).astype(dtype)

    # Create a 'client' and a 'server'
    client_ipc = easyipc.FifoIPC('/tmp/haha', '/tmp/hihi')
    server_ipc = easyipc.FifoIPC('/tmp/hihi', '/tmp/haha')
    
    # Round trip
    sys.stdout.write("Sending a 1GB numpy.ndarray... ")
    sys.stdout.flush()
    tic = time.time()
    client_ipc.send_ndarray(data)
    #data_back = server_ipc.recv_ndarray(shape, dtype)
    toc = time.time()
    sys.stdout.write("[OK]\n")
    
    # Report
    sys.stdout.write("Round trip of a 1GB numpy.ndarray done in " + str(toc - tic) + " seconds.\n")
    
if __name__ == "__main__":
    print('')
    main()
