#The gameloop for Moderately Seafaring, an RPG
#4 Dec, 2016

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

def confirm_action(action, user, target=None, ability=None):
	global party
	global enemy_party
	global current_battle_member_index
	global menus
	global battle_actions
	global floating_texts
	global main_screen
	global battle_screen
	global experience_pool
	global fragile_textboxes
	global battle_over

	battle_actions.append( (action, user, user.get_spd(), target, ability) )
	
	current_battle_member_index += 1
	if current_battle_member_index > len(party.get_members()) - 1:
		#TODO: Let the AI add battle actions
		for enemy_party_member in enemy_party.get_members():
			if not randint(0, 9):
				battle_actions.append( ("Defend", enemy_party_member, enemy_party_member.get_spd()) )
			else:
				battle_actions.append( ("Attack", enemy_party_member, enemy_party_member.get_spd(), party[randint(0,1)-1]) )
		#TODO: Organise the battle actions by speed
		
		#Iterate over the battle actions
		for battle_action in battle_actions:
			crit = False
			colour = (255, 0, 0)
			
			battle_action[1].set_defending(False) #
			if battle_action[1].get_current_hp() > 0:

				if battle_action[0] == "Nothing":
					print(battle_action[1].get_name()+" is down and cannot act!")

				elif battle_action[0] == "Attack":
				
					damage = randint(floor(battle_action[1].get_atk()*0.9), floor(battle_action[1].get_atk()*1.35))
					if damage == floor(battle_action[1].get_atk()*1.35):
						if randint(0, floor(battle_action[3].get_luk()*100/(battle_action[1].get_atk()*1.35 - battle_action[1].get_atk()*0.9))) < battle_action[1].get_luk():
							crit = True
							colour = (0, 255, 255)
							damage *= 2

					damage -= randint(floor(battle_action[3].get_dfn()/2), battle_action[3].get_dfn())

					if battle_action[3].get_defending():
						damage -= randint(floor(battle_action[3].get_dfn()/2), battle_action[3].get_dfn())

					if damage < 1:
						damage = 0

					battle_action[3].heal(-damage, Stat.HitPoints(0))
					floating_texts.append(Text.FloatingText(battle_action[3].get_battle_pos()[0], battle_action[3].get_battle_pos()[1]-16, str(damage), 32, colour, UIConstant.FLOATING_TEXT_FRAMES))
					battle_action[1].attack_sound.play()

				elif battle_action[0] == "Defend":
					colour = (50, 50, 255)
					battle_action[1].set_defending(True)
					floating_texts.append(Text.FloatingText(battle_action[1].get_battle_pos()[0], battle_action[1].get_battle_pos()[1]-16, "Defending.", 32, colour, UIConstant.FLOATING_TEXT_FRAMES))
					Sound.buff.play()

				elif battle_action[0] == "Spell":
					battle_action[1].shift_current_mp(-battle_action[4].get_mp_cost())

					if battle_action[4].__class__.__bases__[0] == Spell.HealingSpell:
						colour = (0, 255, 0)
						damage = randint(floor(battle_action[4].get_power()*0.9), floor(battle_action[4].get_power()*1.35))
						battle_action[3].heal(damage, Stat.HitPoints(0))
						floating_texts.append(Text.FloatingText(battle_action[3].get_battle_pos()[0], battle_action[3].get_battle_pos()[1]-16, str(damage), 32, colour, UIConstant.FLOATING_TEXT_FRAMES))
						Sound.health.play()

					elif battle_action[4].__class__.__bases__[0] == Spell.BuffSpell:
						colour = (100, 100, 255)
						buff_level = randint(floor(battle_action[4].get_stat_power()*0.9), floor(battle_action[4].get_stat_power()*1.35))
						battle_action[3].buff(buff_level, battle_action[4].get_stat_target())
						floating_texts.append(Text.FloatingText(battle_action[3].get_battle_pos()[0], battle_action[3].get_battle_pos()[1]-16, battle_action[4].get_stat_target().upper()+" up!", 32, colour, UIConstant.FLOATING_TEXT_FRAMES))
						Sound.buff.play()

					elif battle_action[4].__class__.__bases__[0] == Spell.DamageSpell:
						colour = (255, 0, 0)
						mag_and_pow = battle_action[1].get_mag() + battle_action[4].get_power()
						damage = randint(floor(mag_and_pow*0.9), floor(mag_and_pow*1.35))
						damage -= randint(floor(battle_action[3].get_res()/2), battle_action[3].get_res())
						if battle_action[3].get_defending():
							damage -= randint(floor(battle_action[3].get_res()/2), battle_action[3].get_res())

						battle_action[3].heal(-damage, Stat.HitPoints(0))
						floating_texts.append(Text.FloatingText(battle_action[3].get_battle_pos()[0], battle_action[3].get_battle_pos()[1]-16, str(damage), 32, colour, UIConstant.FLOATING_TEXT_FRAMES))
						battle_action[4].sound.play()

					elif battle_action[4].__class__.__bases__[0] == Spell.NerfSpell:
						colour = (255, 255, 0)
						nerf_level = randint(floor(battle_action[4].get_stat_power()*0.9), floor(battle_action[4].get_stat_power()*1.35))
						battle_action[3].buff(-nerf_level, battle_action[4].get_stat_target())
						floating_texts.append(Text.FloatingText(battle_action[3].get_battle_pos()[0], battle_action[3].get_battle_pos()[1]-16, battle_action[4].get_stat_target().upper()+" down.", 32, colour, UIConstant.FLOATING_TEXT_FRAMES))
						Sound.nerf.play()

				try:
					battle_action[3].get_current_hp()
				except:
					pass
				else:
					if battle_action[3].get_current_hp() <= 0:
						if battle_action[3] in enemy_party:
							enemy_party.remove_member(battle_action[3])
							experience_pool += battle_action[3].get_death_exp()
						else:
							battle_action[3].heal(-battle_action[3].get_current_hp(), Stat.HitPoints(0))


			#Battle Drawing below (action loop)
			screen.fill((0, 0 ,0))
			screen.blit(BackgroundImage.grass, (0, 0))

			for enemy_party_member in enemy_party:
				screen.blit(enemy_party_member.get_battle_image(), enemy_party_member.get_battle_pos())

			for party_member in party:
				screen.blit(party_member.get_battle_image(), party_member.get_battle_pos())
			
			pygame.draw.rect(screen, UIConstant.BACKGROUND_COLOUR, (screen_size[0]-224, 0, 224, screen_size[1]))
			
			for i in range(len(party.get_members())):
				party_text_colour = (255,255,255)

				Text.draw_text(screen_size[0]-224+32, (i+1)*80 - 40, party[i].get_name(), 24, party_text_colour)
				Text.draw_text(screen_size[0]-244+48, (i+1)*80 - 24, "HP: "+str(party[i].get_current_hp())+"/"+str(party[i].get_hp()), 20, (255,255,255))
				Text.draw_text(screen_size[0]-244+48, (i+1)*80 - 14, "MP: "+str(party[i].get_current_mp())+"/"+str(party[i].get_mp()), 20, (255,255,255))

			for floating_text in floating_texts:
				floating_text.update()
				floating_text.draw()

			pygame.display.flip() #Now you can see the effects
			clock.tick(60)
			time.sleep(0.6)

		'''j = 0
		for i in range(len(enemy_party.get_members())):
			if enemy_party.get_members()[i+j].get_current_hp() <= 0:
				#Dead enemy
				experience_pool += enemy_party.get_members()[i+j].get_death_exp()
				enemy_party.remove_member(enemy_party.get_members()[i+j])
				
				i += 1 #This funny incrementor math allows you to kill multiple enemies at once.
				j -= 1 #I had to do this because the list is shortened when an enemy is killed, which messes up the loop'''

		current_battle_member_index = 0
		battle_actions = []
		menus = [Menu.BattleMenu(party[current_battle_member_index])]

		if len(enemy_party.get_members()) < 1 and len(fragile_textboxes) < 1:
			#Battle won!
			experience_pool = floor(experience_pool/len(party.get_members()))
			for party_member in party:
				party_member.debuff()
				party_member.shift_exp(experience_pool)

			menus = []
			fragile_textboxes.append(Text.TextBox(["Victory! Gained "+str(experience_pool)+" EXP!"], screen_size[0]/2, screen_size[1]/2))
			battle_over = True
			Sound.play_overworld_music("fanfare")

	else:
		menus = [Menu.BattleMenu(party[current_battle_member_index])]

def main():
	done = False
	paused = False
	
	title_screen = True
	
	global main_screen
	main_screen = False
	
	global battle_screen
	battle_screen = False

	global battle_actions
	battle_actions = []

	global battle_over
	battle_over = True

	BACKGROUND_COLOUR = (74,104,200)

	global menus
	menus = []

	global party
	party = Party.Party()
	
	global enemy_party
	enemy_party = Party.Party()
	
	global fragile_textboxes
	fragile_textboxes = [] #Fragile textboxes disappear at a button press
	resiliant_textboxes = [] #Resiliant textboxes don't disappear until some condition is met
	
	global floating_texts
	floating_texts = [] #Floating text ignores inputs and disappears after a certain time. (eg. damage numbers)
	
	main_menu = Menu.MainMenu()
	menus.append(main_menu)

	large_font = pygame.font.Font("resources/fonts/coders_crux.ttf", 80)

	current_map = load_pygame("resources/maps/test_map.tmx")
	party.add_member(Character.CaptainRizzko([750,1450], 1))
	party.add_member(Character.Zirkak([0,0], 50)) #Level 50 for testing purposes
	
	pyscroll_map_data = pyscroll.data.TiledMapData(current_map)
	map_layer = pyscroll.BufferedRenderer(pyscroll_map_data, screen.get_size())
	map_layer.zoom = 2
	pyscroll_group_data = PyscrollGroup(map_layer=map_layer, default_layer=1)
	
	'''for party_member in party.get_members():
		pyscroll_group_data.add(party_member)'''

	pyscroll_group_data.add(party.get_current_member())
						

	logo = pygame.image.load("resources/img/logo.png")

	while not done:# Master gameloop that can contain other gameloops.
		while not done and title_screen:# Gameloop that runs while on the title screen of the game
			title_screen_events = pygame.event.get()

			for title_screen_event in title_screen_events:
				#Event handling 
				if title_screen_event.type == pygame.QUIT:
					done = True
				if title_screen_event.type == pygame.MOUSEBUTTONDOWN and False:
					if title_screen_event.button == 1:
						if quit_button.hovered == True:
							done = True
						if play_button.hovered == True:
							title_screen = False
							main_screen = True

				if title_screen_event.type == pygame.KEYDOWN:
					if title_screen_event.key == K_UP:
						menus[-1].move_selection_up()
					if title_screen_event.key == K_DOWN:
						menus[-1].move_selection_down()
					if title_screen_event.key == K_LEFT:
						menus[-1].move_selection_left()
					if  title_screen_event.key == K_RIGHT:
						menus[-1].move_selection_right()
					if title_screen_event.key == K_RETURN or title_screen_event.key == K_x:
						Sound.confirm.play()
						if menus[-1].__class__ == Menu.MainMenu:							
							if menus[-1].get_selected_name() == "New Game":
								menus = []

								walls = []
								warps = []

								for map_object in current_map.objects:
									if map_object.type == "wall":
										walls.append(pygame.Rect(map_object.x, map_object.y, map_object.width, map_object.height))	
									elif map_object.type == "warp":
										warps.append(map_object)

								title_screen = False
								main_screen = True
								Sound.play_overworld_music("sea")

							elif menus[-1].get_selected_name() == "Load Game":
								menus.append(Menu.LoadMenu())
							elif menus[-1].get_selected_name() == "Settings":
								print("TODO: Settings")
							elif menus[-1].get_selected_name() == "Quit":
								done = True
						elif menus[-1].__class__ == Menu.LoadMenu:
							if menus[-1].get_selected_element_position()["x"] == 0:
								gamefile = "0"
							elif menus[-1].get_selected_element_position()["x"] == 1:
								gamefile = "1"
							elif menus[-1].get_selected_element_position()["x"] == 2:
								gamefile = "2"
							try:
								print("\nLoading shelf...")
								loaded_game = shelve.open("savegames/savegame"+gamefile+".sav")
								print("Shelf loaded.\n")
								
								print("Clearing party from group data...")
								'''for party_member in party.get_members():
									pyscroll_group_data.remove(party_member)'''
								pyscroll_group_data.remove(party.get_current_member())
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
								party = loaded_party

								current_map = loaded_map
								current_map = load_pygame("resources/maps/"+loaded_map+".tmx")
								print("Variables assigned.\n")

								print("Generating map objects...")
								walls = []
								warps = []
								for map_object in current_map.objects:
									if map_object.type == "wall":
										walls.append(pygame.Rect(map_object.x, map_object.y, map_object.width, map_object.height))
									elif map_object.type == "warp":
										warps.append(map_object)
								print("Map objects generated.\n")
							
								
								print("Exiting menus...")
								menus = []
								print("Menus exited.\n")

								print("Creating map data...")
								pyscroll_map_data = pyscroll.data.TiledMapData(current_map)
								print("Map data created.\n")

								print("Creating map layer...")
								map_layer = pyscroll.BufferedRenderer(pyscroll_map_data, screen.get_size())
								map_layer.zoom = 2
								print("Map layer created.\n")

								print("Creating group data...")
								pyscroll_group_data = PyscrollGroup(map_layer=map_layer, default_layer=2)
								print("Group data created.\n")
								
								print("Reloading party and item images...")
								for party_member in party.get_members():
									party_member.reload_images()
									party_member.reload_spell_lines()
									party_member.reload_sounds()
									for item in party_member.items:
										item.reload_image()
									for spell in party_member.spells:
										spell.reload_image()
										spell.reload_sound()
								print("Images reloaded.")

								print("Adding party to group data...")
								'''for party_member in party.get_members():
									pyscroll_group_data.add(party_member)'''
								pyscroll_group_data.add(party.get_current_member())
								print("Party added to group data.\n")

								title_screen = False
								main_screen = True

								Sound.play_overworld_music("sea")
							except:
								pass

					if title_screen_event.key == K_z:
						if len(menus) > 1:
							Sound.back.play()
							menus.remove(menus[-1])
							if len(menus) > 0:
								menus[-1].update()

			#Game logic below
			'''for button in buttons:
				button.update()'''

			for menu in menus:
				menu.update()

			#Drawing Below
			screen.fill(BACKGROUND_COLOUR)

			screen.blit(logo, (screen_size[0]/2-logo.get_width()/2, 0))

			'''for button in buttons:
				button.draw()'''

			for menu in menus:
				menu.draw()

			pygame.display.flip()
			clock.tick(60)

		################################################################################################
		################################################################################################
		while main_screen and not done and not paused and not title_screen: # Main gameloop
			for event in pygame.event.get():
				#Event Handling
				if event.type == pygame.QUIT:
					done = True
				if event.type == pygame.KEYDOWN:
					if len(menus) < 1 and len(fragile_textboxes) < 1:
						if event.key == K_q:
							map_layer.zoom = 1.2
						if event.key == K_UP:
							for party_member in party.get_members():
								party_member.velocity[1] = -1
						if event.key == K_DOWN:
							for party_member in party.get_members():
								party_member.velocity[1] = 1
						if event.key == K_LEFT:
							for party_member in party.get_members():
								party_member.velocity[0] = -1
								party_member.frame = 0
						if event.key == K_RIGHT:
							for party_member in party.get_members():
								party_member.velocity[0] = 1
								party_member.frame = 1

						if event.key == K_RETURN:
							if Menu.StartMenu() not in menus:
								menus.append(Menu.StartMenu())
								for party_member in party.get_members():
									party_member.velocity = [0,0]
						if event.key == K_i:
							#This code is important and will initiate a battle. It is run once!
							global current_battle_member_index
							current_battle_member_index = 0

							global experience_pool
							experience_pool = 0

							enemy_party.add_member(Character.Googlyblob([0,0], 1))
							enemy_party.add_member(Character.CocoonMan([0,0], 1))
							enemy_party.add_member(Character.GenericPirate([0,0], 3))
							menus = [Menu.BattleMenu(party[current_battle_member_index])]

							Battle.position_for_battle(party, screen_size[1]-128)
							Battle.position_for_battle(enemy_party, 64)

							Sound.play_battle_music()

							battle_over = False

							battle_screen = True
							main_screen = False

					else:
						
						try:
							fragile_textboxes.remove(fragile_textboxes[-1]) #Remove a textbox if it exists, and do not interact with the menu system
							break
						except:
							pass

						if event.key == K_UP:
							menus[-1].move_selection_up()
						if event.key == K_DOWN:
							menus[-1].move_selection_down()
						if event.key == K_LEFT:
							menus[-1].move_selection_left()
						if  event.key == K_RIGHT:
							menus[-1].move_selection_right()
						if event.key == K_z:
							Sound.back.play()
							menus.remove(menus[-1])
							if len(menus) > 0:
								menus[-1].update()
							if len(resiliant_textboxes) > 0:
								resiliant_textboxes.remove(resiliant_textboxes[-1])

						if event.key == K_x:
							Sound.confirm.play()
							if menus[-1].__class__ == Menu.StartMenu:
								if menus[-1].get_selected_name() == "Party":
									menus.append(Menu.PartyMenu(party))
								elif menus[-1].get_selected_name() == "Items":
									menus.append(Menu.ItemMenu(party.get_current_member().get_items()))
								elif menus[-1].get_selected_name() == "Save":
									menus.append(Menu.SaveMenu())
								elif menus[-1].get_selected_name() == "Pause":
									paused = True
								elif menus[-1].get_selected_name() == "Spells":
									menus.append(Menu.SpellMenu(party.get_current_member().get_spells()))
								elif menus[-1].get_selected_name() == "Quit":
									done = True
								elif menus[-1].get_selected_name() == "Skills":
									print("TODO: Skills.")
								else:
									print("No item was selected. This is a bug.")
							elif menus[-1].__class__ == Menu.SaveMenu:
								if menus[-1].get_selected_element_position()["x"] == 0: #Notice the x position is needed on a vertical list
									gamefile = "0"
								elif menus[-1].get_selected_element_position()["x"] == 1:
									gamefile = "1"
								elif menus[-1].get_selected_element_position()["x"] == 2:
									gamefile = "2"
								else:
									print("Unknown option. Gamefile will not be set. Aborting")
									pygame.quit()
									exit()
									
								print("\nSaving to game "+gamefile+"...")
								print("Loading shelf...\n")
								loaded_game = shelve.open("savegames/savegame"+gamefile+".sav")
								print("Shelf loaded.\n")
								print("Clearing party from group data...")
								'''for party_member in party.get_members():
									pyscroll_group_data.remove(party_member)'''
								pyscroll_group_data.remove(party.get_current_member())
								print("Party cleared from group data.\n")

								print("Clearing party and item images...")
								for member in party.get_members():
									member.clear_images()
									member.clear_spell_lines()
									member.clear_sounds()
									for item in member.items:
										item.clear_image()
									for spell in member.spells:
										spell.clear_image()
								print("Images cleared.")

								print("Saving party...")
								loaded_game["party"] = party
								print("Party saved.\n")

								print("Adding party to group data...")
								'''for party_member in party.get_members():
									pyscroll_group_data.add(party_member)'''
								pyscroll_group_data.add(party.get_current_member())
								print("Party added to group data.\n")

								print("Saving map...")
								loaded_game["map"] = current_map.name
								print("Map saved.\n")
									
								print("Closing shelf...")
								loaded_game.close()
								print("Shelf closed.\n")

								print("Reloading party and item images...")
								for party_member in party.get_members():
									party_member.reload_images()
									party_member.reload_spell_lines()
									party_member.reload_sounds()
									for item in party_member.items:
										item.reload_image()
									for spell in party_member.spells:
										spell.reload_image()
										spell.reload_sound()
								print("Images reloaded.")

								menus.remove(menus[-1])

							elif menus[-1].__class__ == Menu.ItemMenu:
								#Opens the item use menu for the item you've selected
								menus.append(Menu.ItemUseMenu(party.get_current_member().get_items()[menus[-1].get_selected_element_position()["x"]]))

							elif menus[-1].__class__ == Menu.SpellMenu:
								#Opens the spell use menu for the spell you've selected
								menus.append(Menu.SpellUseMenu(party.get_current_member().get_spells()[menus[-1].get_selected_element_position()["x"]]))

							elif menus[-1].__class__ == Menu.ItemUseMenu:
								if menus[-1].get_selected_name() == "Use":
									if party.get_current_member().get_items()[menus[1].get_selected_element_position()["x"]].get_useable():
										#Adds the "use on whom?" menu to the menu list.
										menus.append(Menu.WhomUseMenu(menus[-1].get_item(), party))
									else:
										fragile_textboxes.append(Text.TextBox([party.get_current_member().get_items()[menus[1].get_selected_element_position()["x"]].get_name()+" isn't useable!"],
											menus[-1].get_position()["x"]+menus[-1].get_box_width()+16, menus[-1].get_position()["y"]))

								elif menus[-1].get_selected_name() == "Examine":
									fragile_textboxes.append(Text.TextBox([party.get_current_member().get_items()[menus[1].get_selected_element_position()["x"]].get_description(),
										"","Type: "+party.get_current_member().get_items()[menus[1].get_selected_element_position()["x"]].get_item_type()],
									 menus[-1].get_position()["x"]+menus[-1].get_box_width()+16, menus[-1].get_position()["y"]))
								
								elif menus[-1].get_selected_name() == "Equip": #Equip
									if party.get_current_member().get_items()[menus[1].get_selected_element_position()["x"]].get_equippable():
										print("Equip to whom?")
										menus.append(Menu.WhomEquipMenu(menus[-1].get_item(), party))
									else:
										fragile_textboxes.append(Text.TextBox([party.get_current_member().get_items()[menus[1].get_selected_element_position()["x"]].get_name()+" isn't equippable!"],
											menus[-1].get_position()["x"]+menus[-1].get_box_width()+16, menus[-1].get_position()["y"]))

								elif menus[-1].get_selected_name() == "Discard":
									party.get_current_member().items.remove(menus[-1].get_item())
									menus[1] = Menu.ItemMenu(party.get_current_member().items)
									menus.remove(menus[-1])

							elif menus[-1].__class__ == Menu.SpellUseMenu:
								if menus[-1].get_selected_name() == "Use":
									selected_spell = party.get_current_member().get_spells()[menus[1].get_selected_element_position()["x"]]
									if selected_spell.get_useable_outside_battle():
										menus.append(Menu.WhomSpellMenu(selected_spell, party))
									elif party.get_current_member().get_spells()[menus[1].get_selected_element_position()["x"]].get_useable_in_field():
										print("TODO: Use spells in field.")
									else:
										fragile_textboxes.append(Text.TextBox([menus[-1].get_spell().get_name()+" isn't useable in the field."],
											menus[-1].get_position()["x"]+menus[-1].get_box_width()+16, menus[-1].get_position()["y"]))
								elif menus[-1].get_selected_name() == "Description":
									fragile_textboxes.append(Text.TextBox([party.get_current_member().get_spells()[menus[1].get_selected_element_position()["x"]].get_description(),
										"",menus[-1].get_spell().get_restore_text()],
										menus[-1].get_position()["x"]+menus[-1].get_box_width()+16, menus[-1].get_position()["y"]))


							elif menus[-1].__class__ == Menu.PartyMenu:
								#Opens the party use menu for the party member you've selected
								menus.append(Menu.PartyUseMenu(party[menus[-1].get_selected_element_position()["x"]]))

							elif menus[-1].__class__ == Menu.PartyUseMenu:
								if menus[-1].get_selected_name() == "Status":
									selected_party_member = party[menus[1].get_selected_element_position()["x"]]
									fragile_textboxes.append(Text.TextBox(
										
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
										"EXP: "+str(selected_party_member.get_exp())+"/"+str(selected_party_member.get_exp_to_next())],

										menus[-1].get_position()["x"]+menus[-1].get_box_width()+16, menus[-1].get_position()["y"]))

								elif menus[-1].get_selected_name() == "Select":
									pyscroll_group_data.remove(party.get_current_member())
									party.set_stored_pos(party.get_current_member().get_pos())
									party.set_current_member(party[menus[1].get_selected_element_position()["x"]])
									party.get_current_member().set_pos(party.get_stored_pos())
									pyscroll_group_data.add(party.get_current_member())

								elif menus[-1].get_selected_name() == "Unequip":
									equipped_items = []
									if party[menus[1].get_selected_element_position()["x"]].get_weapon():
										equipped_items.append(party[menus[1].get_selected_element_position()["x"]].get_weapon())
									if party[menus[1].get_selected_element_position()["x"]].get_armour():
										equipped_items.append(party[menus[1].get_selected_element_position()["x"]].get_armour())
									if party[menus[1].get_selected_element_position()["x"]].get_shield():
										equipped_items.append(party[menus[1].get_selected_element_position()["x"]].get_shield())
									if party[menus[1].get_selected_element_position()["x"]].get_accessory():
										equipped_items.append(party[menus[1].get_selected_element_position()["x"]].get_accessory())
									
									if len(equipped_items) > 0:
										menus.append(Menu.UnequipMenu(equipped_items))
									else:
										fragile_textboxes.append(Text.TextBox([party[menus[1].get_selected_element_position()["x"]].get_name()+" has nothing equipped."],
											menus[-1].get_position()["x"]+menus[-1].get_box_width()+16, menus[-1].get_position()["y"]))

							elif menus[-1].__class__ == Menu.WhomUseMenu:
								if menus[-1].get_item().__class__.__bases__[0] == Item.Medicine:
									party[menus[-1].get_selected_element_position()["x"]].heal(menus[-1].get_item().get_value(), menus[-1].get_item().get_stat())
									party.get_current_member().items.remove(menus[-1].get_item())
									menus[1] = Menu.ItemMenu(party.get_current_member().items)
									menus.remove(menus[-1])
									menus.remove(menus[-1])

							elif menus[-1].__class__ == Menu.WhomSpellMenu:
								if party.get_current_member().get_current_mp() < menus[-1].get_spell().get_mp_cost():
									fragile_textboxes.append(Text.TextBox(["Not enough MP!"],
										menus[-1].get_position()["x"]+menus[-1].get_box_width()+16, menus[-1].get_position()["y"]))
								else:
									party.get_current_member().shift_current_mp(-(menus[-1].get_spell().get_mp_cost()))
									
									if menus[-1].get_spell().__class__.__bases__[0] == Spell.HealingSpell:
										party.get_members()[menus[-1].get_selected_element_position()["x"]].heal((menus[-1].get_spell().get_power()), Stat.HitPoints(-(menus[-1].get_spell().get_power())))

							elif menus[-1].__class__ == Menu.WhomEquipMenu:
								party[menus[-1].get_selected_element_position()["x"]].equip(menus[-1].get_item())
								party.get_current_member().items.remove(menus[-1].get_item())
								menus[1] = Menu.ItemMenu(party.get_current_member().items)
								menus.remove(menus[-1])
								menus.remove(menus[-1])

							elif menus[-1].__class__ == Menu.UnequipMenu:
								party[menus[1].get_selected_element_position()["x"]].items.append(equipped_items[menus[-1].get_selected_element_position()["x"]])
								party[menus[1].get_selected_element_position()["x"]].unequip(equipped_items[menus[-1].get_selected_element_position()["x"]])
								menus.remove(menus[-1])

				if event.type == pygame.KEYUP:
					if event.key == K_q:
						map_layer.zoom = 2
					if event.key == K_UP and party.get_current_member().velocity[1] < 0:
						for party_member in party.get_members():
							party_member.velocity[1] = 0
					if event.key == K_DOWN and party.get_current_member().velocity[1] > 0:
						for party_member in party.get_members():
							party_member.velocity[1] = 0
					if event.key == K_LEFT and party.get_current_member().velocity[0] < 0:
						for party_member in party.get_members():
							party_member.velocity[0] = 0
					if event.key == K_RIGHT and party.get_current_member().velocity[0] > 0:
						for party_member in party.get_members():
							party_member.velocity[0] = 0

			#Game Logic Below
			pyscroll_group_data.update()

			for party_member in party.get_members():
				#Handles interaction with map objects!
				for wall in walls:
					if pygame.Rect.colliderect(party_member.feetrect, wall):
						party_member.move_back()
				for warp in warps:
					if pygame.Rect.colliderect(party_member.feetrect, pygame.Rect(warp.x, warp.y, warp.width, warp.height)):
						current_map = load_pygame("resources/maps/"+warp.destination+".tmx")
						party_member.set_pos([int(warp.xwarp), int(warp.ywarp)])

						'''for party_member in party.get_members():
							pyscroll_group_data.remove(party_member)'''
						pyscroll_group_data.remove(party.get_current_member())

						pyscroll_map_data = pyscroll.data.TiledMapData(current_map)

						map_layer = pyscroll.BufferedRenderer(pyscroll_map_data, screen.get_size())
						map_layer.zoom = 2

						pyscroll_group_data = PyscrollGroup(map_layer=map_layer, default_layer=2)

						walls = []
						warps = []

						for map_object in current_map.objects:
							if map_object.type == "wall":
								walls.append(pygame.Rect(map_object.x, map_object.y, map_object.width, map_object.height))	
							elif map_object.type == "warp":
								warps.append(map_object)

						pyscroll_group_data.add(party.get_current_member())

			for menu in menus:
				menu.update()


			#Drawing Below
			screen.fill((255, 0, 255))
			
			pyscroll_group_data.draw(screen)
			pyscroll_group_data.center(party.get_current_member().rect.center)

			#Draws menus
			for menu in menus:
				menu.draw()

			for textbox in fragile_textboxes:
				textbox.draw()

			for textbox in resiliant_textboxes:
				textbox.draw()

			pygame.display.flip()
			clock.tick(60)

		while not done and battle_screen:
			if party.get_members()[current_battle_member_index].get_current_hp() <= 0:
				confirm_action("Nothing", party[current_battle_member_index])

			for battle_event in pygame.event.get():
				#Battle event handling
				if battle_event.type == pygame.QUIT:
					done = True
				if battle_event.type == pygame.KEYDOWN:
					if len(fragile_textboxes) > 0:
						fragile_textboxes.remove(fragile_textboxes[-1])
						if battle_over:
							battle_screen = False
							main_screen = True
							enemy_party.set_members([])
							menus = []
							floating_texts = []
							Sound.play_overworld_music("sea")

					elif battle_event.key == K_x:
						if len(menus) > 0:
							Sound.confirm.play()
							if menus[-1].__class__ == Menu.BattleMenu:
								if menus[-1].get_selected_name() == "Attack":
									menus.append(Menu.BattleTargetMenu(enemy_party.get_members(), menus[-1].get_user(), "Attack"))

								elif menus[-1].get_selected_name() == "Spells":
									menus.append(Menu.SpellMenu(menus[-1].get_user().get_spells()))

								elif menus[-1].get_selected_name() == "Defend":
									#Defend
									confirm_action("Defend", party[current_battle_member_index])

								elif menus[-1].get_selected_name() == "Run":
									#This block sets the party speeds to the speed of their slowest member.
									party_speed = False
									for party_member in party:
										if not party_speed:
											party_speed = party_member.get_spd()
										elif party_member.get_spd() < party_speed:
											party_speed = party_member.get_spd()

									enemy_party_speed = False
									for enemy_party_member in enemy_party:
										if not enemy_party_speed:
											enemy_party_speed = enemy_party_member.get_spd()
										elif enemy_party_member.get_spd() < enemy_party_speed:
											enemy_party_speed = enemy_party_member.get_spd()

									#If your party is faster, you get away.
									if party_speed > enemy_party_speed: 
										battle_screen = False
										main_screen = True
										#Clears enemy party
										enemy_party.set_members([])
										menus = []
										fragile_textboxes.append(Text.TextBox(["You ran away..."], screen_size[0]/2, screen_size[1]/2))
										battle_over = True
									else:
										fragile_textboxes.append(Text.TextBox(["You couldn't get away!"], screen_size[0]/2, screen_size[1]/2))
										confirm_action("Nothing", party[current_battle_member_index])

							elif menus[-1].__class__ == Menu.SpellMenu:
								selected_spell = party[current_battle_member_index].get_spells()[menus[-1].get_selected_element_position()["x"]]

								if party[current_battle_member_index].get_current_mp() >= selected_spell.get_mp_cost():
									if selected_spell.get_targeting() == "self":
										confirm_action("Spell", party[current_battle_member_index], party[current_battle_member_index], selected_spell)

									elif selected_spell.get_targeting() == "friendly":
										menus.append(Menu.BattleTargetMenu(party.get_members(), menus[0].get_user(), "Spell", selected_spell, True))

									elif selected_spell.get_targeting() == "enemy":
										menus.append(Menu.BattleTargetMenu(enemy_party.get_members(), menus[0].get_user(), "Spell", selected_spell))

								else:
									fragile_textboxes.append(Text.TextBox(["Not enough MP."], menus[-1].get_position()["x"], menus[-1].get_position()["y"]))
									selected_spell = None

							elif menus[-1].__class__ == Menu.BattleTargetMenu:
								if menus[-2].__class__ == Menu.BattleMenu:
									confirm_action("Attack", party[current_battle_member_index], enemy_party[menus[-1].get_selected_element_position()["x"]])
							
								elif menus[-2].__class__ == Menu.SpellMenu:
									if menus[-1].get_friendly() == True:
										confirm_action("Spell", party[current_battle_member_index], party[menus[-1].get_selected_element_position()["x"]], menus[-1].get_spell())
									else:
										confirm_action("Spell", party[current_battle_member_index], enemy_party[menus[-1].get_selected_element_position()["x"]], menus[-1].get_spell())

					if battle_event.key == K_z:
						if len(menus) > 0:
							Sound.back.play()
							if menus[-1].__class__ != Menu.BattleMenu:
								menus.remove(menus[-1])
							else:
								pass

					if battle_event.key == K_UP:
						if len(menus) > 0:
							menus[-1].move_selection_up()
					if battle_event.key == K_DOWN:
						if len(menus) > 0:
							menus[-1].move_selection_down()
					if battle_event.key == K_LEFT:
						if len(menus) > 0:
							menus[-1].move_selection_left()
					if  battle_event.key == K_RIGHT:
						if len(menus) > 0:
							menus[-1].move_selection_right()

			#Battle logic below
			for menu in menus:
				menu.update()

			for floating_text in floating_texts:
				floating_text.update()
				if floating_text.age > floating_text.lifetime:
					floating_texts.remove(floating_text)

			#Battle Drawing below
			screen.fill((0, 0 ,0))
			screen.blit(BackgroundImage.grass, (0, 0))

			for enemy_party_member in enemy_party:
				screen.blit(enemy_party_member.get_battle_image(), enemy_party_member.get_battle_pos())

			for party_member in party:
				screen.blit(party_member.get_battle_image(), party_member.get_battle_pos())

			for floating_text in floating_texts:
				floating_text.draw()

			for menu in menus:
				menu.draw()

			for textbox in fragile_textboxes:
				textbox.draw()

			pygame.draw.rect(screen, UIConstant.BACKGROUND_COLOUR, (screen_size[0]-224, 0, 224, screen_size[1]))
			
			for i in range(len(party.get_members())):
				party_text_colour = (255,255,255)
				hp_text_colour = (255, 255, 255)
				if party[i] == party[current_battle_member_index]:
					party_text_colour = (255, 255, 0)
				if party[i].get_current_hp() <= party[i].get_hp()/10:
					hp_text_colour = (255, 128, 0)				
				if party[i].get_current_hp() <= 0:
					hp_text_colour = (255, 0, 0)

				Text.draw_text(screen_size[0]-224+32, (i+1)*80 - 40, party[i].get_name(), 24, party_text_colour)
				Text.draw_text(screen_size[0]-244+48, (i+1)*80 - 24, "HP: "+str(party[i].get_current_hp())+"/"+str(party[i].get_hp()), 20, hp_text_colour)
				Text.draw_text(screen_size[0]-244+48, (i+1)*80 - 14, "MP: "+str(party[i].get_current_mp())+"/"+str(party[i].get_mp()), 20, (255,255,255))

			pygame.display.flip()
			clock.tick(60)

		while not done and paused:# Paused gameloop
			for event in pygame.event.get():
				#Event handling
				if event.type == pygame.QUIT:
					done = True
				if event.type == pygame.KEYDOWN:
					if event.key == K_x:
						paused = False

			#Game logic below
			paused_text = large_font.render("PAUSED",1,(255,255,255))

			#Drawing below
			screen.blit(paused_text, (screen_size[0]/2-paused_text.get_width()/2, screen_size[1]/3))

			pygame.display.flip()
			clock.tick(60)

	pygame.quit()

if __name__ == "__main__":
	pygame.init()
	pygame.font.init()

	screen_size = (900, 700)
	screen = pygame.display.set_mode(screen_size)
	pygame.display.set_caption("Moderately Seafaring")
	clock = pygame.time.Clock()

	main()