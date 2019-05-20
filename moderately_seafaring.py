# The gameloop for Moderately Seafaring, an RPG
# 4 Dec, 2016
# Code refactor to OOP 31 Jan, 2019

import pygame
from pygame.locals import *

from pytmx.util_pygame import load_pygame

import pyscroll
import pyscroll.data
from pyscroll.group import PyscrollGroup

import shelve
import time

import os.path
import sys

from random import randint

from math import floor
from math import sin

from lib import Character
from lib import Menu
from lib import Text
from lib import Item
from lib import Party
from lib import Spell
from lib import Stat
from lib import Battle
from lib import Sound
from lib import UIConstant
from lib import BackgroundImage
from lib import Selector
from lib import EnemyPool
from lib import NPCID
from lib import Trait

class ModeratelySeafaringGame():
	""" Base class containing the entire game. """
	def __init__(self):
		super(ModeratelySeafaringGame, self).__init__()

		self.screen_size = (900, 700)
		self.screen = pygame.display.set_mode(self.screen_size)
		self.clock = pygame.time.Clock()

		self.done = False
		self.paused = False
		self.title_screen = True
		self.accepting_input = True # Disabled during animations
		self.main_screen = False
		self.battle_screen = False
		
		self.battle_actions = []
		self.battle_over = True
		self.current_battle_member_index = 0
		self.experience_pool = 0

		self.party_text_colour = UIConstant.PARTY_TEXT_COLOUR
		self.hp_text_colour = UIConstant.HP_TEXT_COLOUR

		self.BASE_BACKGROUND_COLOUR = (74, 104, 200)
		
		self.menus = []
		
		self.selectors = [
			Selector.SelectorTopLeft(0, 0),
			Selector.SelectorTopRight(0, 0),
			Selector.SelectorBottomLeft(0, 0),
			Selector.SelectorBottomRight(0, 0)
		]

		'''global enemy_selectors
		enemy_selectors = [
			Selector.SelectorTopLeft(0, 0),
			Selector.SelectorTopRight(0, 0),
			Selector.SelectorBottomLeft(0, 0),
			Selector.SelectorBottomRight(0, 0)
		]'''

		self.party = Party.Party()
		self.enemy_party = Party.Party()
		
		self.npcs = []

		self.current_colliding_object = None
		self.colliding = False
		
		self.fragile_textboxes = []
		self.resiliant_textboxes = []
		self.floating_texts = []

		self.main_menu = Menu.MainMenu()
		self.menus.append(self.main_menu)

		self.current_map = load_pygame("resources/maps/test_map.tmx")

		self.party.add_member(Character.CaptainRizzko([415, 487], 1))
		self.party.add_member(Character.Zirkak([0,0], 50)) #Level 50 for testing purposes
		#self.party.add_member(Character.GenericPirate([0, 0], 1))

		self.pyscroll_map_data = pyscroll.data.TiledMapData(self.current_map)
		self.map_layer = pyscroll.BufferedRenderer(self.pyscroll_map_data, self.screen.get_size())
		self.map_layer.zoom = 2
		self.pyscroll_group_data = PyscrollGroup(map_layer=self.map_layer, default_layer=self.party.get_current_member().get_layer())
		self.pyscroll_group_data.add(self.party.get_current_member())
		self.pyscroll_group_data.change_layer(self.party.get_current_member(), self.party.get_current_member().get_layer())

		self.logo = pygame.image.load("resources/img/logo.png")

	def begin_game(self):
		while not self.done: # Master gameloop that can contain other gameloops.
			while not self.done and self.title_screen: # Gameloop that runs while on the title screen of the game
				title_screen_events = pygame.event.get()

				for title_screen_event in title_screen_events:
					# Title screen event handling
					if title_screen_event.type == pygame.QUIT:
						self.done = True

					if title_screen_event.type == pygame.KEYDOWN:
						if title_screen_event.key == K_UP:
							self.menus[-1].move_selection_up()
						if title_screen_event.key == K_DOWN:
							self.menus[-1].move_selection_down()
						if title_screen_event.key == K_LEFT:
							self.menus[-1].move_selection_left()
						if  title_screen_event.key == K_RIGHT:
							self.menus[-1].move_selection_right()
						if title_screen_event.key == K_RETURN or title_screen_event.key == K_x:
							Sound.confirm.play()
							if self.menus[-1].__class__ == Menu.MainMenu:							
								if self.menus[-1].get_selected_name() == "New Game":
									self.menus = []

									self.walls = []
									self.warps = []
									self.layer_switches = []

									for map_object in self.current_map.objects:
										if map_object.type == "wall":
											self.walls.append(map_object)	
										elif map_object.type == "warp":
											self.warps.append(map_object)
										elif map_object.type == "layer_switch":
											self.layer_switches.append(map_object)

									self.title_screen = False
									self.main_screen = True
									Sound.play_overworld_music("sea")

								elif self.menus[-1].get_selected_name() == "Load Game":
									self.menus.append(Menu.LoadMenu())
								elif self.menus[-1].get_selected_name() == "Settings":
									print("TODO: Settings")
								elif self.menus[-1].get_selected_name() == "Quit":
									self.done = True
							elif self.menus[-1].__class__ == Menu.LoadMenu:
								if self.menus[-1].get_selected_element_position()["x"] == 0:
									gamefile = "0"
								elif self.menus[-1].get_selected_element_position()["x"] == 1:
									gamefile = "1"
								elif self.menus[-1].get_selected_element_position()["x"] == 2:
									gamefile = "2"
								
								self.load(gamefile)

						if title_screen_event.key == K_z:
							if len(self.menus) > 1:
								Sound.back.play()
								self.menus.remove(self.menus[-1])
								if len(self.menus) > 0:
									self.menus[-1].update()

				#Game logic below

				for menu in self.menus:
					menu.update()

				#Drawing Below
				self.screen.fill(self.BASE_BACKGROUND_COLOUR)

				self.screen.blit(self.logo, (self.screen_size[0]/2-self.logo.get_width()/2, 0))

				for menu in self.menus:
					menu.draw(self.screen)

				pygame.display.flip()
				self.clock.tick(60)

			################################################################################################
			################################################################################################

			while self.main_screen and not self.done and not self.paused and not self.title_screen: # Main gameloop
				if self.accepting_input:
					main_screen_events = pygame.event.get()

				for event in main_screen_events:
					#Event Handling
					if event.type == pygame.QUIT:
						self.done = True
					if event.type == pygame.KEYDOWN:
						if len(self.menus) < 1 and len(self.fragile_textboxes) < 1:
							if event.key == K_q:
								self.map_layer.zoom = 1.2
							if event.key == K_UP:
								for party_member in self.party.get_members():
									party_member.velocity[1] = -1
							if event.key == K_DOWN:
								for party_member in self.party.get_members():
									party_member.velocity[1] = 1
							if event.key == K_LEFT:
								for party_member in self.party.get_members():
									party_member.velocity[0] = -1
									party_member.frame = 0
							if event.key == K_RIGHT:
								for party_member in self.party.get_members():
									party_member.velocity[0] = 1
									party_member.frame = 1

							if event.key == K_RETURN:
								if Menu.StartMenu() not in self.menus:
									self.menus.append(Menu.StartMenu())
									for party_member in self.party.get_members():
										party_member.velocity = [0, 0]
							if event.key == K_i:
								self.initate_battle()

							if event.key == K_x:
								# Confirm button in the overworld
								# Used for NPC interactions, etc.
								if self.current_colliding_object != None:
									if self.current_colliding_object.__class__.__bases__[0] == Character.Character:
										
										self.fragile_textboxes.append(
											Text.DialogueBox([self.current_colliding_object.get_lines()[self.current_colliding_object.get_current_line()][0]],
											self.screen_size[0]/2,
											self.screen_size[1]-UIConstant.DIALOGUE_HEIGHT-UIConstant.MENU_BORDER_WIDTH-16,
											self.current_colliding_object.get_line_delays()))

										self.fragile_textboxes[-1].centre_x()
										self.current_colliding_object.advance_lines()
								
									if self.current_colliding_object.get_lines()[self.current_colliding_object.get_current_line()][3] != None:
										# A gift item is associated with this dialogue
										print(self.current_colliding_object.get_lines()[self.current_colliding_object.get_current_line()][3])
										self.party.get_current_member().give_item(self.current_colliding_object.get_lines()[self.current_colliding_object.get_current_line()][3]())
										
										self.fragile_textboxes.append(Text.TextBox("You got a "+self.current_colliding_object.get_lines()[self.current_colliding_object.get_current_line()][3]().get_name()+"!",
											self.screen_size[0]/2,
											self.screen_size[1]/2))
										
										self.fragile_textboxes[-1].centre_x()
						else:
							
							try:
								self.fragile_textboxes.remove(self.fragile_textboxes[-1]) #Remove a textbox if it exists, and do not interact with the menu system
								break
							except:
								pass

							if event.key == K_UP:
								self.menus[-1].move_selection_up()
								Sound.menu.play()
							if event.key == K_DOWN:
								self.menus[-1].move_selection_down()
								Sound.menu.play()
							if event.key == K_LEFT:
								self.menus[-1].move_selection_left()
								Sound.menu.play()
							if  event.key == K_RIGHT:
								self.menus[-1].move_selection_right()
								Sound.menu.play()
							if event.key == K_z:
								Sound.back.play()
								self.menus.remove(self.menus[-1])
								if len(self.menus) > 0:
									self.menus[-1].update()
								if len(self.resiliant_textboxes) > 0:
									self.resiliant_textboxes.remove(resiliant_textboxes[-1])

							if event.key == K_x:
								Sound.confirm.play()
								if self.menus[-1].__class__ == Menu.StartMenu:
									if self.menus[-1].get_selected_name() == "Party":
										self.menus.append(Menu.PartyMenu(self.party))
									elif self.menus[-1].get_selected_name() == "Items":
										if len(self.party.get_current_member().get_items()) > 0:
											self.menus.append(Menu.ItemMenu(self.party.get_current_member().get_items()))
										else:
											self.fragile_textboxes.append(Text.TextBox(["You have no items!"], self.screen_size[0]/2, self.screen_size[1]/2))
											self.fragile_textboxes[-1].centre_x()
									elif self.menus[-1].get_selected_name() == "Save":
										self.menus.append(Menu.SaveMenu())
									elif self.menus[-1].get_selected_name() == "Pause":
										self.paused = True
									elif self.menus[-1].get_selected_name() == "Spells":
										if len(self.party.get_current_member().get_spells()) > 0:
											self.menus.append(Menu.SpellMenu(self.party.get_current_member().get_spells()))
										else: # Don't open the spell menu if the selected character has no spells.
											self.fragile_textboxes.append(Text.TextBox(["You have no spells!"], self.screen_size[0]/2, self.screen_size[1]/2))
											self.fragile_textboxes[-1].centre_x()

									elif self.menus[-1].get_selected_name() == "Quit":
										self.done = True
									elif self.menus[-1].get_selected_name() == "Traits":
										self.menus.append(Menu.TraitWhatMenu())
									else:
										print("No item was selected. ERROR 00-0")
										self.fragile_textboxes.append(Text.TextBox(["ERROR 00-0", "No item was selected."], 100, 100))

								elif self.menus[-1].__class__ == Menu.SaveMenu:
									if self.menus[-1].get_selected_element_position()["x"] == 0: #Notice the x position is needed on a vertical list. This is because it represents the ROW
										gamefile = "0"
									elif menus[-1].get_selected_element_position()["x"] == 1:
										gamefile = "1"
									elif menus[-1].get_selected_element_position()["x"] == 2:
										gamefile = "2"
									else:
										print("Unknown option. Gamefile will not be set. Aborting")
										pygame.quit()
										exit()
										
									self.save(gamefile)

								elif self.menus[-1].__class__ == Menu.ItemMenu:
									# Opens the item use menu for the item you've selected
									self.menus.append(Menu.ItemUseMenu(self.party.get_current_member().get_items()[self.menus[-1].get_selected_element_position()["x"]]))

								elif self.menus[-1].__class__ == Menu.SpellMenu:
									# Opens the spell use menu for the spell you've selected
									self.menus.append(Menu.SpellUseMenu(self.party.get_current_member().get_spells()[self.menus[-1].get_selected_element_position()["x"]]))

								elif self.menus[-1].__class__ == Menu.ItemUseMenu:
									if self.menus[-1].get_selected_name() == "Use":
										if self.party.get_current_member().get_items()[self.menus[1].get_selected_element_position()["x"]].get_useable():
											# Adds the "use on whom?" menu to the menu list.
											self.menus.append(Menu.WhomUseMenu(self.menus[-1].get_item(), self.party))
										else:
											self.fragile_textboxes.append(Text.TextBox([self.party.get_current_member().get_items()[self.menus[1].get_selected_element_position()["x"]].get_name()+" isn't useable!"],
												self.menus[-1].get_position()["x"]+self.menus[-1].get_box_width()+UIConstant.MENU_SPACING+2*UIConstant.MENU_BORDER_WIDTH, self.menus[-1].get_position()["y"]))

									elif self.menus[-1].get_selected_name() == "Examine":
										self.fragile_textboxes.append(Text.TextBox([self.party.get_current_member().get_items()[self.menus[1].get_selected_element_position()["x"]].get_description(),
											"","Type: "+self.party.get_current_member().get_items()[self.menus[1].get_selected_element_position()["x"]].get_item_type()],
										 self.menus[-1].get_position()["x"]+self.menus[-1].get_box_width()+UIConstant.MENU_SPACING+2*UIConstant.MENU_BORDER_WIDTH, self.menus[-1].get_position()["y"]))
									
									elif self.menus[-1].get_selected_name() == "Equip": #Equip
										if self.party.get_current_member().get_items()[self.menus[1].get_selected_element_position()["x"]].get_equippable():
											self.menus.append(Menu.WhomEquipMenu(self.menus[-1].get_item(), self.party))
										else:
											self.fragile_textboxes.append(Text.TextBox([self.party.get_current_member().get_items()[self.menus[1].get_selected_element_position()["x"]].get_name()+" isn't equippable!"],
												self.menus[-1].get_position()["x"]+self.menus[-1].get_box_width()+UIConstant.MENU_SPACING+2*UIConstant.MENU_BORDER_WIDTH, self.menus[-1].get_position()["y"]))

									elif self.menus[-1].get_selected_name() == "Discard":
										self.party.get_current_member().get_items().remove(self.menus[-1].get_item())
										if len(self.party.get_current_member().get_items()) > 0:
											self.menus[1] = Menu.ItemMenu(self.party.get_current_member().get_items())
											self.menus.remove(self.menus[-1])
										else:
											self.menus.remove(self.menus[-1])
											self.menus.remove(self.menus[-1])

									elif self.menus[-1].get_selected_name() == "Give":
										self.menus.append(Menu.WhomGiveMenu(self.menus[-1].get_item(), self.party))

								elif self.menus[-1].__class__ == Menu.SpellUseMenu:
									if self.menus[-1].get_selected_name() == "Use":
										selected_spell = self.party.get_current_member().get_spells()[self.menus[1].get_selected_element_position()["x"]]
										if selected_spell.get_useable_outside_battle():
											self.menus.append(Menu.WhomSpellMenu(selected_spell, self.party))
										elif self.party.get_current_member().get_spells()[self.menus[1].get_selected_element_position()["x"]].get_useable_in_field():
											print("TODO: Use spells in field.")
										else:
											self.fragile_textboxes.append(Text.TextBox([self.menus[-1].get_spell().get_name()+" isn't useable in the field."],
												self.menus[-1].get_position()["x"]+self.menus[-1].get_box_width()+UIConstant.MENU_SPACING+2*UIConstant.MENU_BORDER_WIDTH, self.menus[-1].get_position()["y"]))
									elif self.menus[-1].get_selected_name() == "Description":
										self.fragile_textboxes.append(Text.TextBox([self.party.get_current_member().get_spells()[self.menus[1].get_selected_element_position()["x"]].get_description(),
											"", self.menus[-1].get_spell().get_restore_text()],
											self.menus[-1].get_position()["x"]+self.menus[-1].get_box_width()+UIConstant.MENU_SPACING+2*UIConstant.MENU_BORDER_WIDTH, self.menus[-1].get_position()["y"]))


								elif self.menus[-1].__class__ == Menu.PartyMenu:
									# Opens the party use menu for the party member you've selected
									self.menus.append(Menu.PartyUseMenu(self.party[self.menus[-1].get_selected_element_position()["x"]]))

								elif self.menus[-1].__class__ == Menu.PartyUseMenu:
									if self.menus[-1].get_selected_name() == "Status":
										selected_party_member = self.party[self.menus[1].get_selected_element_position()["x"]]
										self.fragile_textboxes.append(Text.TextBox(
											
											[selected_party_member.get_full_name(),
											"HP: "+str(selected_party_member.get_current_hp())+"/"+str(selected_party_member.get_hp()),
											"MP: "+str(selected_party_member.get_current_mp())+"/"+str(selected_party_member.get_mp()),
											"ATK: "+str(selected_party_member.get_atk()),
											"DEF: "+str(selected_party_member.get_dfn()),
											"MAG: "+str(selected_party_member.get_mag()),
											"RES: "+str(selected_party_member.get_res()),
											"SPD: "+str(selected_party_member.get_spd()),
											"LUCK: "+str(selected_party_member.get_luk()),
											"Weapon: "+selected_party_member.get_weapon_name()+" (+"+str(selected_party_member.get_weapon_power())+")",
											"Armour: "+selected_party_member.get_armour_name()+" (+"+str(selected_party_member.get_armour_power())+")",
											"Shield: "+selected_party_member.get_shield_name()+" (+"+str(selected_party_member.get_shield_power())+")",
											"Accessory: "+selected_party_member.get_accessory_name()+" (+"+str(selected_party_member.get_accessory_power())+")",
											"EXP: "+str(selected_party_member.get_exp())+"/"+str(selected_party_member.get_exp_to_next()),
											"TP: "+str(selected_party_member.get_tp())],

											self.menus[-1].get_position()["x"]+self.menus[-1].get_box_width()+UIConstant.MENU_SPACING+2*UIConstant.MENU_BORDER_WIDTH, self.menus[-1].get_position()["y"]))

									elif self.menus[-1].get_selected_name() == "Select":
										self.pyscroll_group_data.remove(self.party.get_current_member())
										
										self.party.set_stored_pos(self.party.get_current_member().get_pos())
										self.party.set_stored_layer(self.party.get_current_member().get_layer())

										self.party.set_current_member(self.party[self.menus[1].get_selected_element_position()["x"]])
										
										self.party.get_current_member().set_pos(self.party.get_stored_pos())
										self.party.get_current_member().set_layer(self.party.get_stored_layer())
										
										self.pyscroll_group_data.add(self.party.get_current_member())
										self.pyscroll_group_data.change_layer(self.party.get_current_member(), self.party.get_current_member().get_layer())

									elif self.menus[-1].get_selected_name() == "Unequip":
										equipped_items = []
										if self.party[self.menus[1].get_selected_element_position()["x"]].get_weapon():
											equipped_items.append(self.party[self.menus[1].get_selected_element_position()["x"]].get_weapon())
										if self.party[self.menus[1].get_selected_element_position()["x"]].get_armour():
											equipped_items.append(self.party[self.menus[1].get_selected_element_position()["x"]].get_armour())
										if self.party[self.menus[1].get_selected_element_position()["x"]].get_shield():
											equipped_items.append(self.party[self.menus[1].get_selected_element_position()["x"]].get_shield())
										if self.party[self.menus[1].get_selected_element_position()["x"]].get_accessory():
											equipped_items.append(self.party[self.menus[1].get_selected_element_position()["x"]].get_accessory())
										
										if len(equipped_items) > 0:
											self.menus.append(Menu.UnequipMenu(equipped_items))
										else:
											self.fragile_textboxes.append(Text.TextBox([self.party[self.menus[1].get_selected_element_position()["x"]].get_name()+" has nothing equipped."],
												self.menus[-1].get_position()["x"]+self.menus[-1].get_box_width()+UIConstant.MENU_SPACING+2*UIConstant.MENU_BORDER_WIDTH, self.menus[-1].get_position()["y"]))

								elif self.menus[-1].__class__ == Menu.WhomUseMenu:
									if self.menus[-1].get_item().__class__.__bases__[0] == Item.Medicine:
										self.party[self.menus[-1].get_selected_element_position()["x"]].heal(self.menus[-1].get_item().get_value(), self.menus[-1].get_item().get_stat())
										self.party.get_current_member().get_items().remove(self.menus[-1].get_item())
										if len(self.party.get_current_member().get_items()) > 0:
											self.menus[1] = Menu.ItemMenu(self.party.get_current_member().get_items())
										else:
											self.menus.remove(self.menus[-1])
										self.menus.remove(self.menus[-1])
										self.menus.remove(self.menus[-1])

								elif self.menus[-1].__class__ == Menu.WhomSpellMenu:
									if self.party.get_current_member().get_current_mp() < self.menus[-1].get_spell().get_mp_cost():
										self.fragile_textboxes.append(Text.TextBox(["Not enough MP!"],
											self.menus[-1].get_position()["x"]+self.menus[-1].get_box_width()+UIConstant.MENU_SPACING+2*UIConstant.MENU_BORDER_WIDTH, self.menus[-1].get_position()["y"]))
									else:
										self.party.get_current_member().shift_current_mp(-(self.menus[-1].get_spell().get_mp_cost()))
										
										if self.menus[-1].get_spell().__class__.__bases__[0] == Spell.HealingSpell:
											if "down" not in self.party.get_members()[self.menus[-1].get_selected_element_position()["x"]].get_statuses() and self.party.get_members()[self.menus[-1].get_selected_element_position()["x"]].get_current_hp() != self.party.get_members()[self.menus[-1].get_selected_element_position()["x"]].get_hp():
												self.party.get_members()[self.menus[-1].get_selected_element_position()["x"]].heal((self.menus[-1].get_spell().get_power()), Stat.HitPoints(-(self.menus[-1].get_spell().get_power())))
											else:
												self.fragile_textboxes.append(Text.TextBox(["It will have no effect"], self.menus[-1].get_box_width()+UIConstant.MENU_SPACING+2*UIConstant.MENU_BORDER_WIDTH+self.menus[-1].get_position()["x"], self.menus[-1].get_position()["y"]))
												party.get_current_member().shift_current_mp(self.menus[-1].get_spell().get_mp_cost()) # Shift the MP back

										elif self.menus[-1].get_spell().__class__.__bases__[0] == Spell.StatusSpell:
											if self.menus[-1].get_spell().get_inflict():
												print("TODO: Handle field inflict case.")
											else:
												if self.menus[-1].get_spell().get_status_target() in self.party.get_members()[self.menus[-1].get_selected_element_position()["x"]].get_statuses():
													self.party.get_members()[self.menus[-1].get_selected_element_position()["x"]].cure_status(self.menus[-1].get_spell().get_status_target())

												if self.menus[-1].get_spell().get_status_target() == "down":
													self.party.get_members()[self.menus[-1].get_selected_element_position()["x"]].heal(1, Stat.HitPoints(0))

								elif self.menus[-1].__class__ == Menu.WhomEquipMenu:
									if self.party[self.menus[-1].get_selected_element_position()["x"]].get_weapon() and self.menus[-1].get_item().get_item_type() == "Weapon":
										self.fragile_textboxes.append(Text.TextBox([self.party[self.menus[-1].get_selected_element_position()["x"]].get_name()+" already has a weapon equipped."],
											self.menus[-1].get_box_width()+UIConstant.MENU_SPACING+2*UIConstant.MENU_BORDER_WIDTH+self.menus[-1].get_position()["x"], self.menus[-1].get_position()["y"]))
									
									elif self.party[self.menus[-1].get_selected_element_position()["x"]].get_armour() and self.menus[-1].get_item().get_item_type() == "Armour":
										self.fragile_textboxes.append(Text.TextBox([self.party[self.menus[-1].get_selected_element_position()["x"]].get_name()+" already has armour equipped."],
											self.menus[-1].get_box_width()+UIConstant.MENU_SPACING+2*UIConstant.MENU_BORDER_WIDTH+self.menus[-1].get_position()["x"], self.menus[-1].get_position()["y"]))
									
									elif self.party[self.menus[-1].get_selected_element_position()["x"]].get_shield() and self.menus[-1].get_item().get_item_type() == "Shield":
										self.fragile_textboxes.append(Text.TextBox([self.party[self.menus[-1].get_selected_element_position()["x"]].get_name()+" already has a shield equipped."],
											self.menus[-1].get_box_width()+UIConstant.MENU_SPACING+2*UIConstant.MENU_BORDER_WIDTH+self.menus[-1].get_position()["x"], self.menus[-1].get_position()["y"]))
									
									elif self.party[self.menus[-1].get_selected_element_position()["x"]].get_accessory() and self.menus[-1].get_item().get_item_type() == "Accessory":
										self.fragile_textboxes.append(Text.TextBox([self.party[self.menus[-1].get_selected_element_position()["x"]].get_name()+" already has an accessory equipped."],
											self.menus[-1].get_box_width()+UIConstant.MENU_SPACING+2*UIConstant.MENU_BORDER_WIDTH+self.menus[-1].get_position()["x"], self.menus[-1].get_position()["y"]))
									
									else:
										self.party[self.menus[-1].get_selected_element_position()["x"]].equip(self.menus[-1].get_item())
										self.party.get_current_member().get_items().remove(self.menus[-1].get_item())
										
										if len(self.party.get_current_member().get_items()) > 0:
											self.menus[1] = Menu.ItemMenu(self.party.get_current_member().get_items())
											self.menus.remove(self.menus[-1])
											self.menus.remove(self.menus[-1])
										else:
											self.menus.remove(self.menus[-1])
											self.menus.remove(self.menus[-1])
											self.menus.remove(self.menus[-1])

								elif self.menus[-1].__class__ == Menu.UnequipMenu:
									self.party[self.menus[1].get_selected_element_position()["x"]].get_items().append(equipped_items[self.menus[-1].get_selected_element_position()["x"]])
									self.party[self.menus[1].get_selected_element_position()["x"]].unequip(equipped_items[self.menus[-1].get_selected_element_position()["x"]])
									self.menus.remove(self.menus[-1])

								elif self.menus[-1].__class__ == Menu.TraitWhatMenu:
									if self.menus[-1].get_selected_name() == "New":
										try:
											self.menus.append(Menu.TraitMenu(self.party.get_current_member()))
										except ValueError:
											self.fragile_textboxes.append(Text.TextBox([self.party.get_current_member().get_name()+" has no traits to buy!"],
												self.menus[-1].get_box_width()+UIConstant.MENU_SPACING+2*UIConstant.MENU_BORDER_WIDTH+self.menus[-1].get_position()["x"], self.menus[-1].get_position()["y"]))
									elif self.menus[-1].get_selected_name() == "Owned":
										print("TODO: display owned traits.")

								elif self.menus[-1].__class__ == Menu.TraitMenu:
									self.menus.append(Menu.BuyTraitWhatMenu())

								elif self.menus[-1].__class__ == Menu.BuyTraitWhatMenu:
									if self.menus[-1].get_selected_name() == "Description":
										self.fragile_textboxes.append(Text.TextBox(self.menus[-2].get_traits()[self.menus[-2].get_selected_element_position()["x"]].get_description(),
											self.menus[-1].get_box_width()+UIConstant.MENU_SPACING+2*UIConstant.MENU_BORDER_WIDTH+self.menus[-1].get_position()["x"], self.menus[-1].get_position()["y"]))
									elif self.menus[-1].get_selected_name() == "Buy":
										# Give the trait to the character!
										if self.party.get_current_member().get_tp() < self.menus[-2].get_traits()[self.menus[-2].get_selected_element_position()["x"]].get_cost():
											self.fragile_textboxes.append(Text.TextBox("Not enough TP.",
												self.menus[-1].get_box_width()+UIConstant.MENU_SPACING+2*UIConstant.MENU_BORDER_WIDTH+self.menus[-1].get_position()["x"], self.menus[-1].get_position()["y"]))
										else:
											self.party.get_current_member().add_trait(self.menus[-2].get_traits()[self.menus[-2].get_selected_element_position()["x"]])
											self.menus.remove(self.menus[-1])
											self.menus.remove(self.menus[-1])
								
								elif self.menus[-1].__class__ == Menu.WhomGiveMenu:
									self.party[self.menus[-1].get_selected_element_position()["x"]].give_item(self.menus[-1].get_item())
									self.party.get_current_member().remove_item(self.menus[-1].get_item())
									
									if len(self.party.get_current_member().get_items()) > 0:
										self.menus[1] = Menu.ItemMenu(self.party.get_current_member().get_items())
										self.menus.remove(self.menus[-1])
										self.menus.remove(self.menus[-1])
									else:
										self.menus.remove(self.menus[-1])
										self.menus.remove(self.menus[-1])
										self.menus.remove(self.menus[-1])
					
					if event.type == pygame.KEYUP:
						if event.key == K_q:
							self.map_layer.zoom = 2
						if event.key == K_UP and self.party.get_current_member().velocity[1] < 0:
							for party_member in self.party.get_members():
								party_member.velocity[1] = 0
						if event.key == K_DOWN and self.party.get_current_member().velocity[1] > 0:
							for party_member in self.party.get_members():
								party_member.velocity[1] = 0
						if event.key == K_LEFT and self.party.get_current_member().velocity[0] < 0:
							for party_member in self.party.get_members():
								party_member.velocity[0] = 0
						if event.key == K_RIGHT and self.party.get_current_member().velocity[0] > 0:
							for party_member in self.party.get_members():
								party_member.velocity[0] = 0

				# Game Logic Below
				self.pyscroll_group_data.update()

				# Handles interaction with map objects!
				for wall in self.walls:
					if int(wall.layer)+2 == self.party.get_current_member().get_layer():
						if pygame.Rect.colliderect(self.party.get_current_member().feetrect, pygame.Rect(wall.x, wall.y, wall.width, wall.height)):
							self.party.get_current_member().move_back()

				for warp in self.warps:
					if int(warp.layer)+2 == self.party.get_current_member().get_layer() and pygame.Rect.colliderect(self.party.get_current_member().feetrect, pygame.Rect(warp.x, warp.y, warp.width, warp.height)):
						# Enter a new map
						self.current_map = load_pygame("resources/maps/"+warp.destination+".tmx")
						self.party.get_current_member().set_pos([int(warp.xwarp), int(warp.ywarp)])

						self.pyscroll_group_data.remove(self.party.get_current_member())

						self.pyscroll_map_data = pyscroll.data.TiledMapData(self.current_map)

						self.map_layer = pyscroll.BufferedRenderer(self.pyscroll_map_data, self.screen.get_size())
						self.map_layer.zoom = 2

						self.pyscroll_group_data = PyscrollGroup(map_layer=self.map_layer, default_layer=self.party.get_current_member().get_layer())

						self.walls = []
						self.warps = []
						self.layer_switches = []
						self.npcs = []

						for map_object in self.current_map.objects:
							if map_object.type == "wall":
								self.walls.append(map_object)	
							elif map_object.type == "warp":
								self.warps.append(map_object)
							elif map_object.type == "layer_switch":
								self.layer_switches.append(map_object)

						self.pyscroll_group_data.add(self.party.get_current_member())
						self.pyscroll_group_data.change_layer(self.party.get_current_member(), self.party.get_current_member().get_layer())

						self.load_npcs()

				for layer_switch in self.layer_switches:
					if int(layer_switch.layer)+2 == self.party.get_current_member().get_layer():
						if pygame.Rect.colliderect(self.party.get_current_member().feetrect, pygame.Rect(layer_switch.x, layer_switch.y, layer_switch.width, layer_switch.height)):
							self.party.get_current_member().set_layer(int(layer_switch.layer_to)+2)
							self.pyscroll_group_data.change_layer(self.party.get_current_member(), self.party.get_current_member().get_layer())

				for menu in self.menus:
					menu.update()

				self.colliding = False
				for npc in self.npcs:
					if pygame.Rect.colliderect(self.party.get_current_member().feetrect, pygame.Rect(npc.get_pos()[0], npc.get_pos()[1], npc.get_image().get_width(), npc.get_image().get_height())):
						self.current_colliding_object = npc
						self.colliding = True
				# for interactable in interactables, etc...
				if not self.colliding:
					self.current_colliding_object = None
				else:
					# party.get_current_member().move_back() # Collide and disallow movement
					pass

				# Drawing Below
				self.screen.fill((255, 0, 255))
				
				self.pyscroll_group_data.draw(self.screen)
				self.pyscroll_group_data.center(self.party.get_current_member().rect.center)

				# Draws menus
				for menu in self.menus:
					menu.draw(self.screen)

				for textbox in self.fragile_textboxes:
					textbox.draw(self.screen)

				for textbox in self.resiliant_textboxes:
					textbox.draw(self.screen)

				pygame.display.flip()
				self.clock.tick(60)

			while not self.done and self.battle_screen:
				if self.party.get_members()[self.current_battle_member_index].get_current_hp() <= 0:
					if "down" not in self.party.get_members()[self.current_battle_member_index].get_statuses():
						self.fragile_textboxes.append(Text.TextBox([self.party.get_members()[self.current_battle_member_index].get_name()+" went down!"], (self.screen_size[0]-224)/2, self.screen_size[1]/2))
						self.fragile_textboxes[-1].centre_x()
						self.party.get_members()[self.current_battle_member_index].inflict_status("down")
					self.confirm_action("Nothing", self.party[self.current_battle_member_index])

				battle_screen_events = pygame.event.get()

				for battle_event in battle_screen_events:
					#Battle event handling
					if battle_event.type == pygame.QUIT:
						self.done = True
					if battle_event.type == pygame.KEYDOWN:
						if len(self.fragile_textboxes) > 0:
							self.fragile_textboxes.remove(self.fragile_textboxes[-1])
							if self.battle_over:
								self.battle_screen = False
								self.main_screen = True
								self.enemy_party.set_members([])
								self.menus = []
								self.floating_texts = []
								Sound.play_overworld_music("sea")

						elif battle_event.key == K_x:
							if len(self.menus) > 0:
								Sound.confirm.play()
								if self.menus[-1].__class__ == Menu.BattleMenu:
									if self.menus[-1].get_selected_name() == "Attack":
										# Basic attack
										self.menus.append(Menu.BattleTargetMenu(self.enemy_party.get_members(), self.menus[-1].get_user(), "Attack"))
										self.menus[-1].move_width_back()

									elif self.menus[-1].get_selected_name() == "Spells":
										# Spells
										if len(self.menus[-1].get_user().get_spells()) > 0: #Don't open a spell menu if the character has no spells.
											self.menus.append(Menu.SpellMenu(self.party[self.current_battle_member_index].get_spells()))
										else:
											self.fragile_textboxes.append(Text.TextBox(["You have no spells!"], (self.screen_size[0]-224)/2, self.screen_size[1]/2))
											self.fragile_textboxes[-1].centre_x()

									elif self.menus[-1].get_selected_name() == "Defend":
										# Defend
										self.confirm_action("Defend", self.party[self.current_battle_member_index])

									elif self.menus[-1].get_selected_name() == "Item":
										# Item
										if len(self.menus[-1].get_user().get_items()) > 0:
											self.menus.append(Menu.ItemMenu(self.party[self.current_battle_member_index].get_items()))
										else:
											self.fragile_textboxes.append(Text.TextBox(["You have no items."], (self.screen_size[0]-224)/2, self.screen_size[1]/2))
											self.fragile_textboxes[-1].centre_x()

									elif self.menus[-1].get_selected_name() == "Run":
										# This block sets the party speeds to the speed of their slowest member.
										party_speed = False
										for party_member in self.party:
											if not party_speed:
												party_speed = party_member.get_spd()
											elif party_member.get_spd() < party_speed:
												party_speed = party_member.get_spd()

										enemy_party_speed = False
										for enemy_party_member in self.enemy_party:
											if not enemy_party_speed:
												enemy_party_speed = enemy_party_member.get_spd()
											elif enemy_party_member.get_spd() < enemy_party_speed:
												enemy_party_speed = enemy_party_member.get_spd()

										# If your party is faster, you get away.
										if party_speed > enemy_party_speed: 
											# Clears enemy party
											self.enemy_party.set_members([])
											self.menus = []
											self.fragile_textboxes.append(Text.TextBox(["You ran away..."], (self.screen_size[0]-224)/2, self.screen_size[1]/2))
											self.fragile_textboxes[-1].centre_x()
											self.battle_over = True
											Sound.play_overworld_music("escape", 0)
										else:
											self.fragile_textboxes.append(Text.TextBox(["You couldn't get away!"], (self.screen_size[0]-224)/2, self.screen_size[1]/2))
											self.fragile_textboxes[-1].centre_x()
											
											for i in range(self.current_battle_member_index, len(self.party.get_members())):
												self.confirm_action("Nothing", self.party[i])

								elif self.menus[-1].__class__ == Menu.SpellMenu:
									selected_spell = self.party[self.current_battle_member_index].get_spells()[self.menus[-1].get_selected_element_position()["x"]]

									if self.party[self.current_battle_member_index].get_current_mp() >= selected_spell.get_mp_cost():
										if selected_spell.get_targeting() == "self":
											self.confirm_action("Spell", self.party[self.current_battle_member_index], self.party[self.current_battle_member_index], selected_spell)

										elif selected_spell.get_targeting() == "friendly":
											self.menus.append(Menu.BattleTargetMenu(self.party.get_members(), self.menus[0].get_user(), "Spell", selected_spell, True))
											self.menus[-1].move_width_back()

										elif selected_spell.get_targeting() == "enemy":
											self.menus.append(Menu.BattleTargetMenu(self.enemy_party.get_members(), self.menus[0].get_user(), "Spell", selected_spell))
											self.menus[-1].move_width_back()

									else:
										self.fragile_textboxes.append(Text.TextBox(["Not enough MP."], self.menus[-1].get_position()["x"]+self.menus[-1].get_box_width()+UIConstant.MENU_SPACING+2*UIConstant.MENU_BORDER_WIDTH, self.menus[-1].get_position()["y"]))
										selected_spell = None

								elif self.menus[-1].__class__ == Menu.ItemMenu:
									selected_item = self.party[self.current_battle_member_index].get_items()[self.menus[-1].get_selected_element_position()["x"]]

									if selected_item.get_useable():
										self.menus.append(Menu.WhomUseMenu(self.party[self.current_battle_member_index].get_items()[self.menus[-1].get_selected_element_position()["x"]], self.party))
									else:
										self.fragile_textboxes.append(Text.TextBox([selected_item.get_name()+" is not useable."], (self.screen_size[0]-224)/2, self.screen_size[1]/2))

								elif self.menus[-1].__class__ == Menu.WhomUseMenu:
									self.party[self.current_battle_member_index].get_items().remove(self.menus[-1].get_item())

									self.confirm_action("Item", self.party[self.current_battle_member_index], # Item user
										self.party[self.menus[-1].get_selected_element_position()["x"]], # Item target
										self.menus[-1].get_item()) # Passes the actual item
									
										
									'''if len(party[current_battle_member_index].get_items()) > 0:
											menus[1] = Menu.ItemMenu(party[current_battle_member_index].get_items())
									else:
										menus.remove(menus[-1])
									menus.remove(menus[-1])
									menus.remove(menus[-1])'''

								elif self.menus[-1].__class__ == Menu.BattleTargetMenu:
									if self.menus[-2].__class__ == Menu.BattleMenu:
										self.confirm_action("Attack", self.party[self.current_battle_member_index], self.enemy_party[self.menus[-1].get_selected_element_position()["x"]])
								
									elif self.menus[-2].__class__ == Menu.SpellMenu:
										if self.menus[-1].get_friendly() == True:
											self.confirm_action("Spell", self.party[self.current_battle_member_index], self.party[self.menus[-1].get_selected_element_position()["x"]], self.menus[-1].get_spell())
										else:
											self.confirm_action("Spell", self.party[self.current_battle_member_index], self.enemy_party[self.menus[-1].get_selected_element_position()["x"]], self.menus[-1].get_spell())

						elif battle_event.key == K_z:
							if len(self.menus) > 0:
								Sound.back.play()
								if self.menus[-1].__class__ != Menu.BattleMenu:
									self.menus.remove(self.menus[-1]) # Delete the topmost menu, as long as you aren't on the base menu!
								else: # If you are on the base menu, do this:
									if self.current_battle_member_index > 0: # If you aren't on the first party member, you can cancel the previous member's action and reselect
										self.battle_actions.remove(self.battle_actions[-1])
										self.current_battle_member_index -= 1

						elif battle_event.key == K_UP:
							if len(self.menus) > 0:
								self.menus[-1].move_selection_up()
								Sound.menu.play()
						elif battle_event.key == K_DOWN:
							if len(self.menus) > 0:
								self.menus[-1].move_selection_down()
								Sound.menu.play()
						elif battle_event.key == K_LEFT:
							if len(self.menus) > 0:
								self.menus[-1].move_selection_left()
								Sound.menu.play()
						elif  battle_event.key == K_RIGHT:
							if len(self.menus) > 0:
								self.menus[-1].move_selection_right()
								Sound.menu.play()

				#Battle logic below
				for menu in self.menus:
					menu.update()

				for floating_text in self.floating_texts:
					floating_text.update()
					if floating_text.age > floating_text.lifetime:
						self.floating_texts.remove(floating_text)

				#Battle Drawing below
				self.battle_drawing()
				self.clock.tick(60)

			while not self.done and self.paused:# Paused gameloop
				for event in pygame.event.get():
					#Event handling
					if event.type == pygame.QUIT:
						self.done = True
					if event.type == pygame.KEYDOWN:
						if event.key == K_x:
							self.paused = False

				# Paused drawing below
				Text.draw_text(self.screen, self.screen_size[0]/2-Text.get_text_width("PAUSED", UIConstant.HUGE_FONT_SIZE), self.screen_size[1]/3, "PAUSED", UIConstant.HUGE_FONT_SIZE)

				pygame.display.flip()
				self.clock.tick(60)

		self.end_game() # Exits game if gameloop is exited

	def end_game(self):
		pygame.quit()

	def initate_battle(self):
		# Starts a battle

		for i in range(randint(1,4)):
			self.enemy_party.add_member(EnemyPool.test[randint(0, len(EnemyPool.test)-1)]([0,0], randint(1,2)))

		self.menus = [Menu.BattleMenu(self.party[self.current_battle_member_index])]

		Battle.position_for_battle(self.party, self.screen_size[1]-140)
		Battle.position_for_battle(self.enemy_party, 64)

		Sound.play_battle_music()

		self.battle_over = False

		self.battle_screen = True
		self.main_screen = False

	def load(self, gamefile):
		# Method for loading the game
		try:
			print("\nLoading shelf...")
			loaded_game = shelve.open("savegames/savegame"+gamefile+".sav")
			print("Shelf loaded.\n")
			
			print("Clearing party from group data...")
			self.pyscroll_group_data.remove(self.party.get_current_member())
			print("Party cleared from group data.\n")

			print("Loading party...")
			loaded_party = loaded_game["party"]
			print("Party loaded.\n")

			print("Loading map...")
			loaded_map = loaded_game["map"]
			print("Map loaded.\n")

			print("Closing shelf...")
			loaded_game.close()
			print("Shelf closed.\n")

			print("Assigning variables to loaded values...")
			self.party = loaded_party

			self.current_map = loaded_map
			self.current_map = load_pygame("resources/maps/"+loaded_map+".tmx")
			print("Variables assigned.\n")

			print("Generating map objects...")
			self.walls = []
			self.warps = []
			self.layer_switches = []

			for map_object in self.current_map.objects:
				if map_object.type == "wall":
					self.walls.append(map_object)
				elif map_object.type == "warp":
					self.warps.append(map_object)
				elif map_object.type == "layer_switch":
					self.layer_switches.append(map_object)
			print("Map objects generated.\n")
			
			print("Exiting menus...")
			self.menus = []
			print("Menus exited.\n")

			print("Creating map data...")
			self.pyscroll_map_data = pyscroll.data.TiledMapData(self.current_map)
			print("Map data created.\n")

			print("Creating map layer...")
			self.map_layer = pyscroll.BufferedRenderer(self.pyscroll_map_data, self.screen.get_size())
			self.map_layer.zoom = 2
			print("Map layer created.\n")

			print("Creating group data...")
			self.pyscroll_group_data = PyscrollGroup(map_layer=self.map_layer, default_layer=self.party.get_current_member().get_layer())
			print("Group data created.\n")
			
			print("Reloading party and item images...")
			for party_member in self.party.get_members():
				party_member.reload_images()
				party_member.reload_spell_lines()
				party_member.reload_sounds()
				for item in party_member.get_items():
					item.reload_image()
				for spell in party_member.spells:
					spell.reload_image()
					spell.reload_sound()
			print("Images reloaded.")

			print("Adding party to group data...")
			self.pyscroll_group_data.add(self.party.get_current_member())
			self.pyscroll_group_data.change_layer(self.party.get_current_member(), self.party.get_current_member().get_layer())
			print("Party added to group data.\n")

			print("Loading NPCS...")
			self.load_npcs()
			print("NPCs loaded.")

			self.title_screen = False
			self.main_screen = True

			Sound.play_overworld_music("sea")
		except:
			print("Load error.")

	def load_npcs(self):
		map_npc_list = self.current_map.npcs_by_id.split()
		map_npc_x_positions = self.current_map.respective_npc_x.split()
		map_npc_y_positions = self.current_map.respective_npc_y.split()

		for i in range(len(map_npc_list)):
			self.npcs.append(NPCID.npc_id_list[int(map_npc_list[i])]([int(map_npc_x_positions[i]), int(map_npc_y_positions[i]) ]))

		for npc in self.npcs:
			self.pyscroll_group_data.add(npc)
			self.pyscroll_group_data.change_layer(npc, self.party.get_current_member().get_layer())

	def save(self, gamefile):
		print("\nSaving to game "+gamefile+"...")
		print("Loading shelf...\n")
		loaded_game = shelve.open("savegames/savegame"+gamefile+".sav")
		print("Shelf loaded.\n")
		print("Clearing party from group data...")
		'''for party_member in party.get_members():
			pyscroll_group_data.remove(party_member)'''
		self.pyscroll_group_data.remove(self.party.get_current_member())
		print("Party cleared from group data.\n")

		print("Clearing party and item images...")
		for member in self.party.get_members():
			member.clear_images()
			member.clear_spell_lines()
			member.clear_sounds()
			for item in member.get_items():
				item.clear_image()
			for spell in member.spells:
				spell.clear_image()
		print("Images cleared.")

		print("Saving party...")
		loaded_game["party"] = self.party
		print("Party saved.\n")

		print("Adding party to group data...")
		self.pyscroll_group_data.add(self.party.get_current_member())
		self.pyscroll_group_data.change_layer(self.party.get_current_member(), self.party.get_current_member().get_layer())

		print("Party added to group data.\n")

		print("Saving map...")
		loaded_game["map"] = self.current_map.name
		print("Map saved.\n")
			
		print("Closing shelf...")
		loaded_game.close()
		print("Shelf closed.\n")

		print("Reloading party and item images...")
		for party_member in self.party.get_members():
			party_member.reload_images()
			party_member.reload_spell_lines()
			party_member.reload_sounds()
			for item in party_member.get_items():
				item.reload_image()
			for spell in party_member.spells:
				spell.reload_image()
				spell.reload_sound()
		print("Images reloaded.")

		self.menus.remove(self.menus[-1])

	def jiggle_battle_sprite(self, battle_actor):
		# Jiggle the actor so you know they're taking the action
		for i in range(3):
			battle_actor.shift_battle_pos(UIConstant.BATTLE_JIGGLE_AMOUNT, 0)
			self.battle_drawing(exclude_selectors=True, exclude_menus=True)
			time.sleep(0.1)
			battle_actor.shift_battle_pos(-UIConstant.BATTLE_JIGGLE_AMOUNT, 0)
			self.battle_drawing(exclude_selectors=True, exclude_menus=True)
			time.sleep(0.1)
		time.sleep(0.4)

	def battle_drawing(self, exclude_menus=False, exclude_floating=False, exclude_selectors=False):
		# Drawing within a battle
		self.screen.fill((0, 0 ,0))
		self.screen.blit(BackgroundImage.grass, (0, 0))
		self.party_text_colour = UIConstant.PARTY_TEXT_COLOUR

		for party_member in self.party:
			self.screen.blit(party_member.get_battle_image(), party_member.get_battle_pos())

		for enemy_party_member in self.enemy_party:
			self.screen.blit(enemy_party_member.get_battle_image(), enemy_party_member.get_battle_pos())

		pygame.draw.rect(self.screen, UIConstant.BACKGROUND_COLOUR, (self.screen_size[0]-224, 0, 224, self.screen_size[1]))
				
		for i in range(len(self.party.get_members())):
			try:
				self.party[self.current_battle_member_index]
			except:
				pass
			else:
				if self.party[i] == self.party[self.current_battle_member_index]:
					self.party_text_colour = UIConstant.SELECTED_PARTY_TEXT_COLOUR
				else:
					self.party_text_colour = UIConstant.PARTY_TEXT_COLOUR
				if self.party[i].get_current_hp() <= self.party[i].get_hp()/3:
					self.hp_text_colour = UIConstant.LOW_HP_TEXT_COLOUR
				if self.party[i].get_current_hp() <= 0:
					self.hp_text_colour = UIConstant.NO_HP_TEXT_COLOUR

			Text.draw_text(self.screen, self.screen_size[0]-224+26, (i+1)*80 - 60, self.party[i].get_name(), UIConstant.LARGE_FONT_SIZE, self.party_text_colour)
			Text.draw_text(self.screen, self.screen_size[0]-244+48, (i+1)*80 - 24, "HP: "+str(self.party[i].get_current_hp())+"/"+str(self.party[i].get_hp()), UIConstant.FONT_SIZE, self.hp_text_colour)
			Text.draw_text(self.screen, self.screen_size[0]-244+48, (i+1)*80 - 14, "MP: "+str(self.party[i].get_current_mp())+"/"+str(self.party[i].get_mp()), UIConstant.FONT_SIZE, UIConstant.FONT_COLOUR)

		if not exclude_selectors:
			self.selectors[0].set_pos(self.party[self.current_battle_member_index].get_battle_pos()[0]-16,
				self.party[self.current_battle_member_index].get_battle_pos()[1]-16)
			self.selectors[1].set_pos(self.party[self.current_battle_member_index].get_battle_pos()[0]+self.party[self.current_battle_member_index].get_battle_image().get_width(),
				self.party[self.current_battle_member_index].get_battle_pos()[1]-16)
			self.selectors[2].set_pos(self.party[self.current_battle_member_index].get_battle_pos()[0]-16,
				self.party[self.current_battle_member_index].get_battle_pos()[1]+self.party[self.current_battle_member_index].get_battle_image().get_height())
			self.selectors[3].set_pos(self.party[self.current_battle_member_index].get_battle_pos()[0]+self.party[self.current_battle_member_index].get_battle_image().get_width(),
				self.party[self.current_battle_member_index].get_battle_pos()[1]+self.party[self.current_battle_member_index].get_battle_image().get_height())

			for selector in self.selectors:
				selector.update()
				self.screen.blit(selector.get_image(), selector.get_pos())

		if not exclude_floating:
			for floating_text in self.floating_texts:
				floating_text.draw(self.screen)

		if not exclude_menus:
			for menu in self.menus:
				menu.draw(self.screen)

		for textbox in self.fragile_textboxes:
			textbox.draw(self.screen)

		pygame.display.flip() #Now you can see the effects

	def fade_out(self, character):
		copy_battle_image = character.get_battle_image()
		transparent_surface = pygame.Surface((self.screen_size[0], self.screen_size[1]))
		''' START FADE-OUT EFFECT CODE '''
		for i in range(0, 16):
			transparent_surface.set_alpha(255-i*16)
			
			self.screen.fill((0, 0 ,0))
			self.screen.blit(BackgroundImage.grass, (0, 0))
			for party_member in self.party:
				self.screen.blit(party_member.get_battle_image(), party_member.get_battle_pos())
			
			for enemy_party_member in self.enemy_party:
				if enemy_party_member != character:
					self.screen.blit(enemy_party_member.get_battle_image(), enemy_party_member.get_battle_pos())

			pygame.draw.rect(self.screen, UIConstant.BACKGROUND_COLOUR, (self.screen_size[0]-224, 0, 224, self.screen_size[1]))
			for i in range(len(self.party.get_members())):
				self.party_text_colour = UIConstant.PARTY_TEXT_COLOUR

				Text.draw_text(self.screen, self.screen_size[0]-224+26, (i+1)*80 - 60, self.party[i].get_name(), UIConstant.LARGE_FONT_SIZE, self.party_text_colour)
				Text.draw_text(self.screen, self.screen_size[0]-244+48, (i+1)*80 - 24, "HP: "+str(self.party[i].get_current_hp())+"/"+str(self.party[i].get_hp()), UIConstant.FONT_SIZE, self.hp_text_colour)
				Text.draw_text(self.screen, self.screen_size[0]-244+48, (i+1)*80 - 14, "MP: "+str(self.party[i].get_current_mp())+"/"+str(self.party[i].get_mp()), UIConstant.FONT_SIZE, UIConstant.FONT_COLOUR)

			for floating_text in self.floating_texts:
				#floating_text.update()
				floating_text.draw(self.screen)

			transparent_surface.fill((0,0,0))
			transparent_surface.blit(BackgroundImage.grass, (0, 0))
			for party_member in self.party:
				transparent_surface.blit(party_member.get_battle_image(), party_member.get_battle_pos())
			for enemy_party_member in self.enemy_party:
				if enemy_party_member != character: # If the enemy isn't the one killed, draw it
					transparent_surface.blit(enemy_party_member.get_battle_image(), enemy_party_member.get_battle_pos())

			pygame.draw.rect(transparent_surface, UIConstant.BACKGROUND_COLOUR, (self.screen_size[0]-224, 0, 224, self.screen_size[1]))
			for i in range(len(self.party.get_members())):
				self.party_text_colour = UIConstant.PARTY_TEXT_COLOUR

				Text.draw_text(transparent_surface, self.screen_size[0]-224+26, (i+1)*80 - 60, self.party[i].get_name(), UIConstant.LARGE_FONT_SIZE, self.party_text_colour)
				Text.draw_text(transparent_surface, self.screen_size[0]-244+48, (i+1)*80 - 24, "HP: "+str(self.party[i].get_current_hp())+"/"+str(self.party[i].get_hp()), UIConstant.FONT_SIZE, self.hp_text_colour)
				Text.draw_text(transparent_surface, self.screen_size[0]-244+48, (i+1)*80 - 14, "MP: "+str(self.party[i].get_current_mp())+"/"+str(self.party[i].get_mp()), UIConstant.FONT_SIZE, UIConstant.FONT_COLOUR)

			for floating_text in self.floating_texts:
				#floating_text.update()
				floating_text.draw(transparent_surface)
			
			transparent_surface.blit(copy_battle_image, character.get_battle_pos())
			self.screen.blit(transparent_surface, (0, 0))
			
			pygame.display.flip()
			self.clock.tick(60)
		
		del(transparent_surface)

		self.enemy_party.remove_member(character)
		self.experience_pool += character.get_death_exp()

		''' END FADE-OUT EFFECT CODE '''
	
	def confirm_action(self, action, user, target=None, ability=None):
		self.battle_actions.append([action, user, user.get_spd(), target, ability])
		
		self.current_battle_member_index += 1
		self.floating_texts = []
		
		if self.current_battle_member_index > len(self.party.get_members())-1:
			
			self.accepting_input = False
			pygame.event.clear()
			
			# A temporary, very simple, and very bad AI to determine the enemies' moves.
			for enemy_party_member in self.enemy_party.get_members():
				if not randint(0, 9):
					self.battle_actions.append(["Defend", enemy_party_member, enemy_party_member.get_spd()])
				else:
					self.battle_actions.append(["Attack", enemy_party_member, enemy_party_member.get_spd(), self.party[randint(0,1)-1]])
			
			# Organise the battle actions by user speed, highest first
			self.battle_actions.sort(key=lambda x: int(x[2]), reverse=True)
			
			# Iterate over the battle actions
			for battle_action in self.battle_actions:

				crit = False
				colour = (255, 0, 0)
				
				battle_action[1].set_defending(False) # Undefend the current actor incase they defended last turn
				
				# Do effects of status conditions
				if "paralyzed" in battle_action[1].get_statuses():
					if randint(0, 1):
						battle_action[0] = "Nothing"
						self.floating_texts.append(Text.FloatingText(battle_action[1].get_battle_pos()[0], battle_action[1].get_battle_pos()[1]-16, "Paralyzed", UIConstant.LARGE_FONT_SIZE, (200, 200, 0), UIConstant.FLOATING_TEXT_FRAMES))

				if "poisoned" in battle_action[1].get_statuses():
					poison_damage = randint(1, 10)
					battle_action[1].heal(-poison_damage, Stat.HitPoints(0))
					self.floating_texts.append(Text.FloatingText(battle_action[1].get_battle_pos()[0], battle_action[1].get_battle_pos()[1]-16, str(poison_damage), UIConstant.LARGE_FONT_SIZE, (200, 0, 200), UIConstant.FLOATING_TEXT_FRAMES))
				
				if "confused" in battle_action[1].get_statuses():
					print("TODO: Confusion.")

				if "hesitant" in battle_action[1].get_statuses():
					if not randint(0, 2):
						battle_action[0] = "Nothing"
						self.floating_texts.append(Text.FloatingText(battle_action[1].get_battle_pos()[0], battle_action[1].get_battle_pos()[1]-16, "Hesitant", UIConstant.LARGE_FONT_SIZE, (20, 20, 200), UIConstant.FLOATING_TEXT_FRAMES))

				if battle_action[1].get_current_hp() > 0:				

					if battle_action[0] == "Nothing":
						pass

					elif battle_action[0] == "Attack":
						if battle_action[3] in self.enemy_party or battle_action[3] in self.party:
							self.jiggle_battle_sprite(battle_action[1])
							damage = randint(floor(battle_action[1].get_atk()*0.9), floor(battle_action[1].get_atk()*1.35)) # Damage formula
							if damage in range(floor(battle_action[1].get_atk()*1.25), floor(battle_action[1].get_atk()*1.35)): # If near max damage was scored, you may get a crit!
								if randint(0, floor(battle_action[3].get_luk()*100/(battle_action[1].get_atk()*1.35 - battle_action[1].get_atk()*0.9))) < battle_action[1].get_luk():
									crit = True
									colour = (0, 255, 255)
									damage *= 2

							damage -= floor(randint(floor(battle_action[3].get_dfn()/2), battle_action[3].get_dfn())/2) # Defence formula

							if battle_action[3].get_defending():
								damage -= randint(floor(battle_action[3].get_dfn()/2), battle_action[3].get_dfn()) # Additional reduction if defending

							if damage < 1: # Make sure that a target can't take negative damage and heal!
								damage = 0

							battle_action[3].heal(-damage, Stat.HitPoints(0))
							self.floating_texts.append(Text.FloatingText(battle_action[3].get_battle_pos()[0], battle_action[3].get_battle_pos()[1]-16, str(damage), UIConstant.LARGE_FONT_SIZE, colour, UIConstant.FLOATING_TEXT_FRAMES))
							battle_action[1].attack_sound.play()
						else: # If the enemy has been defeated in the meantime
							# Defend instead
							colour = (50, 50, 255)
							battle_action[1].set_defending(True)
							self.floating_texts.append(Text.FloatingText(battle_action[1].get_battle_pos()[0], battle_action[1].get_battle_pos()[1]-16, "Defending.", UIConstant.LARGE_FONT_SIZE, colour, UIConstant.FLOATING_TEXT_FRAMES))
							Sound.buff.play()

					elif battle_action[0] == "Defend":
						colour = (50, 50, 255)
						battle_action[1].set_defending(True)
						self.floating_texts.append(Text.FloatingText(battle_action[1].get_battle_pos()[0], battle_action[1].get_battle_pos()[1]-16, "Defending.", UIConstant.LARGE_FONT_SIZE, colour, UIConstant.FLOATING_TEXT_FRAMES))
						Sound.buff.play()

					elif battle_action[0] == "Item":
						if battle_action[4].__class__.__bases__[0] == Item.Medicine:
							colour = (0, 255, 0)
							if battle_action[4].get_stat().get_name() == "MP":
								colour = (10, 20, 255)
							
							battle_action[3].heal(battle_action[4].get_value(), battle_action[4].get_stat())
							self.floating_texts.append(Text.FloatingText(battle_action[3].get_battle_pos()[0], battle_action[3].get_battle_pos()[1]-16, str(battle_action[4].get_value()), UIConstant.LARGE_FONT_SIZE, colour, UIConstant.FLOATING_TEXT_FRAMES))

					elif battle_action[0] == "Spell":
						if battle_action[3] in self.party or battle_action[3] in self.enemy_party:
							self.jiggle_battle_sprite(battle_action[1])
							battle_action[1].shift_current_mp(-battle_action[4].get_mp_cost())
	
							if battle_action[4].__class__.__bases__[0] == Spell.HealingSpell:
								colour = (0, 255, 0)
								damage = randint(floor(battle_action[4].get_power()*0.9), floor(battle_action[4].get_power()*1.35))
								
								if "down" in battle_action[3].get_statuses():
									damage = 0
									Sound.back.play()
									colour = (250, 255, 0)
								else:
									Sound.health.play()
	
								battle_action[3].heal(damage, Stat.HitPoints(0))
								self.floating_texts.append(Text.FloatingText(battle_action[3].get_battle_pos()[0], battle_action[3].get_battle_pos()[1]-16, str(damage), UIConstant.LARGE_FONT_SIZE, colour, UIConstant.FLOATING_TEXT_FRAMES))
	
							elif battle_action[4].__class__.__bases__[0] == Spell.BuffSpell:
								colour = (100, 100, 255)
								buff_level = randint(floor(battle_action[4].get_stat_power()*0.9), floor(battle_action[4].get_stat_power()*1.35)) # Buff formula
								battle_action[3].buff(buff_level, battle_action[4].get_stat_target())
								self.floating_texts.append(Text.FloatingText(battle_action[3].get_battle_pos()[0], battle_action[3].get_battle_pos()[1]-16, battle_action[4].get_stat_target().upper()+" up!", UIConstant.LARGE_FONT_SIZE, colour, UIConstant.FLOATING_TEXT_FRAMES))
								Sound.buff.play()
	
							elif battle_action[4].__class__.__bases__[0] == Spell.DamageSpell:
								colour = (255, 0, 0)
								mag_and_pow = battle_action[1].get_mag() + battle_action[4].get_power() # Magic damage formula
								damage = randint(floor(mag_and_pow*0.9), floor(mag_and_pow*1.35))
								damage -= randint(floor(battle_action[3].get_res()/2), battle_action[3].get_res())
								if battle_action[3].get_defending():
									damage -= randint(floor(battle_action[3].get_res()/2), battle_action[3].get_res())
	
								battle_action[3].heal(-damage, Stat.HitPoints(0))
								self.floating_texts.append(Text.FloatingText(battle_action[3].get_battle_pos()[0], battle_action[3].get_battle_pos()[1]-16, str(damage), UIConstant.LARGE_FONT_SIZE, colour, UIConstant.FLOATING_TEXT_FRAMES))
								battle_action[4].sound.play()
	
							elif battle_action[4].__class__.__bases__[0] == Spell.NerfSpell:
								colour = (255, 255, 0)
								nerf_level = randint(floor(battle_action[4].get_stat_power()*0.9), floor(battle_action[4].get_stat_power()*1.35)) # Nerf formula
								battle_action[3].buff(-nerf_level, battle_action[4].get_stat_target())
								self.floating_texts.append(Text.FloatingText(battle_action[3].get_battle_pos()[0], battle_action[3].get_battle_pos()[1]-16, battle_action[4].get_stat_target().upper()+" down.", UIConstant.LARGE_FONT_SIZE, colour, UIConstant.FLOATING_TEXT_FRAMES))
								Sound.nerf.play()
	
							elif battle_action[4].__class__.__bases__[0] == Spell.StatusSpell:
								status_target = battle_action[4].get_status_target()
								if battle_action[4].get_inflict():
									colour = (255, 255, 0)
									if status_target not in battle_action[3].get_statuses():
										battle_action[3].inflict_status(status_target)
										self.floating_texts.append(Text.FloatingText(battle_action[3].get_battle_pos()[0], battle_action[3].get_battle_pos()[1]-16, "+"+status_target.upper(), UIConstant.LARGE_FONT_SIZE, colour, UIConstant.FLOATING_TEXT_FRAMES))
										Sound.nerf.play()
	
								else:
									if status_target in battle_action[3].get_statuses():
										colour = (0, 255, 255)
										battle_action[3].cure_status(status_target)
										self.floating_texts.append(Text.FloatingText(battle_action[3].get_battle_pos()[0], battle_action[3].get_battle_pos()[1]-16, "-"+status_target.upper(), UIConstant.LARGE_FONT_SIZE, colour, UIConstant.FLOATING_TEXT_FRAMES))
										Sound.buff.play()
	
										if status_target == "down":
											battle_action[3].heal(1, Stat.HitPoints(0))
						else:
							# Target is dead, defend instead
							colour = (50, 50, 255)
							battle_action[1].set_defending(True)
							self.floating_texts.append(Text.FloatingText(battle_action[1].get_battle_pos()[0], battle_action[1].get_battle_pos()[1]-16, "Defending.", UIConstant.LARGE_FONT_SIZE, colour, UIConstant.FLOATING_TEXT_FRAMES))
							Sound.buff.play()

					else:
						print(battle_action[1].get_name()+" has selected an unknown action. This is probably a bug! ERROR 30-0")
						self.fragile_textboxes.append(Text.TextBox(["ERROR 30-0", battle_action[1].get_name()+" has selected an unknown action."], 100, 100))
					
					try:
						battle_action[3].get_current_hp() # Make sure there is a target with hp
					except:
						pass
					else:
						if battle_action[3].get_current_hp() <= 0:
							if battle_action[3] in self.enemy_party:
								# Dead enemy
								self.fade_out(battle_action[3])

							else:
								# Target is already dead, make sure the HP doesn't go negative
								battle_action[3].heal(-battle_action[3].get_current_hp(), Stat.HitPoints(0))

				else:
					# Current actor is dead
					if "down" not in battle_action[1].get_statuses():
						if battle_action[1] in self.party.get_members():
							self.fragile_textboxes.append(Text.TextBox([battle_action[1].get_name()+" went down!"], (self.screen_size[0]-224)/2 , self.screen_size[1]/2 ))
							self.fragile_textboxes[-1].centre_x()
						
						battle_action[1].inflict_status("down")


				# Battle Drawing below (action loop)
				self.battle_drawing(exclude_menus=True, exclude_selectors=True)
				self.clock.tick(60)

				if battle_action[0] == "Spell":
					time.sleep(battle_action[4].get_sleep_time())
				else:
					time.sleep(0.6)

			for enemy_party_member in self.enemy_party:
				# We need to iterate through the enemy party in case an enemy died,
				# but wasn't the target of any action, eg. died to poison damage
				if enemy_party_member.get_current_hp() <= 0:
					self.fade_out(enemy_party_member)
			
			self.current_battle_member_index = 0
			self.battle_actions = []
			self.menus = [Menu.BattleMenu(self.party[self.current_battle_member_index])]
			self.accepting_input = True
			pygame.event.clear()

			if len(self.enemy_party.get_members()) < 1 and len(self.fragile_textboxes) < 1:
				#Battle won!
				self.experience_pool = floor(self.experience_pool/len(self.party.get_members()))
				for party_member in self.party:
					party_member.debuff()
					for status in party_member.get_statuses():
						if status != "down":
							party_member.cure_status(status)
					
					if "down" not in party_member.get_statuses():
						party_member.shift_exp(self.experience_pool)

				self.menus = []
				self.fragile_textboxes.append(Text.TextBox(["Victory! Gained "+str(self.experience_pool)+" EXP!"], (self.screen_size[0]-224)/2, self.screen_size[1]/2))
				self.fragile_textboxes[-1].centre_x()
				self.battle_over = True
				Sound.play_overworld_music("fanfare")

		else:
			self.accepting_input = True
			self.menus = [Menu.BattleMenu(self.party[self.current_battle_member_index])]

def main():
	game = ModeratelySeafaringGame()
	game.begin_game()
	print("Thank you for playing!")

if __name__ == "__main__":
	pygame.mixer.pre_init(44100, -16, 2, 512)
	pygame.mixer.init()
	pygame.init()
	pygame.font.init()
	pygame.display.set_caption("Moderately Seafaring")

	main()
