#Classes for all in-game characters, inlcuding PCs, monsters, NPCs, etc.
from lib import CharacterImage
from lib import Item
from lib import CharacterClass

import pygame
screen = pygame.display.set_mode()

class Character(pygame.sprite.Sprite):
	"""docstring for Character"""
	def __init__(self, pos):
		super(Character, self).__init__()
		self.pos = pos
		self.old_pos = self.pos
		self.rect = pygame.Rect(self.pos[0], self.pos[1], 16, 32)
		self.feetrect = pygame.Rect(self.pos[0], self.pos[1]+16, 16, 32-16)
		self.velocity = [0,0]
		self.images = [0]
		self.frame = 0
		self.image = self.images[self.frame]
		
		self.title = "Default Title"
		self.name = "Default Name"
		self.character_class = CharacterClass.CharacterClass()
		
		self.hometown = "???"
		self.description = "Couldn't get a read on "+self.name+"!"
		
		self.items = [Item.GreenHerb(), Item.BrownHerb()]
		
		self.lvl = 0
		self.exp = 0
		
		self.hp = 0
		self.mp = 0
		self.atk = 0
		self.dfn = 0
		self.mag = 0
		self.res = 0
		self.spd = 0
		self.ele = []
		self.ele_weak = []
		self.ele_strong = []

		self.weapon = []
		self.armour= []
		self.shield = []
		self.rings = []
		self.w = 0
		self.a = 0

		self.statuses = []

	def draw(self):
		pass
		#screen.blit(self.image, self.pos)

	def update(self):
		self.image = self.images[self.frame]

		self.pos[0] += self.velocity[0]
		self.pos[1] += self.velocity[1]
		self.rect = pygame.Rect(self.pos[0], self.pos[1], 16, 32)
		self.feetrect = pygame.Rect(self.pos[0], self.pos[1]+16, 16, 32-16)

	def move_back(self):
		self.pos[0] -= self.velocity[0]
		self.pos[1] -= self.velocity[1]
		self.rect = pygame.Rect(self.pos[0], self.pos[1], 16, 32)
		self.feetrect = pygame.Rect(self.pos[0], self.pos[1]+16, 16, 32-16)

	def get_items(self):
		return(self.items)

	def get_name(self):
		return self.name

	def get_full_name(self):
		return self.title+" "+self.name+", "+self.character_class.get_name()

class CaptainRizzko(Character):
	"""docstring for CaptainRizzko"""
	def __init__(self, pos):
		super(CaptainRizzko, self).__init__(pos)
		self.images = [CharacterImage.rizzko_left, CharacterImage.rizzko_right]

		self.name = "Rizzko"
		self.race = "Kobold"
		self.title = "\"Captain\""
		self.hometown = "Rohlberg"
		self.character_class = CharacterClass.Deckhand()
		self.lvl = 1
		self.hp = 10
		self.mp = 0
		self.atk = 3
		self.dfn = 1
		self.mag = 0
		self.res = 1
		self.spd = 4

		self.maxspeed = round(1 + self.spd/100)

	def reload_images(self):
		self.images = [CharacterImage.rizzko_left, CharacterImage.rizzko_right]

class Zirkak(object):
	"""docstring for Zurkak"""
	def __init__(self, arg):
		super(Zurkak, self).__init__()
		self.images = []
		self.race = "Sahuagin"
		self.name = "Zurkak"
		self.title = "Ranger"
		
		
						