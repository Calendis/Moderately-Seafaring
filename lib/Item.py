#Classes for items in Moderately Seafaring
from lib import ItemImage

class Item(object):
	"""docstring for Item"""
	def __init__(self):
		super(Item, self).__init__()
		self.name = "Unknown item"
		self.description = "Default item description."
		self.item_type = "Default Item Type"
		self.equippable = False
		self.useable = False
		self.stat = "Stats unaffected. This message should not appear"
		self.value = 0
		self.price = 0
		self.power = 0
		self.w = 0
		self.a = 0
		self.ele = []
		self.image = ItemImage.default

	def get_name(self):
		return self.name

	def get_description(self):
		return self.description

	def get_image(self):
		return self.image

	def clear_image(self):
		self.image = None

class Equippable(Item):
	"""docstring for Equippable"""
	def __init__(self):
		super(Equippable, self).__init__()
		self.item_type = "Equippable"
		self.equippable = True

class Weapon(Equippable):
	"""docstring for Weapon"""
	def __init__(self):
		super(Weapon, self).__init__()
		self.item_type = "Weapon"

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
		self.description_ending = "Restores "+str(self.value)+" "+self.stat
		self.description = "A medicine. "+self.description_ending

class GreenHerb(Medicine):
	"""docstring for GreenHerb"""
	def __init__(self):
		self.value = 20
		self.stat = "HP"
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
		self.stat = "HP"
		super(Healing_Potion_I, self).__init__(self.value, self.stat)
		self.name = "Healing Potion I"
		self.description = "A concentrated healing essence of low quality. "+self.description_ending
		self.image = ItemImage.healing_potion_I

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
		