import numpy as np
import sys
import random
import pygame
import pygame.surfarray as surfarray
from pygame.locals import *
from itertools import cycle
from qlearning4k.games.game import Game




# Global variables
fps = 30
screen_width  = 288
screen_height = 512
pygame.init()
fps_clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')
pipe_gap = 100
base_y = screen_height * 0.79
player_idx_gen = cycle([0, 1, 2, 1])

# Load images
images = {}
images['numbers'] = [pygame.image.load('resources/images/' + str(i) + '.png').convert_alpha() for i in range(10)]
images['player'] = [pygame.image.load('resources/images/bird_' + str(i) + '.png').convert_alpha() for i in range(3)]
images['background'] = pygame.image.load('resources/images/background.png').convert()
images['base'] = pygame.image.load('resources/images/base.png').convert_alpha()
images['pipes'] = [pygame.image.load('resources/images/pipe.png').convert_alpha()]
images['pipes'] += [pygame.transform.rotate(images['pipes'][0], 180)]

def get_hitmask(image):
	mask = []
	for x in range(image.get_width()):
		mask.append([])
		for y in range(image.get_height()):
			mask[x].append(bool(image.get_at((x, y))[3]))
	return mask
hitmasks = {x : map(get_hitmask, images[x]) for x in ['player', 'pipes']}
# Load sounds
ext = '.wav' if 'win' in sys.platform else '.ogg'
sound_names = ['die', 'hit', 'point', 'swoosh', 'wing']
sounds = {sound_name : 'resources/sounds/' + sound_name + ext for sound_name in sound_names}



player_width = images['player'][0].get_width()
player_height = images['player'][0].get_height()
pipe_width = images['pipes'][0].get_width()
pipe_height = images['pipes'][0].get_height()
background_height = images['background'].get_width()


class FlappyBird(Game):
	
	def __init__(self):
		self.reset()

	@property
	def name(self):
		return "FlappyBird"
	
	@property
	def nb_actions(self):
		return 2
	
	def reset(self):
		self.score = self.player_idx = self.looper_iter = 0
		self.player_x = int(screen_width * 0.2)
		self.player_y = int((screen_height - player_height) / 2)
		self.base_x = 0
		self.base_shift = images['base'].get_width() - background_height
		new_pipe_1 = get_random_pipe()
		new_pipe_2 = get_random_pipe()
		self.upper_pipes = [{'x': screen_width, 'y': new_pipe_1[0]['y']}, {'x': screen_width + (screen_width / 2), 'y': new_pipe_2[0]['y']},]
		self.lower_pipes = [{'x': screen_width, 'y': new_pipe_1[1]['y']},{'x': screen_width + (screen_width / 2), 'y': new_pipe_2[1]['y']},]
		self.pipe_velocity_x = -4
		self.player_velocity_y    =  0
		self.player_max_velocity =  10
		self.playerMinVelY =  -8
		self.player_acceleration_y    =   1
		self.player_flap_acceleration =  -9
		self.player_flapped = False
		self.game_over = False

	def play(self, action):
		pygame.event.pump()
		if action is 1:
			if self.player_y > -2 * player_height:
				self.player_velocity_y = self.player_flap_acceleration
				self.player_flapped = True
		playerMidPos = self.player_x + player_width / 2
		for pipe in self.upper_pipes:
			pipeMidPos = pipe['x'] + pipe_width / 2
			if pipeMidPos <= playerMidPos < pipeMidPos + 4:
				self.score += 1   			
		if (self.looper_iter + 1) % 3 == 0:
			self.player_idx = next(player_idx_gen)
		self.looper_iter = (self.looper_iter + 1) % 30
		self.base_x = -((-self.base_x + 100) % self.base_shift)
		if self.player_velocity_y < self.player_max_velocity and not self.player_flapped:
			self.player_velocity_y += self.player_acceleration_y
		if self.player_flapped:
			self.player_flapped = False
		self.player_y += min(self.player_velocity_y, base_y - self.player_y - player_height)
		if self.player_y < 0:
			self.player_y = 0
		for upper_pipe, lower_pipe in zip(self.upper_pipes, self.lower_pipes):
			upper_pipe['x'] += self.pipe_velocity_x
			lower_pipe['x'] += self.pipe_velocity_x
		if 0 < self.upper_pipes[0]['x'] < 5:
			newPipe = get_random_pipe()
			self.upper_pipes.append(newPipe[0])
			self.lower_pipes.append(newPipe[1])
		if self.upper_pipes[0]['x'] < -pipe_width:
			self.upper_pipes.pop(0)
			self.lower_pipes.pop(0)
		self.game_over = check_crash({'x': self.player_x, 'y': self.player_y,
							 'index': self.player_idx},
							self.upper_pipes, self.lower_pipes)
		screen.blit(images['background'], (0, 0))
		for upper_pipe, lower_pipe in zip(self.upper_pipes, self.lower_pipes):
			screen.blit(images['pipes'][0], (upper_pipe['x'], upper_pipe['y']))
			screen.blit(images['pipes'][1], (lower_pipe['x'], lower_pipe['y']))
		screen.blit(images['base'], (self.base_x, base_y))
		screen.blit(images['player'][self.player_idx],
					(self.player_x, self.player_y))
		self.state = pygame.surfarray.array3d(pygame.display.get_surface())
		pygame.display.update()
		fps_clock.tick(fps)

	def get_state(self):
		if not hasattr(self, 'state'):
			self.play(0)
		return self.state

	def get_score(self):
		return self.score

	def is_over(self):
		return self.game_over

	def is_won(self):
		return self.score > 5

	def get_frame(self):
		return np.resize(self.get_state(), (3, 80, 80)).sum(axis=0) / 3
		return cv2.cvtColor(cv2.resize(self.get_state(), (80, 80)), cv2.COLOR_BGR2GRAY)

	def draw(self):
		return np.resize(self.get_state(), (3, 80, 80))
		return cv2.resize(self.get_state(), (80, 80))


def get_random_pipe():
	gap_y = [20, 30, 40, 50, 60, 70, 80, 90]
	rand_gap = gap_y[random.randint(0, len(gap_y) - 1)] + int(base_y * 0.2)
	pipe_x = screen_width + 10
	return [{'x': pipe_x, 'y': rand_gap - pipe_height}, {'x': pipe_x, 'y': rand_gap + pipe_gap}]


def check_crash(player, upper_pipes, lower_pipes):
	pi = player['index']
	player['w'] = images['player'][0].get_width()
	player['h'] = images['player'][0].get_height()
	if player['y'] + player['h'] >= base_y - 1:
		return True
	else:
		player_rect = pygame.Rect(player['x'], player['y'], player['w'], player['h'])
		for upper_pipe, lower_pipe in zip(upper_pipes, lower_pipes):
			upper_pipe_rect = pygame.Rect(upper_pipe['x'], upper_pipe['y'], pipe_width, pipe_height)
			lower_pipe_rect = pygame.Rect(lower_pipe['x'], lower_pipe['y'], pipe_width, pipe_height)
			player_hit_mask = hitmasks['player'][pi]
			upper_hit_mask = hitmasks['pipes'][0]
			lower_hit_mask = hitmasks['pipes'][1]
			upper_collided = pixel_collision(player_rect, upper_pipe_rect, player_hit_mask, upper_hit_mask)
			lower_collided = (player_rect, lower_pipe_rect, player_hit_mask, lower_hit_mask)
			return upper_collided or lower_collided

def pixel_collision(rect1, rect2, hitmask1, hitmask2):
	rect = rect1.clip(rect2)
	if not (rect.width and rect.height):
		return False
	x1, y1 = rect.x - rect1.x, rect.y - rect1.y
	x2, y2 = rect.x - rect2.x, rect.y - rect2.y
	for x in range(rect.width):
		for y in range(rect.height):
			if hitmask1[x1 + x][y1 + y] and hitmask2[x2 + x][y2 + y]:
				return True
	return False
