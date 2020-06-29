#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
@brief    This script performs the same operation as 'pipe_timing_report.py'.
          It is intended to be a quick benchmark for communication of ndarrays.
# @author Luis C. Garcia Peraza Herrera (luiscarlos.gph@gmail.com).
# @date   26 June 2020.
"""

import struct
import numpy as np
import sys
import time
import os
import zmq


def send_array(socket, A, flags=0, copy=True, track=False):
    """send a numpy array with metadata"""
    md = dict(dtype = str(A.dtype), shape = A.shape,)
    socket.send_json(md, flags|zmq.SNDMORE)
    return socket.send(A, flags, copy=copy, track=track)


def recv_array(socket, flags=0, copy=True, track=False):
    """recv a numpy array"""
    md = socket.recv_json(flags=flags)
    msg = socket.recv(flags=flags, copy=copy, track=track)
    A = np.frombuffer(msg, dtype=md['dtype'])
    return A.reshape(md['shape'])


def main():
    # Create a 1GB numpy.ndarray 
    shape = (32, 3, 1700, 1700)
    dtype = np.float32
    
    # Launch client and server
    trials = 10
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
        
        times = []
        for trial in range(trials):
            tic = time.time()

            # Ping
            send_array(client_ipc, data)
            
            # Wait for the data to come back
            data_back = recv_array(client_ipc)

            toc = time.time()
            times.append(toc - tic)

        # Report
        sys.stdout.write("Round trip of a 1GB numpy.ndarray done in " + str(np.mean(times)) + " seconds.\n")

    else:
        server_context = zmq.Context()
        server_ipc = server_context.socket(zmq.REP)
        server_ipc.bind('ipc:///tmp/zmqtest')

        for trial in range(trials):
            # Wait for data to come in
            data_received = recv_array(server_ipc)

            # Pong
            send_array(server_ipc, data_received)

    
if __name__ == "__main__":
    print('')
    main()
