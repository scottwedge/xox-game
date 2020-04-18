# reduce pygame initialization? maybe that eats .exe memory also
# only load some of the functions
from network import Network
# import pickle
import time
from game import Game
import pygame
pygame.init()
pygame.mixer.quit()

import tkinter as tk

import main_menu

rect_pos_list = []
def draw_grid(win,n,m,block):
	global rect_pos_list
	for i_ in range(n):
		for j_ in range(m):
			rect = pygame.Rect(10+i_*block, 10+j_*block,
                               block, block)
			rect_pos = pygame.draw.rect(win, (0,0,0), rect, 1)
			rect_pos_list.append(rect_pos)

def draw_rects(win,game):
	for i_, rect in enumerate(game.rect_list):
			pygame.draw.rect(win,game.rect_color[i_],rect)

def init_game_win(dic):
	n, m, block = dic["n"], dic["m"], dic["block"]
	width = 10 + n*block + 10
	height = 10 + m*block + 10
	win = pygame.display.set_mode((width,height))
	pygame.display.set_caption("XOX - " + dic["player"] + " @ " + dic["game"])
	win.fill((255,255,255))
	draw_grid(win,n,m,block)
	return win

def score_update(game,labels):
	name1,name2,score1,score2 = labels
	name1.set(game.player_names[0])
	name2.set(game.player_names[1])
	score1.set(str(game.score[0]))
	score2.set(str(game.score[1]))

def score_window(master,labels):
	name1,name2,score1,score2 = labels

	score_frame = tk.Frame(master, borderwidth=2, relief=tk.GROOVE)
	score_frame.place(x=10,y=110,width=280,height=180)
	canvas = tk.Canvas(score_frame)
	canvas.place(x=10,y=10,width=260,height=160)

	# table
	canvas.create_rectangle(10,10,120,40)
	canvas.create_rectangle(120,10,240,40)
	canvas.create_rectangle(10,40,120,70)
	canvas.create_rectangle(120,40,240,70)

	name1.set("")
	l = tk.Label(canvas, textvariable=name1, font=(None,12))
	l.place(x=12,y=12,width=106,height=26)

	name2.set("")
	l = tk.Label(canvas, textvariable=name2, font=(None,12))
	l.place(x=124,y=12,width=106,height=26)

	score1.set("0")
	l = tk.Label(canvas, textvariable=score1, font=(None,12))
	l.place(x=12,y=42,width=106,height=26)

	score2.set("0")
	l = tk.Label(canvas, textvariable=score2, font=(None,12))
	l.place(x=124,y=42,width=106,height=26)

def result_update(frame,game,pID,clear=False):
	if not clear:
		if game.won[pID] and game.finish:
			text = "You won!"
			color = "green"
		else:
			text = "You lost!"
			color = "red"
		label = tk.Label(frame, text=text, fg=color, font=(None,20))
		label.place(x=20, y=20, width=240, height=50)
	else:
		label = tk.Label(frame, text=None, fg="red", font=(None,20))
		label.place(x=20, y=20, width=240, height=50)
		
def main(dic):
	pID = dic["ID"]
	win = init_game_win(dic)
	pygame.display.update()

	# Score and result window
	master = tk.Tk()
	master.title("Score window")
	master.geometry("300x300")
	master.resizable(0,0)

	result_frame = tk.Frame(master, borderwidth=2, relief=tk.GROOVE)
	result_frame.place(x=10,y=10,width=280,height=90)
	
	# changable text labels
	result_label = tk.StringVar()
	name1 = tk.StringVar()
	name2 = tk.StringVar()
	score1 = tk.StringVar()
	score2 = tk.StringVar()
	labels = [name1, name2, score1, score2]

	score_window(master,labels)
	
	clock = pygame.time.Clock()

	run = True
	while run:
		clock.tick(60)
		
		try:
			game = netw.send_recv("get")
		except:
			run = False
			print("did not sent or recieved game data")

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		if game.ready:
			if not game.moved[pID]:
				win.fill((255,255,255))
				pos = pygame.mouse.get_pos()
				press1,_,_ = pygame.mouse.get_pressed()
				for rect_pos in rect_pos_list:
					if rect_pos.collidepoint(pos) and press1:
						game = netw.send_recv(rect_pos)
						draw_rects(win,game)
						pygame.display.update()
						break
			else:
				win.fill((200,200,200))
		elif game.finish:
			win.fill((255,255,255))
			draw_grid(win,game.n,game.m,game.block_width)
			draw_rects(win,game)
			pygame.display.update()
			
			result_update(result_frame,game,pID)
			score_update(game,labels)
			master.update()
			
			pygame.time.delay(2500)
			game = netw.send_recv("reset")
			
			win.fill((255,255,255))
			result_update(result_frame,game,pID,True)
			master.update()
		else:
			win.fill((200,200,200))

		draw_grid(win,game.n,game.m,game.block_width)
		draw_rects(win,game)
		pygame.display.update()
		score_update(game,labels)
		master.update()

	pygame.display.quit()
	pygame.quit()

run_main = True
msg = ""
while run_main:
	good = main_menu.MainMenu(msg)

	if good:
		init_data = main_menu.game_init_data
		try:
			netw = Network(init_data["ip"],init_data["port"])
			dic = netw.send_recv(init_data)
			if (dic=="no_game"):
				msg = "No game by name '" + init_data["game"] + "'"
				print(msg)
				pass
			elif (dic=="occupied"):
				msg = "Game '" + init_data["game"] + "' full"
				print(msg)
				pass
			elif (dic=="socket_err"):
				print("Error in sending / recieveing data.")
				run_main = False
			else:
			 	# if everything is Ok start the game
				break
		except:
			msg = "Bad server address or IP"
			pass
	else:
		print("Exiting main menu.")
		run_main = False

if run_main:
	main(dic)

# init_data = {'n': 10, 'm': 10, 'max_len': 4, 'player': 'Dule', 'game': 'da', 'ip': '192.168.178.24', 'port': 5555, 'new': True}
# netw = Network(init_data["ip"],init_data["port"])
# dic = netw.send_recv(init_data)
# main(dic)