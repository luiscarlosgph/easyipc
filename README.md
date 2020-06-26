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
arr = client.recv_ndarray()  # Blocks until it receives an array
```
Too see some more examples click [here](https://github.com/luiscarlosgph/easyipc/tree/master/examples).

# Unit testing
To run the tests execute:
```
python setup.py test
```
