#Character classes and traits, since they are functionally identical
from lib import Spell
from random import randint

class CharacterClass():
	"""docstring for CharacterClass"""
	def __init__(self):
		super(CharacterClass, self).__init__()
		self.name = "Default Character Class"
		self.hp_bonus = 0
		self.mp_bonus = 0
		self.atk_bonus = 0
		self.dfn_bonus = 0
		self.mag_bonus = 0
		self.res_bonus = 0
		self.spd_bonus = 0
		self.luk_bonus = 0
		self.ele_modifier = False

	def get_name(self):
		return self.name

	def get_hp_bonus(self):
		return self.hp_bonus+randint(0, 3)

	def get_mp_bonus(self):
		return self.mp_bonus+randint(0, 3)

	def get_atk_bonus(self):
		return self.atk_bonus+randint(0, 3)

	def get_dfn_bonus(self):
		return self.dfn_bonus+randint(0, 3)

	def get_mag_bonus(self):
		return self.mag_bonus+randint(0, 3)

	def get_res_bonus(self):
		return self.res_bonus+randint(0, 3)

	def get_spd_bonus(self):
		return self.spd_bonus+randint(0, 3)

	def get_luk_bonus(self):
		return self.luk_bonus+randint(0, 3)


class TestClass(CharacterClass):
	"""docstring for TestClass"""
	def __init__(self, arg):
		super(TestClass, self).__init__()
		self.name = "Test Class"
		self.hp_bonus = 5
		self.spd_bonus = 20
		self.ele_modifier = "Saturn"
		self.spell_lines = [Spell.test_line, Spell.basic_healer_line]
		

class Deckhand(CharacterClass):
	"""docstring for Deckhand"""
	def __init__(self):
		super(Deckhand, self).__init__()
		self.name = "Deckhand"
		self.hp_bonus = 1
		self.dfn_bonus = 1
		
