# Trait trees for Moderately Seafaring
from lib import Spell

class Trait():
	""" Base class for all traits """
	def __init__(self):
		super(Trait, self).__init__()
		self.stat_buffs = self.stats = {"hp": 0, "mp": 0, "atk": 0, "dfn": 0, "mag": 0, "res": 0, "spd": 0, "luk": 0}
		self.stat_lvlup_adders = self.stats = {"hp": 0, "mp": 0, "atk": 0, "dfn": 0, "mag": 0, "res": 0, "spd": 0, "luk": 0}
		self.stat_lvlup_multipliers = self.stats = {"hp": 1, "mp": 1, "atk": 1, "dfn": 1, "mag": 1, "res": 1, "spd": 1, "luk": 1}
		self.ele_dmg_adders = self.stats = {"mercury": 0, "venus": 0, "earth": 0, "mars": 0, "jupiter": 0, "saturn": 0, "uranus": 0, "neptune": 0}
		self.ele_res_adders = self.stats = {"mercury": 0, "venus": 0, "earth": 0, "mars": 0, "jupiter": 0, "saturn": 0, "uranus": 0, "neptune": 0}
		self.ele_dmg_multipliers = self.stats = {"mercury": 1, "venus": 1, "earth": 1, "mars": 1, "jupiter": 1, "saturn": 1, "uranus": 1, "neptune": 1}
		self.ele_res_multipliers = self.stats = {"mercury": 1, "venus": 1, "earth": 1, "mars": 1, "jupiter": 1, "saturn": 1, "uranus": 1, "neptune": 1}
		self.weapon_type_dmg_adders = {"staff": 0}
		self.weapon_type_dfn_adders = {"sword": 0}
		self.weapon_type_dmg_multipliers = {"axe": 1}
		self.weapon_type_dfn_multipliers = {"bow": 1}
		self.spell_lines = [Spell.test_line]
		self.name = "Unknown Trait"
		self.description = "Unknown description."
		self.cost = 999999
		self.prereq_lvl = 101
		self.prereq_traits = []
		self.prereq_stats = {"hp": 0, "mp": 0, "atk": 0, "dfn": 0, "mag": 0, "res": 0, "spd": 0, "luk": 0}
		self.antireq_traits = []
		self.antireq_stats = {"hp": 0, "mp": 0, "atk": 0, "dfn": 0, "mag": 0, "res": 0, "spd": 0, "luk": 0}

	def get_stat_buffs(self):
		return self.stat_buffs

	def get_stat_lvlup_adders(self):
		return self.stat_lvlup_adders

	def get_stat_lvlup_multipliers(self):
		return self.stat_lvlup_multipliers

	def get_ele_dmg_adders(self):
		return self.ele_dmg_adders

	def get_ele_res_adders(self):
		return self.ele_res_adders

	def get_ele_dmg_multipliers(self):
		return self.ele_dmg_multipliers

	def get_ele_res_multipliers(self):
		return self.ele_res_multipliers

	def get_weapon_type_dmg_adders(self):
		return self.weapon_type_dmg_adders

	def get_weapon_type_dfn_adders(self):
		return self.weapon_type_dfn_adders

	def get_weapon_type_dmg_multipliers(self):
		return self.weapon_type_dmg_multipliers

	def get_weapon_type_dfn_multipliers(self):
		return self.weapon_type_dfn_multipliers

	def get_spell_lines(self):
		return self.spell_lines

	def get_name(self):
		return self.name

	def get_cost(self):
		return self.cost

	def get_prereq_lvl(self):
		return self.prereq_lvl

	def get_prereq_traits(self):
		return self.prereq_traits

	def get_prereq_stats(self):
		return self.prereq_stats

	def get_antireq_traits(self):
		return self.antireq_traits

	def get_antireq_stats(self):
		return self.antireq_stats

	def get_description(self):
		return self.description

class WildernessEnthusiast(Trait):
	"""docstring for WildernessEnthusiast"""
	def __init__(self):
		super(WildernessEnthusiast, self).__init__()
		self.weapon_type_dmg_adders = {"axe": 10}
		self.ele_dmg_adders = self.stats = {"mercury": 0, "venus": 0, "earth": 0, "mars": 10, "jupiter": 0, "saturn": 0, "uranus": 0, "neptune": 0}
		self.cost = 10
		self.prereq_lvl = 5
		self.name = "Wilderness Enthusiast"
		self.description = "+ 10 damage with axes and Mars-based attacks."

class Survivalist(WildernessEnthusiast):
	"""docstring for Survivalist"""
	def __init__(self):
		super(Survivalist, self).__init__()
		self.weapon_type_dmg_multipliers = {"axe": 1.3}
		self.cost = 7
		self.prereq_lvl = 9
		self.prereq_traits.append(WildernessEnthusiast)
		self.name = "Survivalist"
		self.description = "1.3 times damage with axes."

class Stroud(Survivalist):
	"""docstring for Stroud"""
	def __init__(self):
		super(Stroud, self).__init__()
		self.ele_res_multipliers = self.stats = {"mercury": 1, "venus": 1, "earth": 1, "mars": 1.5, "jupiter": 1, "saturn": 1, "uranus": 1, "neptune": 2}
		self.cost = 45
		self.prereq_lvl = 36
		self.prereq_traits.append(Survivalist)
		self.name = "Stroud"
		self.description = "1.5 and 2 times resistance to Mars and Neptune, respectively."

class Wrangler(Trait):
	"""docstring for Wrangler"""
	def __init__(self):
		super(Wrangler, self).__init__()
		self.weapon_type_dmg_adders = {"whip": 15}
		self.cost = 6
		self.prereq_lvl = 2
		self.name = "Wrangler"
		self.description = "+15 damage with whips."

class Desperado(Wrangler):
	"""docstring for Desperado"""
	def __init__(self):
		super(Desperado, self).__init__()
		self.weapon_type_dmg_multipliers = {"whip": 1.5}
		self.stat_lvlup_adders = {"dfn": 2, "spd": 2}
		self.cost = 18
		self.prereq_lvl = 10
		self.prereq_traits.append(Wrangler)
		self.name = "Desperado"
		self.description = "*1.5 damage with whips, +2 DFN/lvl and SPD/lvl."

class ToughGuy(Trait):
	"""docstring for ToughGuy"""
	def __init__(self):
		super(ToughGuy, self).__init__()
		self.stat_lvlup_adders = {"dfn": 1, "res": 1}
		self.stat_lvlup_multipliers = {"hp": 1.1, "spd": 0.8}
		self.cost = 15
		self.prereq_lvl = 2
		self.name = "Tough Guy"
		self.description = "+1 DFN/lvl and RES/lvl.\n*1.1 and *0.8 HP and SPD\nper level, respectively."
		
class Bruiser(Trait):
	"""docstring for Bruiser"""
	def __init__(self):
		super(Bruiser, self).__init__()
		self.weapon_type_dmg_adders = {"mace": 10, "axe": 5, "sword": 1}
		self.stat_lvlup_multipliers = {"hp": 1.2, "spd": 0.7, "mp": 0.5}
		self.cost = 20
		self.prereq_lvl = 20
		self.prereq_traits.append(ToughGuy)
		self.name = "Bruiser"
		self.description = "+10 damage with maces, +5 with axes, +1 with swords.\n*1.2, 0.7, and 0.5 HP, SPD, and MP per level, respectively."

class Ranger(Stroud, Desperado):
	"""docstring for Ranger"""
	def __init__(self):
		super(Ranger, self).__init__()
		self.stat_lvlup_multipliers = {"spd": 1.3}
		self.stat_lvlup_adders = {"spd": 3}
		self.ele_res_multipliers = {"mercury": 1, "venus": 1, "earth": 2, "mars": 1.5, "jupiter": 1, "saturn": 1, "uranus": 1, "neptune": 2}
		self.spell_lines = [Spell.ranger_line]
		self.cost = 5000
		self.prereq_lvl = 50
		self.prereq_traits.append(Stroud)
		self.prereq_traits.append(Desperado)
		self.name = "Ranger"
		self.description = "*1.3 SPD/level, +3 SPD/level.\n *2 Earth resistance, *1.5 Mars resistance, *2 Neptune resistance.\nGives access to Ranger spells."

class Expert(Trait):
	"""docstring for Expert"""
	def __init__(self):
		super(Expert, self).__init__()
		self.buff_level = 20
		self.stat_buffs = self.stats = {"hp": self.buff_level, "mp": self.buff_level,
		"atk": self.buff_level, "dfn": self.buff_level, "mag": self.buff_level, "res": self.buff_level, "spd": self.buff_level, "luk": self.buff_level}
		self.cost = 15
		self.name = "Expert"
		self.description = "+"+str(self.buff_level)+" to all stats."
		self.prereq_lvl = 5
		
						
trait_list = (WildernessEnthusiast, Survivalist, Stroud, Wrangler, Desperado, ToughGuy, Bruiser, Ranger, Expert)