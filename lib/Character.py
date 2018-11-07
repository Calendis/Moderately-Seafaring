# Classes for all in-game characters, inlcuding PCs, monsters, NPCs, etc.
from lib import CharacterImage
from lib import Item
from lib import CharacterClass
from lib import Stat
from lib import CharacterName
from lib import Sound

from random import randint

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
		self.battle_pos = [0, 0]
		self.spells = []
		self.frame = 0
		self.image = self.images[self.frame]

		self.attack_sound = Sound.attack
		
		self.title = "Default Title"
		self.name = "Default Name"
		self.character_class = CharacterClass.CharacterClass()
		
		self.hometown = "???"
		self.description = "Couldn't get a read on "+self.name+"!"
		
		self.items = [Item.GreenHerb(), Item.BrownHerb(), Item.Healing_Potion_I(), Item.Dagger(), Item.Mana_Potion_I()]
		
		self.lvl = 0
		self.exp = 0
		self.exp_to_next = 0
		self.death_exp = 0
		
		hp = Stat.HitPoints(0)
		mp = Stat.ManaPoints(0)
		atk = Stat.Attack(0)
		dfn = Stat.Defence(0)
		mag = Stat.MagicalAttack(0)
		res = Stat.MagicalResistance(0)
		spd = Stat.Speed(0)
		luk = Stat.Luck(0)

		self.stats = {"hp": hp, "mp": mp, "atk": atk, "dfn": dfn, "mag": mag, "res": res, "spd": spd, "luk": luk}

		self.buffstats = {"atk": Stat.Attack(0), "dfn": Stat.Defence(0), "mag": Stat.MagicalAttack(0), "res": Stat.MagicalResistance(0), "spd": Stat.Speed(0), "luk": Stat.Luck(0)}

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
		self.defending = False

		self.collision_object = None
		self.layer = 2

		'''
			Lines are accessed by a dict key.
			Line format:
			Text to display, Options to give (if any), respectivedict keys to go to from options, items to give, auto T/F
		'''
		self.lines = {
			0: ["This message should not appear.\nERROR 60-0", ("Yes", "No"), (2, 3), None, False],
			1: ["This message should not appear.\nERROR 60-1", None, 1, None, False],
			2: ["This message should not appear.\nERROR 60-2", None, 1, Item.RedHerb, False],
			3: ["This message should not appear.\nERROR 60-3", None, 1, None, False]
		}
		self.current_line = 0

		self.line_delays = [0, 0, 0, 0]

	def draw(self):
		pass
		#screen.blit(self.image, self.pos)

	def update(self):
		if self.frame < len(self.images):
			self.image = self.images[self.frame]
		else:
			self.image = self.images[0]

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
		self.exp = self.exp - self.exp_to_next
		if self.exp < 0:
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

	def shift_battle_pos(self, shift_vector):
		self.battle_pos = (self.battle_pos[0]+shift_vector[0], self.battle_pos[1]+shift_vector[1])

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
				spell.clear_image()
				spell.clear_sound()

	def clear_sounds(self):
		self.attack_sound = None

	def heal(self, value, stat):
		if stat.get_name() == "HP":
			self.current_hp += value
		elif stat.get_name() == "MP":
			self.current_mp += value
		else:
			print("ERROR: The stat affected was unrecognized.")

		if self.get_current_hp() > self.get_hp():
			self.heal(self.get_hp() - self.get_current_hp(), Stat.HitPoints(0))

	def buff(self, value, statname):
		self.buffstats[statname].shift_value(value)

	def debuff(self, statname=False):
		if not statname: #Debuff all stats by default
			for statname in self.buffstats.keys():
				self.buffstats[statname].set_value(0)
		else:
			self.buffstats[statname].set_value(0)

	def full_heal(self):
		self.current_mp = self.get_mp()
		self.current_hp = self.get_hp()

	def shift_current_mp(self, mp_offset):
		self.current_mp += mp_offset
		if self.current_mp < 0:
			self.current_mp = 0
		elif self.current_mp > self.get_mp():
			self.current_mp = self.get_mp()

	def shift_exp(self, exp_offset):
		self.exp += exp_offset

		while self.exp >= self.exp_to_next:
			self.level_up()

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

	def advance_lines(self):
		#Text to display, Options to give (if any), respectivedict keys to go to from options, items to give, auto T/F

		self.current_line = self.lines[self.current_line][2]


	def get_pos(self):
		return self.pos

	def get_battle_pos(self):
		return self.battle_pos

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
		return self.stats["atk"].get_value() + self.buffstats["atk"].get_value()

	def get_dfn(self):
		return self.stats["dfn"].get_value() + self.buffstats["dfn"].get_value()

	def get_mag(self):
		return self.stats["mag"].get_value() + self.buffstats["mag"].get_value()

	def get_res(self):
		return self.stats["res"].get_value() + self.buffstats["res"].get_value()

	def get_spd(self):
		return self.stats["spd"].get_value() + self.buffstats["spd"].get_value()

	def get_luk(self):
		return self.stats["luk"].get_value() + self.buffstats["luk"].get_value()

	def get_exp(self):
		return self.exp

	def get_exp_to_next(self):
		return self.exp_to_next

	def get_death_exp(self):
		return self.death_exp

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

	def get_image(self):
		return self.image

	def get_battle_image(self):
		return pygame.transform.scale2x(self.image)

	def get_defending(self):
		return self.defending

	def get_statuses(self):
		return self.statuses

	def get_layer(self):
		return self.layer

	def get_lines(self):
		return self.lines

	def get_current_line(self):
		return self.current_line

	def get_line_delays(self):
		return self.line_delays

	def set_pos(self, new_pos):
		self.pos = new_pos

	def set_battle_pos(self, new_battle_pos):
		self.battle_pos = new_battle_pos

	def shift_battle_pos(self, new_rel_x, new_rel_y):
		self.battle_pos[0] += new_rel_x
		self.battle_pos[1] += new_rel_y

	def set_weapon(self, new_weapon):
		self.weapon = new_weapon

	def set_armour(self, new_armour):
		self.armour = new_armour

	def set_shield(self, new_shield):
		self.shield = new_shield

	def set_accessory(self, new_accessory):
		self.accessory = new_accessory

	def set_defending(self, new_defending):
		if new_defending.__class__ != bool:
			raise TypeError("defending must be True or False.")
		self.defending = new_defending

	def set_layer(self, new_layer):
		self.layer = new_layer

	def inflict_status(self, status):
		self.statuses.append(status)

	def cure_status(self, status):
		self.statuses.remove(status)

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
				spell.reload_sound()

	def reload_sounds(self):
		self.attack_sound = Sound.attack

class CaptainRizzko(Character):
	"""docstring for CaptainRizzko"""
	def __init__(self, pos, lvl):
		super(CaptainRizzko, self).__init__(pos)
		self.images = [CharacterImage.rizzko_left, CharacterImage.rizzko_right]
		self.image = self.images[self.frame]

		self.name = "Rizzko"
		self.race = "Kobold"
		self.title = "\"Cap'n\""
		self.hometown = "Rohlberg"
		self.character_class = CharacterClass.Deckhand()
		self.lvl = 0
		self.stats["hp"] = Stat.HitPoints(10)
		self.stats["mp"] = Stat.ManaPoints(3)
		self.stats["atk"] = Stat.Attack(4)
		self.stats["dfn"] = Stat.Defence(1)
		self.stats["mag"] = Stat.MagicalAttack(0)
		self.stats["res"] = Stat.MagicalResistance(1)
		self.stats["spd"] = Stat.Speed(4)
		self.stats["luk"] = Stat.Luck(3)

		self.maxspeed = round(1 + self.stats["spd"].get_value()/100)
		
		for i in range(lvl):
			self.level_up()
		
		self.full_heal()

	def reload_images(self):
		self.images = [CharacterImage.rizzko_left, CharacterImage.rizzko_right]
		if self.frame < len(self.images):
			self.image = self.images[self.frame]
		else:
			self.image = self.images[0]
		self.reload_gear_images()

	def reload_sounds(self):
		self.attack_sound = Sound.attack

class Zirkak(Character):
	"""docstring for Zirkak"""
	def __init__(self, pos, lvl):
		super(Zirkak, self).__init__(pos)
		self.images = [CharacterImage.default_left, CharacterImage.default_right]
		self.image = self.images[self.frame]
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

		for i in range(lvl):
			self.level_up()

		self.full_heal()

	def reload_images(self):
		self.images = [CharacterImage.default_left, CharacterImage.default_right]
		self.image = self.images[self.frame]
		self.reload_gear_images()

	def reload_sounds(self):
		self.attack_sound = Sound.attack

class Googlyblob(Character):
	"""A weak enemy"""
	def __init__(self, pos, lvl):
		super(Googlyblob, self).__init__(pos)

		self.images = [CharacterImage.googlyblob]
		self.image = self.images[self.frame]

		self.race = "Googlyblob"
		self.title = "Monster"
		self.name = "Googlyblob"
		self.description = "Googlyblob are a common phenomena formed from fresh dew and clay."
		self.character_class = CharacterClass.WeakSlime()
		self.lvl = 0
		self.stats["hp"] = Stat.HitPoints(4)
		self.stats["mp"] = Stat.ManaPoints(0)
		self.stats["atk"] = Stat.Attack(2)
		self.stats["dfn"] = Stat.Defence(2)
		self.stats["mag"] = Stat.MagicalAttack(0)
		self.stats["res"] = Stat.MagicalResistance(2)
		self.stats["spd"] = Stat.Speed(1)
		self.stats["luk"] = Stat.Luck(1)

		for i in range(lvl):
			self.level_up()

		self.death_exp = 4*self.lvl + 1

		self.full_heal()

	def get_battle_image(self):
		return self.image

	def reload_images(self):
		self.images = [CharacterImage.googlyblob]
		self.image = self.images[self.frame]
		self.reload_gear_images()

class BigBird(Character):
	"""docstring for BigBird"""
	def __init__(self, pos, lvl):
		super(BigBird, self).__init__(pos)

		self.images = [CharacterImage.big_bird]
		self.image = self.images[self.frame]

		self.race = "Monstrous Duck"
		self.title = "Monster"
		self.name = "Monstrous Duck"
		self.description = "Someone's pet duck, Tweets, escaped long ago and bred with the local monsters..."
		self.character_class = CharacterClass.WeakFlying()
		self.lvl = 0
		self.stats["hp"] = Stat.HitPoints(12)
		self.stats["mp"] = Stat.ManaPoints(5)
		self.stats["atk"] = Stat.Attack(20)
		self.stats["dfn"] = Stat.Defence(0)
		self.stats["mag"] = Stat.MagicalAttack(2)
		self.stats["res"] = Stat.MagicalResistance(3)
		self.stats["spd"] = Stat.Speed(3)
		self.stats["luk"] = Stat.Luck(0)

		for i in range(lvl):
			self.level_up()

		self.death_exp = 12*self.lvl + 0

		self.full_heal()

class GenericPirate(Character):
	"""docstring for GenericPirate"""
	def __init__(self, pos, lvl):
		super(GenericPirate, self).__init__(pos)
		
		self.images = [CharacterImage.pirates[randint(0, len(CharacterImage.pirates)-1)]]
		self.image = self.images[self.frame]

		self.race = "Human"
		self.title = ""
		self.name = CharacterName.GenerateName("pirate_male")
		self.description = "A ferocious pirate."
		self.character_class = CharacterClass.Pirate()
		self.lvl = 0
		self.stats["hp"] = Stat.HitPoints(randint(5, 12))
		self.stats["mp"] = Stat.ManaPoints(randint(0, 9))
		self.stats["atk"] = Stat.Attack(randint(2, 10))
		self.stats["dfn"] = Stat.Defence(randint(1, 9))
		self.stats["mag"] = Stat.MagicalAttack(randint(0, 6))
		self.stats["res"] = Stat.MagicalResistance(randint(3, 6))
		self.stats["spd"] = Stat.Speed(randint(0, 10))
		self.stats["luk"] = Stat.Luck(randint(4, 16))

		for i in range(lvl):
			self.level_up()

		self.death_exp = 12*(self.lvl+1)

		self.full_heal()

	def get_battle_image(self):
		return self.image

class GenericPirateCaptain(Character):
	"""docstring for GenericPirate"""
	def __init__(self, pos, lvl):
		super(GenericPirateCaptain, self).__init__(pos)
		
		self.images = [CharacterImage.pirates[randint(0, len(CharacterImage.pirates)-1)]]
		self.image = self.images[self.frame]

		self.race = "Human"
		self.title = "Captain"
		self.name = CharacterName.GenerateName("pirate_male")
		self.description = "The leader of a band of ferocious pirates."
		self.character_class = CharacterClass.Captain()
		self.lvl = 0
		self.stats["hp"] = Stat.HitPoints(randint(13, 23))
		self.stats["mp"] = Stat.ManaPoints(randint(5, 12))
		self.stats["atk"] = Stat.Attack(randint(7, 15))
		self.stats["dfn"] = Stat.Defence(randint(4, 13))
		self.stats["mag"] = Stat.MagicalAttack(randint(4, 8))
		self.stats["res"] = Stat.MagicalResistance(randint(7, 11))
		self.stats["spd"] = Stat.Speed(randint(8, 13))
		self.stats["luk"] = Stat.Luck(randint(10, 20))

		for i in range(lvl):
			self.level_up()
		
		self.death_exp = 20*self.lvl + 1

		self.full_heal()

class CocoonMan(Character):
	"""docstring for CocoonMan"""
	def __init__(self, pos, lvl):
		super(CocoonMan, self).__init__(pos)
		
		self.images = [CharacterImage.cocoon_man]
		self.image = self.images[self.frame]

		self.race = "Cocoon Man"
		self.title = ""
		self.name = "Cocoon Man"
		self.description = "This silent figure serves the Mothmaster. His cocoon looks soft."
		self.character_class = CharacterClass.Servant()
		self.lvl = 0
		self.stats["hp"] = Stat.HitPoints(30)
		self.stats["mp"] = Stat.ManaPoints(30)
		self.stats["atk"] = Stat.Attack(5)
		self.stats["dfn"] = Stat.Defence(1)
		self.stats["mag"] = Stat.MagicalAttack(14)
		self.stats["res"] = Stat.MagicalResistance(20)
		self.stats["spd"] = Stat.Speed(14)
		self.stats["luk"] = Stat.Luck(3)

		for i in range(lvl):
			self.level_up()

		self.death_exp = 30*self.lvl + 1

		self.full_heal()

class Avik(Character):
	"""docstring for Avik"""
	def __init__(self, pos):
		super(Avik, self).__init__(pos)
		self.race = "Kobold"
		self.title = ""
		self.name = "Avik Clearwater"
		
		self.lines = {
			0:["If you leave us Arbot, I'll whoop yer ass!\nDon't you have any respect for your elders?", None, 1, None, False],
			1:["Oh... I'm sorry for that little outburst.\nI was the same way when I was your age... \nAlways wanted adventure.. so energetic.\nIf anything, I was even more energetic!\nToday's youth are so lazy!", None, 2, None, False],
			2:["Oh, apologies for calling you lazy.\nThanks for stopping by to chat\nbefore you go, young'un.\nRemember me, Arbot.\n\nI hope you end up more successful than\nI did.", None, 3, Item.CrossRing, False],
			3:["Go on, get out of here!\n\nYou don't have to hang around any longer...", None, 3, 3, False]
		}

		self.line_delays = [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0]

class GenericOldMan(Character):
	"""docstring for GenericOldMan"""
	def __init__(self, pos):
		super(GenericOldMan, self).__init__(pos)
		self.race = "Human"
		self.title = ""
		self.name = CharacterName.GenerateName("human_male")
		self.images = [CharacterImage.old_man_overworld]

		self.lines = {
			0:["Ho hum.", None, 1, None, False],
			1:["I've nothing to say.", None, 0, None, False]
		}