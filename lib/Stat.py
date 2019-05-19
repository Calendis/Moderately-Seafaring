#Classes for stats

class Stat(object):
	"""docstring for Stat"""
	def __init__(self):
		super(Stat, self).__init__()
		self.name = "Default stat"
		self.short_name = "STAT"
		self.value = 0
		self.temp_modifier = 0

	def get_name(self, short=True):
		if short:
			return self.short_name
		return self.name

	def get_value(self):
		return self.value

	def shift_value(self, offset):
		self.value += offset

	def set_value(self, new_value):
		self.value = new_value

class HitPoints(Stat):
	"""When these reach zero, you're done."""
	def __init__(self, value):
		super(HitPoints, self).__init__()
		self.name = "Hit Points"
		self.short_name = "HP"
		self.value = value
		

class ManaPoints(Stat):
	"""Costs these to use magic."""
	def __init__(self, value):
		super(ManaPoints, self).__init__()
		self.name = "Mana Points"
		self.short_name = "MP"
		self.value = 0
		

class Attack(Stat):
	"""Determines how much non-magical damage you can inflict."""
	def __init__(self, value):
		super(Attack, self).__init__()
		self.name = "Attack"
		self.short_name = "ATK"
		self.value = value

class Defence(Stat):
		"""Reduces non-magical damage dealt to you."""
		def __init__(self, value):
			super(Defence, self).__init__()
			self.name = "Defence"
			self.short_name = "DEF"
			self.value = value

class MagicalAttack(Stat):
	"""Determines how much magical damage you can inflict."""
	def __init__(self, value):
		super(MagicalAttack, self).__init__()
		self.name = "Magical Attack"
		self.short_name = "MAG"
		self.value = value

class MagicalResistance(Stat):
	"""Reduces magical damage done to you."""
	def __init__(self, value):
		super(MagicalResistance, self).__init__()
		self.name = "Magical Resistance"
		self.short_name = "RES"
		self.value = value

class Speed(Stat):
	"""Determines who goes first and how easy it is to escape."""
	def __init__(self, value):
		super(Speed, self).__init__()
		self.name = "Speed"
		self.short_name = "SPD"
		self.value = value
		
class Luck(Stat):
	"""Determines crit rate, and acts as attack/defence against status effects."""
	def __init__(self, value):
		super(Luck, self).__init__()
		self.name = "Luck"
		self.short_name = "LUK"
		self.value = value
		