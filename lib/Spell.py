#Spells and spell lines

#Possible spell targets: 'friendly', 'enemy', 'self'

class Spell():
	"""docstring for Spell"""
	def __init__(self):
		super(Spell, self).__init__()
		self.targeting = "self"
		self.radius = 0
		self.name = "Unknown spell"
		self.description = "Default spell description."
		self.mp_cost = 999999
		self.power = 0 #This should be negative for healing spells!
		self.stat_target = False
		self.stat_power = 0 #This should be positive for buffing spells!

		self.ele = False

class HealingSpell(Spell):
	"""docstring for HealingSpell"""
	def __init__(self, power):
		super(HealingSpell, self).__init__()
		if power > 0:
			raise ValueError("Healing spells may not have positive power!")
		self.description_ending = "Restores somewhere around "+str(self.power)+" HP."
		self.power = power
		self.name = "Unknown healing spell"
		self.description = "Default healing spell description."+self.description_ending

class DamageSpell(Spell):
	"""docstring for DamageSpell"""
	def __init__(self):
		super(DamageSpell, self).__init__()
		self.targeting = "enemy"
		self.name = "Unknown damaging spell"
		self.description = "Default damaging spell description."

class BuffSpell(Spell):
	"""docstring for BuffSpell"""
	def __init__(self, stat_power):
		super(BuffSpell, self).__init__()
		if stat_power < 0:
			raise ValueError("Buff spells may not have negative stat power!")
		self.stat_power = stat_power
		self.name = "Unknown buff spell"
		self.description = "Default buff spell description."
		self.stat_target = True

class NerfSpell(Spell):
			"""docstring for NerfSpell"""
			def __init__(self):
				super(NerfSpell, self).__init__()
				self.targeting = "enemy"
				self.name = "Unknown nerf spell"
				self.description = "Default nerf spell description"
				self.stat_target = True
						
		
class Mend(HealingSpell):
	"""docstring for Mend"""
	def __init__(self):
		self.power = -10
		super(Mend, self).__init__(self.power)
		self.name = "Mend"
		self.description = "Weak spell capable of instantly soothing cuts and bruises. "+self.description_ending
		self.mp_cost = 3
		self.targeting = "friendly"
		self.radius = 1

class Heal(HealingSpell):
	"""docstring for Heal"""
	def __init__(self):
		self.power = -25
		super(Heal, self).__init__(self.power)
		self.name = "Heal"
		self.description = "Average spell capable of instantly healing up to fractures. "+self.description_ending
		self.mp_cost = 5
		self.targeting = "friendly"
		self.radius = 1

class Cure(HealingSpell):
	"""docstring for Cure"""
	def __init__(self):
		self.power = -50
		super(Cure, self).__init__(self.power)
		self.name = "Cure"
		self.description = "Stronger spell capable of quickly healing major lacerations and broken bones"
		self.mp_cost = 9
		self.targeting = "friendly"
		self.radius = 1
		

class Icicle(DamageSpell):
	"""docstring for Icicle"""
	def __init__(self):
		super(Icicle, self).__init__()
		self.name = "Icicle"
		self.description = "Summon a large icicle to strike your foe."
		self.power = 10
		self.mp_cost = 2
		self.ele = "Neptune"
		self.radius = 1

class IceSpire(DamageSpell):
	"""docstring for IceSpire"""
	def __init__(self):
		super(IceSpire, self).__init__()
		self.name = "Ice Spire"
		self.description = "Summon a massive cone of solid ice to strike your foe."
		self.power = 30
		self.mp_cost = 6
		self.ele = "Neptune"
		self.radius = 1
		

class Mire(NerfSpell):
	"""docstring for Mire"""
	def __init__(self):
		super(Mire, self).__init__()
		self.stat_power = 5
		self.mp_cost = 5
		self.stat_target = "Speed"
		self.radius = 3
		
		
						
basic_healer_line = [Mend(), Heal(), Cure()]
test_line = [Mire(), Icicle(), IceSpire()]