#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @brief  This module has unit tests for the classes of EasyIPC.
# @author Luis C. Garcia-Peraza Herrera (luiscarlos.gph@gmail.com).
# @date   25 June 2020.

import unittest
import os
import sys

# My imports
import easyipc

class TestEasyIPC(unittest.TestCase):

    def test_client_server_in_same_process(self):
        client_ipc = easyipc.FifoIPC('/tmp/haha', '/tmp/hihi')
        server_ipc = easyipc.FifoIPC('/tmp/hihi', '/tmp/haha')

    def test_client_in_fork(self):
        newpid = os.fork()
        if newpid == 0:
            client_ipc = easyipc.FifoIPC('/tmp/haha', '/tmp/hihi')
        else:
            server_ipc = easyipc.FifoIPC('/tmp/hihi', '/tmp/haha')

    def test_server_in_fork(self):
        newpid = os.fork()
        if newpid == 0:
            server_ipc = easyipc.FifoIPC('/tmp/hihi', '/tmp/haha')
        else:
            client_ipc = easyipc.FifoIPC('/tmp/haha', '/tmp/hihi')

    def test_fifo_pickle(self):
        client_ipc = easyipc.FifoIPC('/tmp/haha', '/tmp/hihi')
        server_ipc = easyipc.FifoIPC('/tmp/hihi', '/tmp/haha')

        # TODO: Send a dictionary (client -> server) and check integrity
        
        # TODO: Send a dictionary (server -> client) and check integrity

        pass
    
    def test_fifo_ndarray(self):
        pass

    def test_udp_pickle(self):
        pass

    def test_udp_ndarray(self):
        pass

if __name__ == '__main__':
    unittest.main()
