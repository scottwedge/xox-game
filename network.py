import socket
import pickle
import xdrlib
import sys

# problem is in recieving end of the socket
# which points to the client
# game object data that is sent to the client
# is not read fully

class Network:
	def __init__(self, server, port):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server = server
		self.port = port
		self.addr = (self.server, self.port)
		self.client.connect(self.addr)

	def send(self,data):
		msg = pickle.dumps(data)
		self.client.sendall(msg)

	def recv(self):
		msg = self.client.recv(8192)
		return pickle.loads(msg)

	def send_recv(self, data):
		try:
			self.send(data)
			out = self.recv()
			return out
		except socket.error as e:
			print(e)