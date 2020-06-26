# EasyIPC
Easy-to-use Python library for inter-process communications.

# Installation
Using pip:
```
pip install easyipc --user
```
From source:
```
git clone https://github.com/luiscarlosgph/easyipc.git
cd easyipc
python setup.py build
python setup.py install --user
```

# Usage
Server:
```
import numpy as np
import easyipc

server = easyipc.Pipe('haha')
server.listen()  # Blocks until a client is connected
whatever_object = {'Hello': 'This is an example'}

# Send an object 
server.send_whatever(whatever_object)  # Blocks until all data is sent

# Send a numpy.ndarray: you can send numpy arrays with send_whatever(), but this is faster
shape = (32, 3, 1080, 1920)
dtype = np.float32
arr = np.ones(shape, dtype=dtype)
server.send_ndarray(arr)  # Block until all data is sent
```
Client:
```
import numpy as np
import easyipc

client = easyipc.Pipe('haha')
client.connect()  # Blocks until it can connect to a server

# Receive an object
whatever_object = client.recv_whatever()  # Blocks until it receives an object
print(whatever_object)

# Receive a numpy.ndarray
shape = (32, 3, 1080, 1920)
dtype = np.float32
arr = client.recv_ndarray(shape, dtype)  # Blocks until it receives an array
```
Too see some more examples click [here](https://github.com/luiscarlosgph/easyipc/tree/master/examples).

# Speed
In the [examples](https://github.com/luiscarlosgph/easyipc/tree/master/examples) folder, two timing scripts can be found: [pipe_timing_report.py](https://github.com/luiscarlosgph/easyipc/tree/master/examples/pipe_timing_report.py) and [zmq_timing_report.py](https://github.com/luiscarlosgph/easyipc/tree/master/examples/zmq_timing_report.py). The same operation is performed by both, a round trip of a numpy array of shape (32, 3, 1700, 1700), whose size if approximately 1GB. These are the results obtained in Ubuntu 16.04 on a machine with Intel(R) Core(TM) i7-4790K CPU @ 4.00GHz.
| Software                      | Time          |
| -------------                 | ------------- |
| EasyIPC                       | 1.8s          |
| [ZeroMQ](https://zeromq.org)  | 2.8s          |

# Unit testing
To run the tests execute:
```
python setup.py test
```

# Support
This code uses [FIFOs](https://man7.org/linux/man-pages/man7/pipe.7.html) (particularly [os.mkfifo](https://docs.python.org/3/library/os.html#os.mkfifo)), which are supported by Unix-like systems only. This code has been tested in Ubuntu 16.04 and Ubuntu 18.04.
