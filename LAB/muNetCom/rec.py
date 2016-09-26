import time
import zmq
import curses

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5000")

buffer = socket.recv().decode('utf-8')
runNum = buffer.replace('@', '')

socket.send(b"Ok")
