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
	"""docstring for HitPoints"""
	def __init__(self, value):
		super(HitPoints, self).__init__()
		self.name = "Hit Points"
		self.short_name = "HP"
		self.value = value
		

class ManaPoints(Stat):
	"""docstring for ManaPoints"""
	def __init__(self, value):
		super(ManaPoints, self).__init__()
		self.name = "Mana Points"
		self.short_name = "MP"
		self.value = 0
		

class Attack(Stat):
	"""docstring for Attack"""
	def __init__(self, value):
		super(Attack, self).__init__()
		self.name = "Attack"
		self.short_name = "ATK"
		self.value = value

class Defence(Stat):
		"""docstring for Defence"""
		def __init__(self, value):
			super(Defence, self).__init__()
			self.name = "Defence"
			self.short_name = "DEF"
			self.value = value

class MagicalAttack(Stat):
	"""docstring for MagicalAttack"""
	def __init__(self, value):
		super(MagicalAttack, self).__init__()
		self.name = "Magical Attack"
		self.short_name = "MAG"
		self.value = value

class MagicalResistance(Stat):
	"""docstring for MagicalResistance"""
	def __init__(self, value):
		super(MagicalResistance, self).__init__()
		self.name = "Magical Resistance"
		self.short_name = "RES"
		self.value = value

class Speed(Stat):
	"""docstring for Speed"""
	def __init__(self, value):
		super(Speed, self).__init__()
		self.name = "Speed"
		self.short_name = "SPD"
		self.value = value
		
class Luck(Stat):
	"""docstring for Luck"""
	def __init__(self, value):
		super(Luck, self).__init__()
		self.name = "Luck"
		self.short_name = "LUK"
		self.value = value
		