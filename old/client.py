# reduce pygame initialization? maybe that eats .exe memory also
# only load some of the functions
import pygame
from network import Network
# import pickle
import time
from game import Game
pygame.init()
pygame.mixer.quit()

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

def write_result(win,game,pID):
	# print on the screen current game result (lost/won)
	w = pygame.display.get_surface().get_width()
	h = pygame.display.get_surface().get_height()
	
	font = pygame.font.SysFont("comicsans", 40)
	if game.won[pID]:
		txt = "You won!"
		text = font.render(txt, 1, (200,0,0))
	else:
		txt = "You lost!"
		text = font.render(txt, 1, (0,200,0))

	xpos = 10+game.n*game.block_width+10
	text_height = round(text.get_height()/2)
	ypos = 20 + text_height
	width = round((w-10-xpos)/2)
	height = 70
	label = pygame.Rect(xpos, ypos, width, height)
	win.blit(text, (xpos + round(width/2) - round(text.get_width()/2),
					 ypos + round(height/2) - round(text.get_height()/2)))

def draw_table(win,game):
	# and table with full score of the given game
	w = pygame.display.get_surface().get_width()
	h = pygame.display.get_surface().get_height()
	xbeg = 10+game.n*game.block_width+10
	height = 35
	ybeg = round(h/2) - 35
	width = round((w-10-xbeg)/2)

	font = pygame.font.SysFont("comicsans", 30)
	font = pygame.font.SysFont("arial", 20)
	
	r1 = pygame.Rect(xbeg, ybeg, width, height)
	pygame.draw.rect(win, (0,0,0), r1, 1)
	text = font.render(game.player_names[0], 1, (0,0,0))
	win.blit(text, (xbeg + round(width/2) - round(text.get_width()/2),
					 ybeg + round(height/2) - round(text.get_height()/2)))
	
	r2 = pygame.Rect(xbeg+width, ybeg, width, height)
	pygame.draw.rect(win, (0,0,0), r2, 1)
	text = font.render(game.player_names[1], 1, (0,0,0))
	win.blit(text, (xbeg+width + round(width/2) - round(text.get_width()/2),
					 ybeg + round(height/2) - round(text.get_height()/2)))
	
	s1 = pygame.Rect(xbeg,ybeg+height,width,height)
	pygame.draw.rect(win, (0,0,0), s1, 1)
	text = font.render(str(game.score[0]), 1, (0,0,0))
	win.blit(text, (xbeg + round(width/2) - round(text.get_width()/2),
					 ybeg+height + round(height/2) - round(text.get_height()/2)))
	
	s2 = pygame.Rect(xbeg+width, ybeg+height,width,height)
	pygame.draw.rect(win, (0,0,0), s2, 1)
	text = font.render(str(game.score[1]), 1, (0,0,0))
	win.blit(text, (xbeg+width + round(width/2) - round(text.get_width()/2),
					 ybeg+height + round(height/2) - round(text.get_height()/2)))

def init_game_win(dic):
	n, m, block = dic["n"], dic["m"], dic["block"]
	width = 10 + n*block + 10
	height = 10 + m*block + 10
	width += 300
	win = pygame.display.set_mode((width,height))
	pygame.display.set_caption("XOX - " + dic["player"] + " (" + str(dic["ID"]+1) + ") @ " + dic["game"])
	win.fill((255,255,255))
	draw_grid(win,n,m,block)
	return win

def main(dic):
	pID = dic["ID"]
	win = init_game_win(dic)
	pygame.display.update()
	
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
				pos = pygame.mouse.get_pos()
				press1,_,_ = pygame.mouse.get_pressed()
				for rect_pos in rect_pos_list:
					if rect_pos.collidepoint(pos) and press1:
						game = netw.send_recv(rect_pos)
						draw_rects(win,game)
						pygame.display.update()
						break
		elif game.finish:
			write_result(win,game,pID)
			pygame.display.update()
			pygame.time.delay(2000)
			game = netw.send_recv("reset")
			win.fill((255,255,255))
			draw_grid(win,game.n,game.m,game.block_width)

		draw_table(win,game)
		draw_rects(win,game)
		pygame.display.update()

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