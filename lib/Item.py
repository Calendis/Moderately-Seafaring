#Classes for items in Moderately Seafaring
from lib import ItemImage
from lib import Stat

class Item(object):
	"""docstring for Item"""
	def __init__(self):
		super(Item, self).__init__()
		self.name = "Unknown item"
		self.description = "Default item description."
		self.item_type = "Default Item Type"
		self.equippable = False
		self.useable = False
		self.stat = None
		self.value = 0
		self.price = 0
		self.ele = []
		self.image = ItemImage.default

	def get_name(self):
		return self.name

	def get_description(self):
		return self.description

	def get_image(self):
		return self.image

	def get_useable(self):
		return self.useable

	def get_equippable(self):
		return self.equippable

	def get_item_type(self):
		return self.item_type

	def get_stat(self):
		return self.stat

	def get_value(self):
		return self.value

	def get_stats(self):
		return self.stats

	def get_attack_stat(self):
		return self.stats["atk"]

	def get_defence_stat(self):
		return self.stats["dfn"]

	def clear_image(self):
		self.image = None

	def reload_image(self):
		self.image = ItemImage.default

class Equippable(Item):
	"""docstring for Equippable"""
	def __init__(self):
		super(Equippable, self).__init__()
		self.item_type = "Equippable"
		self.equippable = True
		self.stats = {"hp": Stat.HitPoints(0), "mp": Stat.ManaPoints(0),
		"atk": Stat.Attack(0), "dfn": Stat.Defence(0),
		"mag": Stat.MagicalAttack(0), "res": Stat.MagicalResistance(0),
		"spd": Stat.Speed(0), "luk": Stat.Luck(0)}

class Weapon(Equippable):
	"""docstring for Weapon"""
	def __init__(self, atk_bonus):
		super(Weapon, self).__init__()
		self.item_type = "Weapon"
		self.atk_bonus = atk_bonus
		self.stats["atk"].set_value(self.atk_bonus)
		self.description_ending = "Weapon power: "+str(self.atk_bonus)+"."
		self.description = "A weapon."

class Armour(Equippable):
	"""docstring for Armour"""
	def __init__(self, dfn_bonus):
		super(Armour, self).__init__()
		self.item_type = "Armour"
		self.dfn_bonus = dfn_bonus
		self.stats["dfn"].set_value(self.dfn_bonus)
		self.description_ending = "Defence power: "+str(self.dfn_bonus)+"."
		self.description = "A piece of armour."

class Accessory(Equippable):
	"""docstring for Accessory"""
	def __init__(self, hp_val, mp_val, atk_val, dfn_val, mag_val, res_val, spd_val, luk_val, ele=[], char_class=None):
		super(Accessory, self).__init__()
		self.item_type = "Accessory"

		self.ele = ele
		self.char_class = char_class

		self.stats["hp"].set_value(hp_val)
		self.stats["mp"].set_value(mp_val)
		self.stats["atk"].set_value(atk_val)
		self.stats["dfn"].set_value(dfn_val)
		self.stats["mag"].set_value(mag_val)
		self.stats["res"].set_value(res_val)
		self.stats["spd"].set_value(spd_val)
		self.stats["luk"].set_value(luk_val)
		
		self.description_ending = ""
		for stat in self.stats.values():
			if stat.get_value():
				self.description_ending += "+"+str(stat.get_value())+" "+stat.get_name()

		self.description = "An accessory. "

	def get_accessory_values(self):
		values = ""
		for stat in self.stats.values():
			if stat.get_value():
				values += "+"+str(stat.get_value())+" "+stat.get_name()

		return values
		
class Ingredient(Item):
	"""docstring for Ingredient"""
	def __init__(self):
		super(Ingredient, self).__init__()
		self.item_type = "Ingredient"
		
class Consumable(Item):
	"""docstring for Consumable"""
	def __init__(self):
		super(Consumable, self).__init__()
		self.item_type = "Consumable"
		self.useable = True

class Medicine(Consumable):
	"""docstring for Medicine"""
	def __init__(self, value, stat):
		super(Medicine, self).__init__()
		self.value = value
		self.stat = stat
		self.description_ending = "Restores "+str(self.value)+" "+self.stat.get_name()+"."
		self.description = "A medicine. "+self.description_ending

class GreenHerb(Medicine):
	"""docstring for GreenHerb"""
	def __init__(self):
		self.value = 20
		self.stat = Stat.HitPoints(self.value)
		super(GreenHerb, self).__init__(self.value, self.stat)
		self.name = "Green Herb"
		self.price = 20
		self.description = "A fragrant bright green herb. "+self.description_ending
		self.image = ItemImage.green_herb

	def reload_image(self):
		self.image = ItemImage.green_herb

class BrownHerb(Ingredient):
	"""docstring for BrownHerb"""
	def __init__(self):
		super(BrownHerb, self).__init__()
		self.name = "Brown Herb"
		self.description = "A dried brown herb that stings to the touch."
		self.price = 1000
		self.image = ItemImage.brown_herb

	def reload_image(self):
		self.image = ItemImage.brown_herb

class Healing_Potion_I(Medicine):
	"""docstring for Healing_Potion_I"""
	def __init__(self):
		self.value = 50
		self.stat = Stat.HitPoints(self.value)
		super(Healing_Potion_I, self).__init__(self.value, self.stat)
		self.name = "Healing Potion I"
		self.description = "A concentrated healing essence of low quality. "+self.description_ending
		self.image = ItemImage.healing_potion_I

	def reload_image(self):
		self.image = ItemImage.healing_potion_I

class Mana_Potion_I(Medicine):
	"""docstring for Mana_Potion_I"""
	def __init__(self):
		self.value = 50
		self.stat = Stat.ManaPoints(self.value)
		super(Mana_Potion_I, self).__init__(self.value, self.stat)
		self.name = "Mana Potion I"
		self.description = "A tongue-tickling brew that fills you with magical power. "+self.description_ending
		self.image = ItemImage.mana_potion_I
	
	def reload_image(self):
		self.image = ItemImage.mana_potion_I
		

class RedHerb(Ingredient):
	"""docstring for RedHerb"""
	def __init__(self):
		super(RedHerb, self).__init__()
		self.name = "Red Herb"
		self.description = "A tremendously spicy herb. One sniff makes you burst into tears."
		self.price = 1000
		self.image = ItemImage.red_herb

	def reload_image(self):
		self.image = ItemImage.red_herb

class Dagger(Weapon):
	"""docstring for Dagger"""
	def __init__(self):
		self.atk_bonus = 10
		super(Dagger, self).__init__(self.atk_bonus)
		self.name = "Dagger"
		self.description = "A cheap iron dagger. "+self.description_ending
		self.image = ItemImage.dagger
		self.price = 25

	def reload_image(self):
		self.image = ItemImage.dagger

class CrossRing(Accessory):
	"""docstring for CrossRing"""
	def __init__(self):
		super(CrossRing, self).__init__(0, 0, 60, 100, 0, 0, 0, 0)
		self.name = "Cross Ring"
		self.description = "A grey metal ring, awkwardly shaped like a cross."+self.description_ending
		self.image = ItemImage.cross_ring
		self.price = 8000

	def reload_image(self):
		self.image = ItemImage.cross_ring
		