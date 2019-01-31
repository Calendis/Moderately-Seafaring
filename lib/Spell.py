# Spells and spell lines
# Possible spell targets: 'friendly', 'enemy', 'self'

from lib import SpellImage
from lib import EleImage
from lib import Sound

class Spell():
	"""docstring for Spell"""
	def __init__(self):
		super(Spell, self).__init__()
		self.targeting = "self"
		self.radius = 0
		self.radial_decay = False
		self.name = "Unknown spell"
		self.description = "Default spell description."
		self.mp_cost = 999999
		self.power = 0 #This should still be positive for healing spells!
		self.stat_target = False
		self.stat_power = 0 #This should be positive for buffing spells!

		self.ele = False
		#self.ele_image = self.set_ele_image()

		self.useable_in_field = False
		self.useable_outside_battle = False

		self.image = SpellImage.default
		self.sleep_time = 0.6

	def clear_image(self):
		self.image = None

	def clear_sound(self):
		self.sound = None

	def reload_image(self):
		self.image = SpellImage.default

	def reload_sound(self):
		self.sound = Sound.attack

	def set_ele_image(self):
		if self.ele == "Mercury":
			return EleImage.mercury
		elif self.ele == "Venus":
			return EleImage.venus
		elif self.ele == "Earth":
			return EleImage.earth
		elif self.ele == "Mars":
			return EleImage.mars
		elif self.ele == "Jupiter":
			return EleImage.jupiter
		elif self.ele == "Saturn":
			return EleImage.saturn
		elif self.ele == "Uranus":
			return EleImage.uranus
		elif self.ele == "Neptune":
			return EleImage.neptune
		else:
			return EleImage.none

	def get_name(self):
		return self.name

	def get_description(self):
		return self.description

	def get_image(self):
		return self.image

	def get_power(self):
		return self.power

	def get_stat_power(self):
		return self.stat_power

	def get_stat_target(self):
		return self.stat_target

	def get_mp_cost(self):
		return self.mp_cost

	def get_restore_text(self):
		if self.__class__ == HealingSpell:
			return "Restores around "+self.power+" HP."
		else:
			return None

	def get_useable_in_field(self):
		return self.useable_in_field

	def get_useable_outside_battle(self):
		return self.useable_outside_battle

	def get_targeting(self):
		return self.targeting

	def get_sleep_time(self):
		return self.sleep_time

class HealingSpell(Spell):
	"""docstring for HealingSpell"""
	def __init__(self, power):
		super(HealingSpell, self).__init__()
		self.power = power
		self.description_ending = "Restores somewhere around "+str(self.power)+" HP."
		self.name = "Unknown healing spell"
		self.description = "Default healing spell description."+self.description_ending
		self.useable_outside_battle = True

class DamageSpell(Spell):
	"""docstring for DamageSpell"""
	def __init__(self):
		super(DamageSpell, self).__init__()
		self.targeting = "enemy"
		self.name = "Unknown damaging spell"
		self.description = "Default damaging spell description."
		self.sound = Sound.attack

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
		self.targeting = "friendly"

class NerfSpell(Spell):
	"""docstring for NerfSpell"""
	def __init__(self):
		super(NerfSpell, self).__init__()
		self.targeting = "enemy"
		self.name = "Unknown nerf spell"
		self.description = "Default nerf spell description."
		self.stat_target = True

class StatusSpell(Spell):
	"""docstring for StatusSpell"""
	def __init__(self):
		super(StatusSpell, self).__init__()
		self.status_target = None
		self.inflict = True
		self.name = "Unknown status spell"
		self.description = "Default status spell description."

	def get_inflict(self):
		return self.inflict

	def get_status_target(self):
		return self.status_target
		
		
class Mend(HealingSpell):
	"""docstring for Mend"""
	def __init__(self):
		self.power = 10
		super(Mend, self).__init__(self.power)
		self.name = "Mend"
		self.description = "Weak spell capable of instantly soothing cuts and bruises. "+self.description_ending
		self.mp_cost = 3
		self.targeting = "friendly"
		self.radius = 1
		self.image = SpellImage.mend

	def reload_image(self):
		self.image = SpellImage.mend

class Heal(HealingSpell):
	"""docstring for Heal"""
	def __init__(self):
		self.power = 25
		super(Heal, self).__init__(self.power)
		self.name = "Heal"
		self.description = "Average spell capable of instantly healing up to fractures. "+self.description_ending
		self.mp_cost = 5
		self.targeting = "friendly"
		self.radius = 1
		self.image = SpellImage.heal

	def reload_image(self):
		self.image = SpellImage.heal

class Cure(HealingSpell):
	"""docstring for Cure"""
	def __init__(self):
		self.power = 50
		super(Cure, self).__init__(self.power)
		self.name = "Cure"
		self.description = "Stronger spell capable of quickly healing major lacerations and broken bones"
		self.mp_cost = 9
		self.targeting = "friendly"
		self.radius = 1
		self.image = SpellImage.cure

	def reload_image(self):
		self.image = SpellImage.cure

class Icicle(DamageSpell):
	"""docstring for Icicle"""
	def __init__(self):
		super(Icicle, self).__init__()
		self.name = "Icicle"
		self.description = "Summon a large icicle to strike your foe."
		self.power = 10
		self.mp_cost = 2
		self.ele = "Neptune"
		#self.set_ele_image()
		self.radius = 1
		self.image = SpellImage.icicle
		self.sound = Sound.attack_rocket

	def reload_image(self):
		self.image = SpellImage.icicle

	def reload_sound(self):
		self.sound = Sound.attack_rocket

class IceSpire(DamageSpell):
	"""docstring for IceSpire"""
	def __init__(self):
		super(IceSpire, self).__init__()
		self.name = "Ice Spire"
		self.description = "Summon a massive cone of solid ice to strike your foe."
		self.power = 30
		self.mp_cost = 6
		self.ele = "Neptune"
		#self.set_ele_image()
		self.radius = 1
		self.image = SpellImage.ice_spire

	def reload_image(self):
		self.image = SpellImage.ice_spire
		
class Mire(NerfSpell):
	"""docstring for Mire"""
	def __init__(self):
		super(Mire, self).__init__()
		self.name = "Mire"
		self.description = "Entrap your foes in a sticky bog."
		self.stat_power = 5
		self.mp_cost = 5
		self.stat_target = "spd"
		self.radius = 3
		self.image = SpellImage.mire

	def reload_image(self):
		self.image = SpellImage.mire

class Slime(NerfSpell):
	"""docstring for Slime"""
	def __init__(self):
		super(Slime, self).__init__()
		self.stat_power = 8
		self.mp_cost = 4
		self.name = "Slime"
		self.description = "Trap a foe in tough, gluey, slime."
		self.radius = 1
		self.image = SpellImage.slime
		self.stat_target = "spd"

class Swell(DamageSpell):
	"""docstring for Swell"""
	def __init__(self):
		super(Swell, self).__init__()
		self.name = "Swell"
		self.description = "Summon a wave from beneath to strike your foe."
		self.power = 12
		self.mp_cost = 3
		self.ele = "Neptune"
		self.radius = 1
		self.image = SpellImage.swell

	def reload_image(self):
		self.image = SpellImage.swell

class LargeSwell(DamageSpell):
	"""docstring for LargeSwell"""
	def __init__(self):
		super(LargeSwell, self).__init__()
		self.name = "Large Swell"
		self.description = "Summon a large wave from beneath to strike your foes."
		self.power = 24
		self.mp = 7
		self.ele = "Neptune"
		self.radius = 3
		self.radial_decay = True
		self.image = SpellImage.large_swell

	def reload_image(self):
		self.image = SpellImage.large_swell

class RogueWave(DamageSpell):
	"""docstring for RogueWave"""
	def __init__(self):
		super(RogueWave, self).__init__()
		self.name = "Rogue Wave"
		self.description = "Summon a towering wave to smother your foe!"
		self.power = 75
		self.mp_cost = 14
		self.ele = "Neptune"
		self.radius = 1
		self.radial_decay = True
		self.image = SpellImage.rogue_wave

	def reload_image(self):
		self.image = SpellImage.rogue_wave

class Tsunami(DamageSpell):
	"""docstring for Tsunami"""
	def __init__(self):
		super(Tsunami, self).__init__()
		self.name = "Tsunami"
		self.description = "Summon an encompassing tsunami to drown your foes!!"
		self.power = 150
		self.mp_cost = 55
		self.ele = "Neptune"
		self.radius = 5
		self.radial_decay = True
		self.image = SpellImage.tsunami

	def reload_image(self):
		self.image = SpellImage.tsunami

class Mist(HealingSpell):
	"""docstring for Mist"""
	def __init__(self):
		self.power = 10
		super(Mist, self).__init__(self.power)
		self.name = "Mist"
		self.description = "Summon a soothing mist."+self.description_ending
		self.mp_cost = 6
		self.ele = "Neptune"
		self.radius = 7
		self.image = SpellImage.mist

	def reload_image(self):
		self.image = SpellImage.mist

class Aquablast(DamageSpell):
	"""docstring for Aquablast"""
	def __init__(self):
		super(Aquablast, self).__init__()
		self.name = "AquaBlast"
		self.description = "Blast your foe with a magical jet of water."
		self.power = 8
		self.mp_cost = 2
		self.ele = "Neptune"
		self.radius = 1
		self.image = SpellImage.aquablast
		self.sound = Sound.death_long
		self.sleep_time = 1

	def reload_image(self):
		self.image = SpellImage.aquablast

	def reload_sound(self):
		self.sound = Sound.death_long

class Electrolyze(DamageSpell):
	"""docstring for Electrolyze"""
	def __init__(self):
		super(Electrolyze, self).__init__()
		self.name = "Electrolyze"
		self.description = "Separate a small amount of water into its fundamental components."
		self.power = 10
		self.mp_cost = 4
		self.ele = "Neptune"
		self.radius = 1
		self.image = SpellImage.electrolyze

	def reload_image(self):
		SpellImage.electrolyze

class Drizzle(DamageSpell):
	"""docstring for Drizzle"""
	def __init__(self):
		super(Drizzle, self).__init__()
		self.name = "Drizzle"
		self.description = "Summon a magical rain to strike your foes."
		self.power = 4
		self.mp_cost = 3
		self.ele = "Neptune"
		self.radius = 3
		self.radial_decay = True
		self.image = SpellImage.drizzle

	def reload_image(self):
		self.image = SpellImage.drizzle

class Rainstorm(DamageSpell):
	"""docstring for Rainstorm"""
	def __init__(self):
		super(Rainstorm, self).__init__()
		self.name = "RainStorm"
		self.description = "Summon a heavy magical rain to strike your foes."
		self.power = 13
		self.mp_cost = 5
		self.ele = "Neptune"
		self.radius = 3
		self.radial_decay = True
		self.image = SpellImage.rainstorm

	def reload_image(self):
		self.image = SpellImage.rainstorm

class Hail(DamageSpell):
	"""docstring for Hail"""
	def __init__(self):
		super(Hail, self).__init__()
		self.name = "HailStorm"
		self.description = "Summon a magical hail to strike your foes!"
		self.power = 33
		self.mp_cost = 13
		self.ele = "Neptune"
		self.radius = 3
		self.radial_decay = True
		self.image = SpellImage.hail

	def reload_image(self):
		self.image = SpellImage.hail

class Deluge(DamageSpell):
	"""docstring for Deluge"""
	def __init__(self):
		super(Deluge, self).__init__()
		self.name = "Deluge"
		self.description = "Summon a torrential rain to drench yout foes!"
		self.power = 70
		self.mp_cost = 25
		self.ele = "Neptune"
		self.radius = 3
		self.radial_decay = True
		self.image = SpellImage.deluge

	def reload_image(self):
		self.image = SpellImage.deluge
		
class SuperSleet(DamageSpell):
	"""docstring for SuperSleet"""
	def __init__(self):
		super(SuperSleet, self).__init__()
		self.name = "SuperSleet"
		self.description = "Summon a wet torrential hail to drench your foes!"
		self.power = 100
		self.mp_cost = 40
		self.ele = "Neptune"
		self.radius = 3
		self.image = SpellImage.supersleet

	def reload_image(self):
		self.image = SpellImage.supersleet


class Breeze(DamageSpell):
	"""docstring for Breeze"""
	def __init__(self):
		super(Breeze, self).__init__()
		self.name = "Breeze"
		self.description = "Summon a magical breeze to tear at your foes."
		self.power = 5
		self.mp_cost = 4
		self.ele = "Jupiter"
		self.radius = 3
		self.radial_decay = True
		self.image = SpellImage.breeze

	def reload_image(self):
		self.image = SpellImage.breeze

class Squall(DamageSpell):
	"""docstring for Squall"""
	def __init__(self):
		super(Squall, self).__init__()
		self.name = "Squall"
		self.description = "Summon a magical storm to barrage your foes."
		self.power = 20
		self.mp_cost = 6
		self.ele = "Jupiter"
		self.radius = 5
		self.radial_decay = True
		self.image = SpellImage.squall

	def reload_image(self):
		self.image = SpellImage.squall

class Gale(DamageSpell):
	"""docstring for Gale"""
	def __init__(self):
		super(Gale, self).__init__()
		self.name = "Gale"
		self.description = "Summon an intense magical wind to tear at your foes!"
		self.power = 50
		self.mp_cost = 10
		self.ele = "Jupiter"
		self.radius = 5
		self.radial_decay = True
		self.image = SpellImage.gale

	def reload_image(self):
		self.image = SpellImage.gale

class Cyclone(DamageSpell):
	"""docstring for Cyclone"""
	def __init__(self):
		super(Cyclone, self).__init__()
		self.name = "Cyclone"
		self.power = 100
		self.mp_cost = 30
		self.ele = "Jupiter"
		self.radius = 7
		self.radial_decay = True
		self.image = SpellImage.cyclone

	def reload_image(self):
		self.image = SpellImage.cyclone

class Waterspout(DamageSpell):
	"""docstring for Waterspout"""
	def __init__(self):
		super(Waterspout, self).__init__()
		self.name = "Waterspout"
		self.description = "Call forth a towering pillar of water from beneath!!"
		self.power = 175
		self.mp_cost = 75
		self.ele = "Neptune"
		self.radius = 1
		self.image = SpellImage.waterspout

	def reload_image(self):
		self.image = SpellImage.waterspout

class Swab(BuffSpell):
	"""docstring for Swab"""
	def __init__(self):
		self.stat_power = 6
		super(Swab, self).__init__(self.stat_power)
		self.name = "Swab"
		self.description = "Swab the decks! Speed up an ally."
		self.stat_target = "spd"
		self.mp_cost = 3
		self.radius = 1
		self.image = SpellImage.swab

	def reload_image(self):
		self.image = SpellImage.swab

class Batten(BuffSpell):
	"""docstring for Batten"""
	def __init__(self):
		self.stat_power = 30
		super(Batten, self).__init__(self.stat_power)
		self.name = "Batten"
		self.description = "Batten down the hatches! Boost an ally's defence."
		self.stat_target = "dfn"
		self.mp_cost = 5
		self.radius = 1
		self.image = SpellImage.batten

	def reload_image(self):
		self.image = SpellImage.batten


class Bestow(BuffSpell):
	"""docstring for Bestow"""
	def __init__(self):
		self.stat_power = 10
		super(Bestow, self).__init__(self.stat_power)
		self.name = "Bestow"
		self.description = "Grant an ally immense strength."
		self.stat_target = "atk"
		self.targeting = "friendly"
		self.mp_cost = 20
		self.radius = 1
		self.image = SpellImage.bestow

	def reload_image(self):
		self.image = SpellImage.bestow

class Swig(BuffSpell):
	"""docstring for Swig"""
	def __init__(self):
		self.stat_power = 50
		super(Swig, self).__init__(self.stat_power)
		self.name = "Swig"
		self.description = "Down a bottle of magical rum."
		self.stat_target = "atk"
		self.mp_cost = 15
		self.radius = 1
		self.targeting = "self"
		self.image = SpellImage.swig

	def reload_image(self):
		self.image = SpellImage.swig

class Lime(StatusSpell):
	"""docstring for Lime"""
	def __init__(self):
		super(Lime, self).__init__()
		self.name = "Lime"
		self.description = "Administer a magical lime to purge disease and poison."
		self.status_target = "poison"
		self.inflict = False
		self.mp_cost = 3
		self.radius = 1
		self.targeting = "friendly"
		self.image = SpellImage.lime

	def reload_image(self):
		self.image = SpellImage.lime

class Revive(StatusSpell):
	"""docstring for Revive"""
	def __init__(self):
		super(Revive, self).__init__()
		self.name = "Revive"
		self.description = "Raise an ally."
		self.status_target = "down"
		self.inflict = False
		self.mp_cost = 20
		self.radius = 1
		self.targeting = "friendly"
		self.image = SpellImage.revive
		self.useable_outside_battle = True

	def reload_image(self):
		self.image = SpellImage.revive
		
basic_healer_line = {1: Mend(), 5: Heal(), 10: Cure(), 30: Revive()}
test_line = {1: Mire(), 2: Icicle(), 3: IceSpire(), 4: Bestow(), 5: Revive()}
neptune_line = {2: Aquablast(), 3: Drizzle(), 3: Mist(), 5: Swell(), 9: Rainstorm(), 14: LargeSwell(), 20: Hail(), 30: RogueWave(), 33: Deluge(), 42: Tsunami(), 58: SuperSleet()}
wrath_o_the_sea_line = {1: Swab(), 3: Swell(), 6: Lime(), 11: Squall(), 15: Batten(), 21: Swig(), 60: Waterspout()}
weak_slime_line = {15: Heal(), 15: Mist(), 17: Aquablast()}
weak_flying_line = {20: Breeze()}
servant_line = {1: Mend(), 2: Heal(), 4: Cure(), 10: Breeze()}