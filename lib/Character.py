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
		
		self.items = [Item.GreenHerb(), Item.BrownHerb(), Item.Healing_Potion_I(), Item.Dagger()]
		
		self.lvl = 0
		self.exp = 0
		self.exp_to_next = 0
		
		self.hp = 0
		self.mp = 0
		self.atk = 0
		self.dfn = 0
		self.mag = 0
		self.res = 0
		self.spd = 0
		self.luk = 0
		self.ele = []
		self.ele_weak = []
		self.ele_strong = []

		self.weapon = None
		self.armour= None
		self.shield = None
		self.rings = []
		self.w = 0
		self.a = 0

		self.statuses = []
		self.current_hp = self.hp
		self.current_mp = self.mp

	def draw(self):
		pass
		#screen.blit(self.image, self.pos)

	def update(self):
		self.image = self.images[self.frame]

		self.pos[0] += self.velocity[0]
		self.pos[1] += self.velocity[1]
		self.rect = pygame.Rect(self.pos[0], self.pos[1], 16, 32)
		self.feetrect = pygame.Rect(self.pos[0], self.pos[1]+16, 16, 32-16)

	def level_up(self):
		self.hp += self.character_class.get_hp_bonus()
		self.mp += self.character_class.get_mp_bonus()
		self.atk += self.character_class.get_atk_bonus()
		self.dfn += self.character_class.get_dfn_bonus()
		self.mag += self.character_class.get_mag_bonus()
		self.res += self.character_class.get_res_bonus()
		self.spd += self.character_class.get_spd_bonus()
		self.luk += self.character_class.get_luk_bonus()
		
		if self.get_lvl() == 0:
			self.current_hp = self.hp
			self.current_mp = self.mp

		self.lvl += 1
		self.exp = 0
		self.exp_to_next = (self.lvl**2)*(100)

	def move_back(self):
		self.pos[0] -= self.velocity[0]
		self.pos[1] -= self.velocity[1]
		self.rect = pygame.Rect(self.pos[0], self.pos[1], 16, 32)
		self.feetrect = pygame.Rect(self.pos[0], self.pos[1]+16, 16, 32-16)

	def clear_images(self):
		self.image = None
		self.images = []
		if self.weapon:
			self.weapon.image = None
		if self.armour:
			self.armour.image = None

	def heal(self, value, stat):
		if stat == "HP":
			self.current_hp += value
		elif stat == "MP":
			self.current_mp += value
		else:
			print("ERROR: The stat affected was unrecognized.")

	def equip(self, equipment):
		if equipment.get_item_type() == "Weapon":
			self.set_weapon(equipment)
		elif equipment.get_item_type == "Armour":
			self.set_armour(equipment)

	def unequip(self, equipment):
		if equipment.get_item_type() == "Weapon":
			self.set_weapon(None)
		elif equipment.get_item_type == "Armour":
			self.set_armour(None)

	def get_items(self):
		return(self.items)

	def get_name(self):
		return self.name

	def get_lvl(self):
		return self.lvl

	def get_full_name(self):
		return self.title+" "+self.name+", level "+str(self.get_lvl())+" "+self.character_class.get_name()

	def get_hp(self):
		return self.hp

	def get_current_hp(self):
		return self.current_hp

	def get_mp(self):
		return self.mp

	def get_current_mp(self):
		return self.current_mp

	def get_atk(self):
		return self.atk

	def get_dfn(self):
		return self.dfn

	def get_mag(self):
		return self.mag

	def get_res(self):
		return self.res

	def get_spd(self):
		return self.spd

	def get_luk(self):
		return self.luk

	def get_exp(self):
		return self.exp

	def get_exp_to_next(self):
		return self.exp_to_next

	def get_weapon_name(self):
		if self.weapon == None:
			return("None")
		return self.weapon.get_name()

	def get_weapon_power(self):
		if self.weapon == None:
			return(0)
		return self.weapon.get_power()

	def get_armour_name(self):
		if self.armour == None:
			return("None")
		return self.armour.get_name()

	def get_armour_power(self):
		if self.armour == None:
			return(0)
		return self.armour.get_defence()

	def get_weapon(self):
		return self.weapon

	def get_armour(self):
		return self.armour

	def set_weapon(self, new_weapon):
		self.weapon = new_weapon

	def set_armour(self, new_armour):
		self.armour = new_armour

class CaptainRizzko(Character):
	"""docstring for CaptainRizzko"""
	def __init__(self, pos):
		super(CaptainRizzko, self).__init__(pos)
		self.images = [CharacterImage.rizzko_left, CharacterImage.rizzko_right]

		self.name = "Rizzko"
		self.race = "Kobold"
		self.title = "\"Cap'n\""
		self.hometown = "Rohlberg"
		self.character_class = CharacterClass.Deckhand()
		self.lvl = 0
		self.hp = 10
		self.mp = 0
		self.atk = 3
		self.dfn = 1
		self.mag = 0
		self.res = 1
		self.spd = 4
		self.luk = 3

		self.maxspeed = round(1 + self.spd/100)
		self.level_up()

	def reload_images(self):
		self.images = [CharacterImage.rizzko_left, CharacterImage.rizzko_right]
		self.image = self.images[self.frame]
		if self.weapon:
			self.weapon.reload_image()
		if self.armour:
			self.armour.reload_image()

class Zirkak(object):
	"""docstring for Zurkak"""
	def __init__(self, arg):
		super(Zurkak, self).__init__()
		self.images = []
		self.race = "Sahuagin"
		self.name = "Zurkak"
		self.title = "Ranger"
		
		
						