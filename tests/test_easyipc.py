#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @brief  This module has unit tests for the classes of EasyIPC.
# @author Luis C. Garcia-Peraza Herrera (luiscarlos.gph@gmail.com).
# @date   25 June 2020.

import unittest
import os
import sys
import numpy as np

# My imports
import easyipc

class TestEasyIPC(unittest.TestCase):
    
    def test_pipe(self):
        data = [np.random.rand(1000, 1000) for i in range(100)]
        newpid = os.fork()
        if newpid == 0:
            client = easyipc.Pipe('hoho')
            client.connect()
            client.send_whatever({'Hello': 'from the client'})
            for i in range(len(data)):
                client.send_array(data[i])
        else:
            server = easyipc.Pipe('hoho')
            server.listen()

            whatever = server.recv_whatever()
            self.assertTrue(whatever['Hello'] == 'from the client')
            
            for i in range(len(data)):
                data_back = server.recv_array()
                self.assertTrue(np.sum(data[i] - data_back) == 0)


if __name__ == '__main__':
    unittest.main()
