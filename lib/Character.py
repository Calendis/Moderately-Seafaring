#Classes for all in-game characters, inlcuding PCs, monsters, NPCs, etc.
from lib import CharacterImage
from lib import Item
from lib import CharacterClass
from lib import Stat

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
		self.images = [CharacterImage.default_left, CharacterImage.default_right]
		self.spells = []
		self.frame = 0
		self.image = self.images[self.frame]
		
		self.title = "Default Title"
		self.name = "Default Name"
		self.character_class = CharacterClass.CharacterClass()
		
		self.hometown = "???"
		self.description = "Couldn't get a read on "+self.name+"!"
		
		self.items = [Item.GreenHerb(), Item.BrownHerb(), Item.Healing_Potion_I(), Item.Dagger(), Item.CrossRing()]
		
		self.lvl = 0
		self.exp = 0
		self.exp_to_next = 0
		
		hp = Stat.HitPoints(0)
		mp = Stat.ManaPoints(0)
		atk = Stat.Attack(0)
		dfn = Stat.Defence(0)
		mag = Stat.MagicalAttack(0)
		res = Stat.MagicalResistance(0)
		spd = Stat.Speed(0)
		luk = Stat.Luck(0)

		self.stats = {"hp": hp, "mp": mp, "atk": atk, "dfn": dfn, "mag": mag, "res": res, "spd": spd, "luk": luk}

		self.ele = []
		self.ele_weak = []
		self.ele_strong = []

		self.weapon = None
		self.armour= None
		self.shield = None
		self.accessory = None

		self.statuses = []
		self.current_hp = self.stats["hp"]
		self.current_mp = self.stats["mp"]

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
		#Adjust stats
		self.stats["hp"].shift_value(self.character_class.get_hp_bonus())
		self.stats["mp"].shift_value(self.character_class.get_mp_bonus())
		self.stats["atk"].shift_value(self.character_class.get_atk_bonus())
		self.stats["dfn"].shift_value(self.character_class.get_dfn_bonus())
		self.stats["mag"].shift_value(self.character_class.get_mag_bonus())
		self.stats["res"].shift_value(self.character_class.get_res_bonus())
		self.stats["spd"].shift_value(self.character_class.get_spd_bonus())
		self.stats["luk"].shift_value(self.character_class.get_luk_bonus())
		
		if self.get_lvl() == 0:
			self.current_hp = self.stats["hp"].get_value()
			self.current_mp = self.stats["mp"].get_value()

		#Adjust level and experience points
		self.lvl += 1
		self.exp = 0
		self.exp_to_next = (self.lvl**2)*(100)

		#Adjust spells
		for spell_line in self.get_spell_lines():
			for spell_master_level in spell_line.keys():
				if self.get_lvl() >= spell_master_level and spell_line[spell_master_level] not in self.spells:
					self.spells.append(spell_line[spell_master_level])

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
		if self.shield:
			self.shield.image = None
		if self.accessory:
			self.accessory.image = None

	def clear_spell_lines(self):
		for spell_line in self.get_spell_lines():
			for spell in spell_line.values():
				print(spell)
				spell.clear_image()

	def heal(self, value, stat):
		if stat.get_name() == "HP":
			self.current_hp += value
		elif stat.get_name() == "MP":
			self.current_mp += value
		else:
			print("ERROR: The stat affected was unrecognized.")

	def shift_current_mp(self, mp_offset):
		self.current_mp += mp_offset
		if self.current_mp < 0:
			self.current_mp = 0
		elif self.current_mp > self.mp:
			self.current_mp = self.mp

	def equip(self, equipment):
		if equipment.get_item_type() == "Weapon":
			self.set_weapon(equipment)
		elif equipment.get_item_type == "Armour":
			self.set_armour(equipment)
		elif equipment.get_item_type() == "Shield":
			self.set_shield(equipment)
		elif equipment.get_item_type() == "Accessory":
			self.set_accessory(equipment)

		self.shift_stats(equipment)

	def unequip(self, equipment):
		if equipment.get_item_type() == "Weapon":
			self.set_weapon(None)
		elif equipment.get_item_type == "Armour":
			self.set_armour(None)
		elif equipment.get_item_type() == "Shield":
			self.set_shield(None)
		elif equipment.get_item_type() == "Accessory":
			self.set_accessory(None)
		
		self.shift_stats(equipment, -1)

	def get_pos(self):
		return self.pos

	def get_items(self):
		return self.items

	def get_spells(self):
		return self.spells

	def get_spell_lines(self):
		return self.character_class.get_spell_lines()

	def get_name(self):
		return self.name

	def get_hometown(self):
		return self.hometown

	def get_lvl(self):
		return self.lvl

	def get_race(self):
		return self.race

	def get_full_name(self):
		return self.title+" "+self.name+" of "+self.get_hometown()+", level "+str(self.get_lvl())+" "+self.get_race()+" "+self.character_class.get_name()

	def get_hp(self):
		return self.stats["hp"].get_value()

	def get_current_hp(self):
		return self.current_hp

	def get_mp(self):
		return self.stats["mp"].get_value()

	def get_current_mp(self):
		return self.current_mp

	def get_atk(self):
		return self.stats["atk"].get_value()

	def get_dfn(self):
		return self.stats["dfn"].get_value()

	def get_mag(self):
		return self.stats["mag"].get_value()

	def get_res(self):
		return self.stats["res"].get_value()

	def get_spd(self):
		return self.stats["spd"].get_value()

	def get_luk(self):
		return self.stats["luk"].get_value()

	def get_exp(self):
		return self.exp

	def get_exp_to_next(self):
		return self.exp_to_next

	def get_weapon_name(self):
		if self.weapon:
			return self.weapon.get_name()
		return "None"

	def get_weapon_power(self):
		if self.weapon:
			return self.weapon.get_attack_stat().get_value()
		return 0

	def get_armour_name(self):
		if self.armour:
			return self.armour.get_name()
		return "None"

	def get_armour_power(self):
		if self.armour:
			return self.armour.get_defence_stat().get_value()
		return 0

	def get_shield_name(self):
		if self.shield:
			return shield.get_name()
		return "None"

	def get_shield_power(self):
		if self.shield:
			return shield.get_defence()
		return 0

	def get_accessory_name(self):
		if self.accessory:
			return self.accessory.get_name()
		return "None"

	def get_accessory_power(self):
		if self.accessory:
			return self.accessory.get_accessory_values()
		return 0

	def get_weapon(self):
		return self.weapon

	def get_armour(self):
		return self.armour

	def get_shield(self):
		return self.shield

	def get_accessory(self):
		return self.accessory

	def set_pos(self, new_pos):
		self.pos = new_pos

	def set_weapon(self, new_weapon):
		self.weapon = new_weapon

	def set_armour(self, new_armour):
		self.armour = new_armour

	def set_shield(self, new_shield):
		self.shield = new_shield

	def set_accessory(self, new_accessory):
		self.accessory = new_accessory

	def shift_stats(self, equipment, positive=1):
		print("Shifting stats!")
		self.stats["hp"].shift_value(equipment.stats["hp"].get_value()*positive)
		self.stats["mp"].shift_value(equipment.stats["mp"].get_value()*positive)
		print(equipment.stats["atk"].get_value())
		self.stats["atk"].shift_value(equipment.stats["atk"].get_value()*positive)
		self.stats["dfn"].shift_value(equipment.stats["dfn"].get_value()*positive)
		self.stats["mag"].shift_value(equipment.stats["mag"].get_value()*positive)
		self.stats["res"].shift_value(equipment.stats["res"].get_value()*positive)
		self.stats["spd"].shift_value(equipment.stats["spd"].get_value()*positive)
		self.stats["luk"].shift_value(equipment.stats["luk"].get_value()*positive)

		for el in equipment.ele:
			if positive:
				self.ele.append(el)
			else:
				self.ele.remove(el)

	def reload_gear_images(self):
		if self.weapon:
			self.weapon.reload_image()
		if self.armour:
			self.armour.reload_image()
		if self.shield:
			self.shield.reload_image()
		if self.accessory:
			self.accessory.reload_image()

	def reload_spell_lines(self):
		for spell_line in self.get_spell_lines():
			for spell in spell_line.values():
				spell.reload_image()

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
		self.stats["hp"] = Stat.HitPoints(10)
		self.stats["mp"] = Stat.ManaPoints(0)
		self.stats["atk"] = Stat.Attack(4)
		self.stats["dfn"] = Stat.Defence(1)
		self.stats["mag"] = Stat.MagicalAttack(0)
		self.stats["res"] = Stat.MagicalResistance(1)
		self.stats["spd"] = Stat.Speed(4)
		self.stats["luk"] = Stat.Luck(3)

		self.maxspeed = round(1 + self.stats["spd"].get_value()/100)
		self.level_up()

	def reload_images(self):
		self.images = [CharacterImage.rizzko_left, CharacterImage.rizzko_right]
		self.image = self.images[self.frame]
		self.reload_gear_images()

class Zirkak(Character):
	"""docstring for Zirkak"""
	def __init__(self, pos):
		super(Zirkak, self).__init__(pos)
		self.images = [CharacterImage.default_left, CharacterImage.default_right]
		self.race = "Sahuagin"
		self.title = ""
		self.name = "Zirkak"
		self.hometown = "Ieekauoreg"
		self.character_class = CharacterClass.TestClass()
		self.lvl = 0
		self.stats["hp"] = Stat.HitPoints(15)
		self.stats["mp"] = Stat.ManaPoints(0)
		self.stats["atk"] = Stat.Attack(2)
		self.stats["dfn"] = Stat.Defence(5)
		self.stats["mag"] = Stat.MagicalAttack(0)
		self.stats["res"] = Stat.MagicalResistance(3)
		self.stats["spd"] = Stat.Speed(1)
		self.stats["luk"] = Stat.Luck(1)

		self.maxspeed = round(1 + self.stats["spd"].get_value()/100)

		self.level_up()

		for i in range(50):
			self.level_up()

	def reload_images(self):
		self.images = [CharacterImage.default_left, CharacterImage.default_right]
		self.image = self.images[self.frame]
		self.reload_gear_images()