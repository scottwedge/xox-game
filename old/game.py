import numpy as np

class Game:
	def __init__(self, game_name):
		self.n = None
		self.m = None
		self.max_len = None
		self.player_names = [None,None]
		self.game_name = game_name
		self.block_width = 30
		self.matrix = None
		self.moved = [True,True]
		self.ready = False
		self.finish = False
		self.colors = [(255,0,0),(0,0,255)]
		self.rect_list = []
		self.rect_color = []
		self.init_data = None
		self.won = [False,False]
		self.score = [0,0]

	def create(self,playerID,dic):
		self.n = dic["n"]
		self.m = dic["m"]
		self.max_len = dic["max_len"]
		self.player_names[playerID] = dic["player"]
		self.matrix = np.zeros((self.n,self.m))#[[0]*self.n]*self.m
		self.init_data = dic

	def move(self, pID):
		if pID == 0:
			self.moved[0] = True
			self.moved[1] = False
		else:
			self.moved[1] = True
			self.moved[0] = False
		pass

	def game_reset(self):
		self.ready = True
		self.finish = False
		self.moved = [False,True]
		self.won = [False,False]
		self.rect_list = []
		self.rect_color = []
		self.matrix = np.zeros((self.n, self.m))

	def update_rect_list(self,pID,rect_pos):
		xpos = int((rect_pos.centerx-10-self.block_width/2)/self.block_width)
		ypos = int((rect_pos.centery-10-self.block_width/2)/self.block_width)
		if self.matrix[xpos][ypos] == 0:
			self.matrix[xpos][ypos] = pID+1
			self.rect_list.append(rect_pos)
			self.rect_color.append(self.colors[pID])
			good = True
		else:
			good = False

		return good

	def check_if_finished(self,pID,rect_pos):
		xpos = int((rect_pos.centerx-10-self.block_width/2)/self.block_width)
		ypos = int((rect_pos.centery-10-self.block_width/2)/self.block_width)
		counter = 1
		
		# sta ako je odigrano polje u sred niza? :)

		# right check
		for i_ in range(1,self.max_len):
			if xpos+i_ < self.n:
				if self.matrix[xpos+i_][ypos] == pID+1:
					counter += 1
					if counter == self.max_len:
						self.ready = False
						self.finish = True
						self.won[pID] = True
						self.score[pID] += 1
				else:
					counter = 1
					break
			else:
				break
		
		# left check
		for i_ in range(1,self.max_len):
			if xpos-i_ >= 0:
				if self.matrix[xpos-i_][ypos] == pID+1:
					counter += 1
					if counter == self.max_len:
						self.ready = False
						self.finish = True
						self.won[pID] = True
						self.score[pID] += 1
				else:
					counter = 1
					break
			else:
				break
		
		# up check
		for i_ in range(1,self.max_len):
			if ypos-i_ >= 0:
				if self.matrix[xpos][ypos-i_] == pID+1:
					counter += 1
					if counter == self.max_len:
						self.ready = False
						self.finish = True
						self.won[pID] = True
						self.score[pID] += 1
				else:
					counter = 1
					break
			else:
				break

		# down check
		for i_ in range(1,self.max_len):
			if ypos+i_ < self.m:
				if self.matrix[xpos][ypos+i_] == pID+1:
					counter += 1
					if counter == self.max_len:
						self.ready = False
						self.finish = True
						self.won[pID] = True
						self.score[pID] += 1
				else:
					counter = 1
					break
			else:
				break

		# up-right check
		for i_ in range(1,self.max_len):
			if (xpos+i_<self.n) and (ypos-i_>= 0):
				if self.matrix[xpos+i_][ypos-i_] == pID+1:
					counter += 1
					if counter == self.max_len:
						self.ready = False
						self.finish = True
						self.won[pID] = True
						self.score[pID] += 1
				else:
					counter = 1
					break
			else:
				break

		# up-left check
		for i_ in range(1,self.max_len):
			if (xpos-i_>= 0) and (ypos-i_>= 0):
				if self.matrix[xpos-i_][ypos-i_] == pID+1:
					counter += 1
					if counter == self.max_len:
						self.ready = False
						self.finish = True
						self.won[pID] = True
						self.score[pID] += 1
				else:
					counter = 1
					break
			else:
				break

		# down-left check
		for i_ in range(1,self.max_len):
			if (xpos-i_>= 0) and (ypos+i_< self.m):
				if self.matrix[xpos-i_][ypos+i_] == pID+1:
					counter += 1
					if counter == self.max_len:
						self.ready = False
						self.finish = True
						self.won[pID] = True
						self.score[pID] += 1
				else:
					counter = 1
					break
			else:
				break

		# down-right check
		for i_ in range(1,self.max_len):
			if (xpos+i_< self.n) and (ypos+i_< self.m):
				if self.matrix[xpos+i_][ypos+i_] == pID+1:
					counter += 1
					if counter == self.max_len:
						self.ready = False
						self.finish = True
						self.won[pID] = True
						self.score[pID] += 1
				else:
					counter = 1
					break
			else:
				break