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

# My imports
import easyipc

def main():
    trials = 10
    newpid = os.fork()
    if newpid == 0:
        sys.stdout.write("Sending a 1GB numpy.ndarray... \n")
        sys.stdout.flush()

        # Create client
        client_ipc = easyipc.Pipe('haha')
        client_ipc.connect()

        # Create a random numpy array
        data = np.random.rand(32, 3, 1700, 1700).astype(np.float32)
        
        # Do round trips and average time 
        times = [] 
        for trial in range(trials):
            
            tic = time.time()
            
            # Ping: send array
            client_ipc.send_array(data)
            
            # Wait for the data to come back
            data_back = client_ipc.recv_array()

            toc = time.time()

            # Report
            times.append(toc - tic)
        sys.stdout.write("Round trip of a 1GB numpy.ndarray done in " + str(np.mean(times)) + " seconds.\n")

    else:
        server_ipc = easyipc.Pipe('haha')
        server_ipc.listen()

        # Wait for data to come in
        for trial in range(trials):
            # Receive array
            data_received = server_ipc.recv_array()

            # Pong: send it back
            server_ipc.send_array(data_received)

    
if __name__ == "__main__":
    print('')
    main()
