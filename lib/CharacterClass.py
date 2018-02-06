#Character classes and traits, since they are functionally identical
from lib import Spell

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
		self.ele_modifier = False

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
		
