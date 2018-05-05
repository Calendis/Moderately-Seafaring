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

		self.final_level = 999
		self.level_to = None

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

	def get_spell_lines(self):
		return self.spell_lines


class TestClass(CharacterClass):
	"""docstring for TestClass"""
	def __init__(self):
		super(TestClass, self).__init__()
		self.name = "Test Class"
		self.hp_bonus = 5
		self.spd_bonus = 7
		self.ele_modifier = "Saturn"
		self.spell_lines = [Spell.test_line, Spell.basic_healer_line, Spell.neptune_line]
		

class Deckhand(CharacterClass):
	"""docstring for Deckhand"""
	def __init__(self):
		super(Deckhand, self).__init__()
		self.name = "Deckhand"
		self.hp_bonus = 1
		self.dfn_bonus = 1
		self.luk_bonus = 1
		self.spell_lines = [Spell.neptune_line, Spell.wrath_o_the_sea_line]

class Pirate(CharacterClass):
	"""docstring for Pirate"""
	def __init__(self):
		super(Pirate, self).__init__()
		self.name = "Pirate"
		self.hp_bonus = 4
		self.atk_bonus = 2
		self.dfn_bonus = 2
		self.luk_bonus = 4
		self.spd_bonus = 1
		self.spell_lines = [Spell.neptune_line, Spell.wrath_o_the_sea_line]

class Captain(CharacterClass):
	"""docstring for Captain"""
	def __init__(self):
		super(Captain, self).__init__()
		self.name = "Captain"
		self.hp_bonus = 7
		self.mp_bonus = 2
		self.atk_bonus = 6
		self.dfn_bonus = 4
		self.mag_bonus = 1
		self.res_bonus = 2
		self.spd_bonus = 4
		self.luk_bonus = 6
		self.spell_lines = [Spell.neptune_line, Spell.wrath_o_the_sea_line]
		
		
class WeakSlime(CharacterClass):
	"""docstring for WeakSlime"""
	def __init__(self):
		super(WeakSlime, self).__init__()
		self.name = "Weak Slime"

		self.spell_lines = [Spell.weak_slime_line]

class WeakFlying(CharacterClass):
	"""docstring for WeakFlying"""
	def __init__(self):
		super(WeakFlying, self).__init__()
		self.name = "Weak Flying"
		self.hp_bonus = 1

		self.spell_lines = [Spell.weak_flying_line]

class Servant(CharacterClass):
	"""docstring for Servant"""
	def __init__(self):
		super(Servant, self).__init__()
		self.name  = "Servant"
		self.hp_bonus = 2
		self.spd_bonus = 2
		self.spell_lines = [Spell.servant_line]
		