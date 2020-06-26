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
    tic = time.time()

    # Create a 'client' and a 'server'
    shape = (32, 3, 170, 170)
    dtype = np.float32
    newpid = os.fork()
    if newpid == 0:
        # Child
        client_ipc = easyipc.FifoIPC('/tmp/haha', '/tmp/hihi')
        
        # Create a 1GB numpy.ndarray 
        data = np.random.rand(*shape).astype(dtype)
        
        # Send it to the server
        client_ipc.send_ndarray(data)
    else:
        # Parent
        server_ipc = easyipc.FifoIPC('/tmp/hihi', '/tmp/haha')
        
        # Get the numpy array
        #server_ipc.recv_ndarray(shape, dtype)
    
    # Send it and read it back
    #sys.stdout.write("Sending a 1GB numpy.ndarray... ")
    #sys.stdout.flush()
    #tic = time.time()
    #toc = time.time()
    #sys.stdout.write("Round trip of a 1GB numpy.ndarray done in " + str(toc - tic) + " seconds.\n")

    
if __name__ == "__main__":
    print('')
    main()
    print('')
