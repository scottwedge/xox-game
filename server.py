import socket
from _thread import *
#from player import Player
import pickle
from game import Game
import sys

def send_data(conn,data):
	msg = pickle.dumps(data)
	conn.sendall(msg)

def recv_data(conn):
	try:	
		msg = conn.recv(8192)
		return pickle.loads(msg), True
	except:
		return "error", False

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8192)
s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8192)

server = "192.168.178.24"
port = 5555

try:
	s.bind((server,port))
except socket.error as e:
	print(e)

# opening the port for listening the port
# 5 = only five clients can connect, if None = unlimited
s.listen(10)
print("Waiting for a connection, Server Started!\n")

# connected = set() # store IP addresses of connected clients
games = {} # store games - ID as key; Game object
# idCount = 0 # number of connected users
gameID = 0  # ID of game that user plays

# for each client we have on of this function running in the background
def threded_client(conn, pID, gameID):
	global idCount # to have the track of number of players at all times

	while True:
		try:
			data,flag = recv_data(conn)
			if gameID in games:
				game = games[gameID]

				if data=="reset":
					game.game_reset(pID)
				elif data!="get":
					flag = game.update_rect_list(pID,data)
					if flag:
						game.move(pID)
						game.check_if_finished(pID,data)

				send_data(conn,game)
			else:
				print("There is no game o.O. It was deleted")
				break
		except:
			break

	print("Lost connection")
	try:
		print("Closing game - ", games[gameID].game_name)
		del games[gameID]
		print()
	except:
		pass

	conn.close()

run_server = True
while run_server:
	conn, addr = s.accept()
	print("Conetcted to: ", addr) # IP address of connection

	# receive data initialisation from the client
	init_data, flag = recv_data(conn)

	# if we received data go!
	if flag:
		# if the user is creating the new game go!
		if init_data["new"]:
			p = 0 # player ID
			game_name = init_data["game"]
			games[game_name] = Game(game_name)
			games[game_name].create(p, init_data)
			print("Created the new game ", game_name)
			msg = {"ID"    : p,
				   "n"     : init_data["n"],
				   "m"     : init_data["m"],
				   "player": init_data["player"],
				   "game"  : game_name,
				   "block" : games[game_name].block_width}
			send_data(conn, msg)
			start_new_thread(threded_client, (conn, p, game_name))
		# if the user is requesting to join the game
		else:
			# join user to given game and return the game initial data
			game_name = init_data["game"]
			if (game_name in games):
				if (not games[game_name].ready):
					p = 1
					games[game_name].ready = True
					games[game_name].moved[0] = False
					games[game_name].player_names[1] = init_data["player"]
					print(games[game_name].player_names)
					print("Joining the game ", init_data["game"])
					print()
					msg = {"ID"    : p,
				   		   "n"     : games[game_name].n,
				   		   "m"     : games[game_name].m,
				   		   "player": init_data["player"],
				   		   "game"  : init_data["game"],
				   		   "block" : games[game_name].block_width}
					send_data(conn, msg)
					start_new_thread(threded_client, (conn, p, game_name))
				else:
					# user should be returned to the MainMenu()
					# send_data(conn, "no_game")
					send_data(conn, "occupied")
					print("game is full")
			else:
				# usre should be returned to the MainMenu()
				send_data(conn, "no_game")
				print("there is no this game")

	else:
		# game kill (socket error)
		send_data(conn, "socket_err")
		print("Bad inital data receive :/")
