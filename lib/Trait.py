# Trait trees for Moderately Seafaring
from lib import Spell

class Trait():
	""" Base class for all traits """
	def __init__(self):
		super(Trait, self).__init__()
		self.stat_buffs = self.stats = {"hp": 0, "mp": 0, "atk": 0, "dfn": 0, "mag": 0, "res": 0, "spd": 0, "luk": 0}
		self.stat_lvlup_adders = self.stats = {"hp": 0, "mp": 0, "atk": 0, "dfn": 0, "mag": 0, "res": 0, "spd": 0, "luk": 0}
		self.stat_lvlup_multipliers = self.stats = {"hp": 1, "mp": 1, "atk": 1, "dfn": 1, "mag": 1, "res": 1 "spd": 1, "luk": 1}
		self.ele_dmg_adders = self.stats = {"mercury": 0, "venus": 0, "earth": 0, "mars": 0, "jupiter": 0, "saturn": 0, "uranus": 0, "neptune": 0}
		self.ele_res_adders = self.stats = {"mercury": 0, "venus": 0, "earth": 0, "mars": 0, "jupiter": 0, "saturn": 0, "uranus": 0, "neptune": 0}
		self.ele_dmg_multipliers = self.stats = {"mercury": 1, "venus": 1, "earth": 1, "mars": 1, "jupiter": 1, "saturn": 1, "uranus": 1, "neptune": 1}
		self.ele_res_multipliers = self.stats = {"mercury": 1, "venus": 1, "earth": 1, "mars": 1, "jupiter": 1, "saturn": 1, "uranus": 1, "neptune": 1}
		self.weapon_type_dmg_adders = {"staff": 0}
		self.weapon_type_dfn_adders = {"sword": 0}
		self.weapon_type_dmg_multipliers = {"axe": 1}
		self.weapon_type_dfn_multipliers = {"bow": 1}
		self.spell_lines = Spell.test_line
		self.name = "Unknown Trait"
		self.cost = 999999
		self.prereq = {"lvl":101, "trait": None}		

class WildernessEnthusiast(Trait):
	"""docstring for WildernessEnthusiast"""
	def __init__(self):
		super(WildernessEnthusiast, self).__init__()
		self.weapon_type_dmg_adders = {"axe": 10}
		self.ele_dmg_adders = self.stats = {"mercury": 0, "venus": 0, "earth": 0, "mars": 10, "jupiter": 0, "saturn": 0, "uranus": 0, "neptune": 0}
		self.cost = 10
		self.prereq = {"lvl": 5, "trait": None}

class Survivalist(WildernessEnthusiast):
	"""docstring for Survivalist"""
	def __init__(self):
		super(Survivalist, self).__init__()
		self.weapon_type_dmg_multipliers = {"axe": 1.3}
		self.cost = 7
		self.prereq = {"lvl": 9, "trait": WildernessEnthusiast}

class Stroud(Survivalist):
	"""docstring for Stroud"""
	def __init__(self):
		super(Stroud, self).__init__()
		self.ele_res_multipliers = self.stats = {"mercury": 1, "venus": 1, "earth": 1, "mars": 1, "jupiter": 1, "saturn": 1, "uranus": 1, "neptune": 2}