#The gameloop for Moderately Seafaring, an RPG
#4 Dec, 2016

import pygame
from pygame.locals import *

from pytmx.util_pygame import load_pygame

import pyscroll
import pyscroll.data
from pyscroll.group import PyscrollGroup

import shelve

import os.path
import sys

from lib import Character
from lib import Menu
from lib import Text
from lib import Item

def main():
	done = False
	paused = False
	title_screen = True
	main_screen = False

	BACKGROUND_COLOUR = (74,104,200)

	menus = []
	party = []
	fragile_textboxes = [] #Fragile textboxes disappear at a button press
	resiliant_textboxes = [] #Resiliant textboxes don't disappear until some condition is met
	
	main_menu = Menu.MainMenu()
	menus.append(main_menu)

	large_font = pygame.font.Font("resources/fonts/coders_crux.ttf", 80)

	current_map = load_pygame("resources/maps/test_map.tmx")
	hero = Character.CaptainRizzko([1090,1450])
	party.append(hero)
	#party.append(Character.CaptainRizzko([395,10]))
	pyscroll_map_data = pyscroll.data.TiledMapData(current_map)
	map_layer = pyscroll.BufferedRenderer(pyscroll_map_data, screen.get_size())
	map_layer.zoom = 2
	pyscroll_group_data = PyscrollGroup(map_layer=map_layer, default_layer=1)
	
	for party_member in party:
		pyscroll_group_data.add(party_member)
						

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
								for party_member in party:
									pyscroll_group_data.remove(party_member)
								print("Party cleared from group data.\n")

								print("Loading party...")
								loaded_party = loaded_game["party"]
								print("Party loaded.\n")

								'''print("Reloading party images...")
								for party_member in party:
									party_member.reload_images()
								print("Images reloaded.")'''

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
								for party_member in party:
									party_member.reload_images()
									for item in party_member.items:
										item.reload_image()
								print("Images reloaded.")

								print("Adding party to group data...")
								for party_member in party:
									pyscroll_group_data.add(party_member)
								print("Party added to group data.\n")

								title_screen = False
								main_screen = True
							except:
								pass

					if title_screen_event.key == K_z:
						if len(menus) > 1:
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
							for party_member in party:
								party_member.velocity[1] = -party_member.maxspeed
						if event.key == K_DOWN:
							for party_member in party:
								party_member.velocity[1] = party_member.maxspeed
						if event.key == K_LEFT:
							for party_member in party:
								party_member.velocity[0] = -party_member.maxspeed
								party_member.frame = 0
						if event.key == K_RIGHT:
							for party_member in party:
								party_member.velocity[0] = party_member.maxspeed
								party_member.frame = 1

						if event.key == K_RETURN:
							if Menu.StartMenu() not in menus:
								menus.append(Menu.StartMenu())
								for party_member in party:
									party_member.velocity = [0,0]
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
							menus.remove(menus[-1])
							if len(menus) > 0:
								menus[-1].update()
							if len(resiliant_textboxes) > 0:
								resiliant_textboxes.remove(resiliant_textboxes[-1])

						if event.key == K_x:
							if menus[-1].__class__ == Menu.StartMenu:
								if menus[-1].get_selected_name() == "Party":
									menus.append(Menu.PartyMenu(party))
								elif menus[-1].get_selected_name() == "Items":
									menus.append(Menu.ItemMenu(party[0].get_items()))
								elif menus[-1].get_selected_name() == "Save":
									menus.append(Menu.SaveMenu())
								elif menus[-1].get_selected_name() == "Pause":
									paused = True
								elif menus[-1].get_selected_name() == "Spells":
									print("TODO: Spells.")
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
								for party_member in party:
									pyscroll_group_data.remove(party_member)
								print("Party cleared from group data.\n")

								print("Clearing party and item images...")
								for member in party:
									member.clear_images()
									for item in member.items:
										item.clear_image()
								print("Images cleared.")

								print("Saving party...")
								print(party)
								loaded_game["party"] = party
								print("Party saved.\n")

								print("Adding party to group data...")
								for party_member in party:
									pyscroll_group_data.add(party_member)
								print("Party added to group data.\n")

								print("Saving map...")
								loaded_game["map"] = current_map.name
								print("Map saved.\n")
									
								print("Closing shelf...")
								loaded_game.close()
								print("Shelf closed.\n")

								print("Reloading party and item images...")
								for party_member in party:
									party_member.reload_images()
									for item in party_member.items:
										item.reload_image()
								print("Images reloaded.")

								menus.remove(menus[-1])

							elif menus[-1].__class__ == Menu.ItemMenu:
								#Opens the item use menu for the item you've selected
								menus.append(Menu.ItemUseMenu(party[0].get_items()[menus[-1].get_selected_element_position()["x"]]))

							elif menus[-1].__class__ == Menu.ItemUseMenu:
								if menus[-1].get_selected_name() == "Use":
									if party[0].get_items()[menus[1].get_selected_element_position()["x"]].get_useable():
										#Adds the "use on whom?" menu to the menu list.
										menus.append(Menu.WhomUseMenu(menus[-1].get_item(), party))
									else:
										fragile_textboxes.append(Text.TextBox([party[0].get_items()[menus[1].get_selected_element_position()["x"]].get_name()+" isn't useable!"],
											menus[-1].get_position()["x"]+menus[-1].get_box_width()+16, menus[-1].get_position()["y"]))

								elif menus[-1].get_selected_name() == "Examine":
									fragile_textboxes.append(Text.TextBox([party[0].get_items()[menus[1].get_selected_element_position()["x"]].get_description(),
										"","Type: "+party[0].get_items()[menus[1].get_selected_element_position()["x"]].get_item_type()],
									 menus[-1].get_position()["x"]+menus[-1].get_box_width()+16, menus[-1].get_position()["y"]))
								
								elif menus[-1].get_selected_name() == "Equip": #Equip
									if party[0].get_items()[menus[1].get_selected_element_position()["x"]].get_equippable():
										print("Equip to whom?")
										menus.append(Menu.WhomEquipMenu(menus[-1].get_item(), party))
									else:
										fragile_textboxes.append(Text.TextBox([party[0].get_items()[menus[1].get_selected_element_position()["x"]].get_name()+" isn't equippable!"],
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
									print("TODO: Set current party member to "+party[menus[1].get_selected_element_position()["x"]].get_name())

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
									party[0].items.remove(menus[-1].get_item())
									menus[1] = Menu.ItemMenu(party[0].items)
									menus.remove(menus[-1])
									menus.remove(menus[-1])

							elif menus[-1].__class__ == Menu.WhomEquipMenu:
								party[menus[-1].get_selected_element_position()["x"]].equip(menus[-1].get_item())
								party[0].items.remove(menus[-1].get_item())
								menus[1] = Menu.ItemMenu(party[0].items)
								menus.remove(menus[-1])
								menus.remove(menus[-1])

							elif menus[-1].__class__ == Menu.UnequipMenu:
								party[menus[1].get_selected_element_position()["x"]].items.append(equipped_items[menus[-1].get_selected_element_position()["x"]])
								party[menus[1].get_selected_element_position()["x"]].unequip(equipped_items[menus[-1].get_selected_element_position()["x"]])
								menus.remove(menus[-1])

				if event.type == pygame.KEYUP:
					if event.key == K_q:
						map_layer.zoom = 2
					if event.key == K_UP and party[0].velocity[1] < 0:
						for party_member in party:
							party_member.velocity[1] = 0
					if event.key == K_DOWN and party[0].velocity[1] > 0:
						for party_member in party:
							party_member.velocity[1] = 0
					if event.key == K_LEFT and party[0].velocity[0] < 0:
						for party_member in party:
							party_member.velocity[0] = 0
					if event.key == K_RIGHT and party[0].velocity[0] > 0:
						for party_member in party:
							party_member.velocity[0] = 0

			#Game Logic Below
			pyscroll_group_data.update()

			for party_member in party:
				for wall in walls:
					if pygame.Rect.colliderect(party_member.feetrect, wall):
						party_member.move_back()
				for warp in warps:
					if pygame.Rect.colliderect(party_member.feetrect, pygame.Rect(warp.x, warp.y, warp.width, warp.height)):
						current_map = load_pygame("resources/maps/"+warp.destination+".tmx")
						party_member.pos = [int(warp.xwarp), int(warp.ywarp)]

						for party_member in party:
							pyscroll_group_data.remove(party_member)

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

						for party_member in party:
							pyscroll_group_data.add(party_member)

			for menu in menus:
				menu.update()


			#Drawing Below
			screen.fill((255, 0, 255))
			
			pyscroll_group_data.draw(screen)
			pyscroll_group_data.center(party[0].rect.center)

			#Draws menus
			for menu in menus:
				menu.draw()

			for textbox in fragile_textboxes:
				textbox.draw()

			for textbox in resiliant_textboxes:
				textbox.draw()

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
				#screen.blit(paused_outline, (screen_size[0]/2-paused_outline.get_width()/2, screen_size[1]/3))
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