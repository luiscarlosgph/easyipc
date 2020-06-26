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
import easyipc
server = easyipc.Pipe('haha')
server.listen()                                    # Blocks until a client is connected
whatever_object = {'Hello': 'This is an example'}
server.send_whatever(whatever_object)              # Blocks until all the data is sent
```
Client:
```
import easyipc
client = easyipc.Pipe('haha')
client.connect()                          # Blocks until it can connect to a server
whatever_object = client.recv_whatever()  # Blocks until it receives an object
print(whatever_object)
```
Too see some more examples click [here](https://github.com/luiscarlosgph/easyipc/tree/master/examples).

# Unit testing
To run the tests execute:
```
python setup.py test
```
