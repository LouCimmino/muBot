import zmq
import time

context = zmq.Context()

print ("starting muBot...")
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
print ("server found!.")

while True:
    print ("waiting for data...")
    message = socket.recv()
    print ("recv:", message)

    print ("send:", message)
    socket.send(message)
