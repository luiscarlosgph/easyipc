#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
@brief    This script creates a FIFO client/server pair and times
          the time it takes to send 1GB of data among each other.
# @author Luis C. Garcia Peraza Herrera (luiscarlos.gph@gmail.com).abs
# @date   20 June 2020.
"""

import struct
import numpy as np
import sys
import time
import os
import zmq

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
        client_context = zmq.Context()
        client_ipc = client_context.socket(zmq.REQ)
        client_ipc.connect('ipc:///tmp/zmqtest')

        # Create a random numpy array
        data = np.random.rand(*shape).astype(dtype)
        
        tic = time.time()

        # Ping
        client_ipc.send(data.tobytes())
        
        # Wait for the data to come back
        data_back = np.frombuffer(client_ipc.recv(), dtype=dtype).reshape(shape)

        toc = time.time()

        # Report
        sys.stdout.write("Round trip of a 1GB numpy.ndarray done in " + str(toc - tic) + " seconds.\n")

    else:
        server_context = zmq.Context()
        server_ipc = server_context.socket(zmq.REP)
        server_ipc.bind('ipc:///tmp/zmqtest')

        # Wait for data to come in
        data_received = np.frombuffer(server_ipc.recv(), dtype=dtype).reshape(shape)

        # Pong
        server_ipc.send(data_received.tobytes())

    
if __name__ == "__main__":
    print('')
    main()
