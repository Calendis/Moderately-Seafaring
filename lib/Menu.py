#Code for menus
import pygame
screen = pygame.display.set_mode()

from lib import Text
from lib import UIConstant
from lib import Character
from lib import Sound

DEFAULT_COLOUR = UIConstant.FONT_COLOUR
BACKGROUND_COLOUR = UIConstant.BACKGROUND_COLOUR
SCREEN_SIZE = (900, 700)

def limit_colour_255(c):
	if c.__class__ != tuple:
		raise TypeError("Must pass tuple to limit_colour_255.")
	if len(c) != 3:
		raise ValueError("Tuple must be of length 3.")
	new_colour = []
	for v in c:
		if v > 255:
			new_colour.append(255)
		else:
			new_colour.append(v)
	return(new_colour[0], new_colour[1], new_colour[2])

class Menu(object):
	"""Easy-to-use Menu system for pygame.

		Initialize a menu according to the arguments in the init function (duh!)
		Use the move_selection functions based on user keystrokes. This will change the current menu selection.
		Getting the current menu selection is easy! get_selected will return the element, and get_selected_name will return its text!

	"""
	def __init__(self, x, y, width, height, elements, box_width=False, box_height=False, y_spacing_multiplier=1, additional_top_buffer=0, background_colour=BACKGROUND_COLOUR):
		#Error handling to make sure valid arguments are used.
		if elements.__class__ != list:
			raise TypeError("Elements must be passed in in a list!")
		if len(elements) < 1:
			raise ValueError("Menu cannot have fewer than one element!")
		for element in elements:
			if element.__class__ != MenuItem:
				raise TypeError("Menu elements must be of type "+str(MenuItem))
		if len(elements) > width*height:
			raise ValueError(str(len(elements))+" elements cannot fit into a "+str(width)+" by "+str(height)+" grid!")
		
		super(Menu, self).__init__()
		
		self.position = {"x": x, "y": y}
		self.menu_list = []
		self.width = width
		self.height = height
		self.elements = elements
		self.x_selected_element = 0
		self.y_selected_element = 0
		self.font_size = UIConstant.MENU_FONT_SIZE
		self.box_width = box_width
		self.box_height = box_height
		self.y_spacing_multiplier = y_spacing_multiplier
		self.additional_top_buffer = additional_top_buffer
		if self.width > 1:
			self.centred_text_value = 0
		else:
			self.centred_text_value = 1

		strlen_elements = []
		for element in elements:
			strlen_elements.append(len(element.get_text()))

		longest_text_string = elements[strlen_elements.index(max(strlen_elements))].get_text()
		self.longest_text_rendered = Text.sized_font(self.font_size).render(longest_text_string, 1, (0,0,0))

		self.background_colour = background_colour

		if self.box_width:
			self.xspacing = self.box_width//self.width
			self.centred_text_value = 0
		else:
			self.box_width = ((self.longest_text_rendered.get_width())*self.width)+UIConstant.MENU_LEFT_BUFFER*2
			self.xspacing = self.longest_text_rendered.get_width()

		if not self.box_height:
			self.box_height = self.longest_text_rendered.get_height()*self.height + UIConstant.MENU_TOP_BUFFER

		for i in range(self.height):
			self.menu_list.append([])

		self.listcounter = 0
		for element in self.elements:
			if len(self.menu_list[self.listcounter]) >= self.width:
				self.listcounter += 1
			self.menu_list[self.listcounter].append(element)

	def update(self):
		for element in self.elements:
			element.set_colour(element.get_original_colour())
			element.selected = False

		self.menu_list[self.x_selected_element][self.y_selected_element].set_colour(self.menu_list[self.x_selected_element][self.y_selected_element].get_selected_colour())
		self.menu_list[self.x_selected_element][self.y_selected_element].selected = True

	def draw(self, surface): #This draws the menu and menu elements. It's hard to explain.
				
		# This first part draws the box around the menu
		pygame.draw.rect(surface, self.background_colour, ((self.position["x"], self.position["y"]), (self.box_width, self.box_height+UIConstant.MENU_TOP_BUFFER)))

		menu_list_counter = -1
		menu_element_counter = -1
		for menu_element_list in self.get_menu_list():
			menu_list_counter += 1
			menu_element_counter = -1
			for menu_element in menu_element_list:
				menu_element_counter += 1
				menu_element_text = Text.sized_font(self.font_size).render(menu_element.get_text(), 1, menu_element.get_colour())
				
				# The important bit
				surface.blit(menu_element_text, (self.get_position()["x"]+(self.get_xspacing()*menu_element_counter)+UIConstant.MENU_LEFT_BUFFER+self.centred_text_value*(self.get_xspacing()-menu_element_text.get_width())/2,
					self.get_position()["y"]+(menu_list_counter*self.longest_text_rendered.get_height()*self.y_spacing_multiplier)+(UIConstant.MENU_TOP_BUFFER+self.additional_top_buffer)))

				# Draws the image associated with the menu option
				if menu_element.get_image():
					surface.blit(menu_element.get_image(), (self.get_position()["x"]+UIConstant.MENU_IMAGE_LEFT_BUFFER,
						self.get_position()["y"]+(menu_list_counter*self.longest_text_rendered.get_height()*self.y_spacing_multiplier)+(UIConstant.MENU_IMAGE_TOP_BUFFER+self.additional_top_buffer+UIConstant.MENU_IMAGE_SHIFT)))

		# Draws the menu borders
		pygame.draw.rect(surface, UIConstant.MENU_UPPER_BORDER_COLOUR, ((self.get_position()["x"]-UIConstant.MENU_BORDER_WIDTH, self.get_position()["y"]-UIConstant.MENU_BORDER_WIDTH), (self.box_width+2*UIConstant.MENU_BORDER_WIDTH, UIConstant.MENU_BORDER_WIDTH)))
		pygame.draw.rect(surface, UIConstant.MENU_RIGHT_BORDER_COLOUR, ((self.get_position()["x"]+self.box_width, self.get_position()["y"]), (UIConstant.MENU_BORDER_WIDTH, self.box_height+UIConstant.MENU_BORDER_BUFFER+UIConstant.MENU_BORDER_WIDTH)))
		pygame.draw.rect(surface, UIConstant.MENU_LOWER_BORDER_COLOUR, ((self.get_position()["x"]+self.box_width, self.get_position()["y"]+UIConstant.MENU_BORDER_BUFFER+self.box_height), (-self.box_width+1, UIConstant.MENU_BORDER_WIDTH)))
		pygame.draw.rect(surface, UIConstant.MENU_LEFT_BORDER_COLOUR, ((self.get_position()["x"]-UIConstant.MENU_BORDER_WIDTH, self.get_position()["y"]+self.box_height+UIConstant.MENU_BORDER_BUFFER+UIConstant.MENU_BORDER_WIDTH-1), (UIConstant.MENU_BORDER_WIDTH, -self.box_height-UIConstant.MENU_BORDER_BUFFER-UIConstant.MENU_BORDER_WIDTH+1)))

		# Draws the box width and height for debugging/menu aligning purposes
		'''Text.draw_text(surface, self.get_position()["x"]+30, self.get_position()["y"], str(self.get_box_width()), UIConstant.LARGE_FONT_SIZE, (255, 0, 0))
		Text.draw_text(surface, self.get_position()["x"]+30, self.get_position()["y"]+30, str(self.box_height), UIConstant.LARGE_FONT_SIZE, (255, 0, 0))'''

	def move_selection_right(self):
		if self.y_selected_element < self.width-1:
			self.y_selected_element += 1

		try:
			self.menu_list[self.x_selected_element][self.y_selected_element]
		except:
			self.y_selected_element -= 1

	def move_selection_left(self):
		if self.y_selected_element > 0:
			self.y_selected_element -= 1

	def move_selection_down(self):
		if self.x_selected_element < self.height-1:
			self.x_selected_element += 1

		try:
			self.menu_list[self.x_selected_element][self.y_selected_element]
		except:
			self.x_selected_element -= 1

	def move_selection_up(self):
		if self.x_selected_element > 0:
			self.x_selected_element -= 1

	def get_selected_name(self):
		for element in self.elements:
			if element.selected == True:
				return element.get_text()

	def get_position(self):
		return self.position

	def get_xspacing(self):
		return self.xspacing

	def get_menu_list(self):
		return self.menu_list

	def get_selected_element_position(self):
		return({"x":self.x_selected_element, "y": self.y_selected_element})

	def get_box_width(self):
		return self.box_width

	def shift_position(self, rel_x, rel_y):
		self.position["x"] += rel_x
		self.position["y"] += rel_y

	def centre_x(self, multiplier=1):
		self.shift_position(-self.get_box_width()*multiplier/2, 0)

	def centre_y(self):
		self.shift_position(0, -self.box_height/2)

	def move_width_back(self):
		self.shift_position(-self.get_box_width(), 0)

class MenuItem(object):
	"""docstring for MenuItem"""
	def __init__(self, text, image, colour=DEFAULT_COLOUR):
		super(MenuItem, self).__init__()

		self.text = str(text)
		self.colour = colour
		self.original_colour = colour
		self.selected_colour = UIConstant.MENU_SELECTED_COLOUR

		self.image = image
		self.selected = False
		
	def get_text(self):
		return self.text

	def get_colour(self):
		return self.colour

	def get_selected_colour(self):
		return self.selected_colour

	def get_original_colour(self):
		return self.original_colour

	def get_image(self):
		if self.image:
			return self.image
		else:
			return False

	def set_colour(self, new_colour):
		self.colour = new_colour

	def set_text(self, new_text):
		self.text = new_text

class BasicMenuItem(MenuItem):
	"""docstring for BasicMenuItem"""
	def __init__(self, text, colour=DEFAULT_COLOUR):
		self.colour = colour
		self.image = False
		self.text = text
		super(BasicMenuItem, self).__init__(self.text, self.image, self.colour)
		self.__class__ = MenuItem


class MainMenu(Menu):
	"""docstring for MainMenu"""
	def __init__(self):
		
		self.elements = [
			BasicMenuItem("New Game"),
			BasicMenuItem("Load Game"),
			BasicMenuItem("Settings"),
			BasicMenuItem("Quit")
		]

		super(MainMenu, self).__init__(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2, 1, len(self.elements), self.elements)
		self.centre_x()
		self.centre_y()

class StartMenu(Menu):
	"""docstring for StartMenu"""
	def __init__(self):
		
		self.elements = [
			BasicMenuItem("Items"),
			BasicMenuItem("Party"),
			BasicMenuItem("Spells"),
			BasicMenuItem("Traits"),
			BasicMenuItem("Save"),
			BasicMenuItem("Pause"),
			BasicMenuItem("Quit")
		]

		super(StartMenu, self).__init__(UIConstant.MENU_SPACING+UIConstant.MENU_BORDER_WIDTH, SCREEN_SIZE[1]-(3*UIConstant.FONT_SIZE)-2*UIConstant.MENU_TOP_BUFFER-1, len(self.elements)/2, 2, self.elements, SCREEN_SIZE[0]-4*(UIConstant.MENU_LEFT_BUFFER))
		
file_elements = [
	BasicMenuItem("File 1"),
	BasicMenuItem("File 2"),
	BasicMenuItem("File 3")
]

class SaveMenu(Menu):
	"""docstring for SaveMenu"""
	def __init__(self):
		super(SaveMenu, self).__init__(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2, 1, len(file_elements), file_elements)
		self.centre_x()
		self.centre_y()

class LoadMenu(Menu):
	"""docstring for LoadMenu"""
	def __init__(self):
		super(LoadMenu, self).__init__(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2+100, 1, len(file_elements), file_elements)
		self.centre_x()
		self.centre_y()

class ItemMenu(Menu):
	"""docstring for ItemMenu"""
	def __init__(self, items):
		item_elements = []
		for item in items:
			item_elements.append(MenuItem(item.get_name(), item.get_image()))
		super(ItemMenu, self).__init__(UIConstant.MENU_SPACING+UIConstant.MENU_BORDER_WIDTH, UIConstant.MENU_SPACING+UIConstant.MENU_BORDER_WIDTH, 1, len(item_elements), item_elements, 240, SCREEN_SIZE[1]-(50+(4*(UIConstant.MENU_SPACING+UIConstant.MENU_BORDER_WIDTH))), 1.4, 4)

class SpellMenu(Menu):
	"""docstring for SpellMenu"""
	def __init__(self, spells):
		spell_elements = []
		for spell in spells:
			spell_elements.append(MenuItem(spell.get_name(), spell.get_image()))
		super(SpellMenu, self).__init__(UIConstant.MENU_SPACING+UIConstant.MENU_BORDER_WIDTH, UIConstant.MENU_SPACING+UIConstant.MENU_BORDER_WIDTH, 1, len(spell_elements), spell_elements, 240, SCREEN_SIZE[1]-(50+(4*(UIConstant.MENU_SPACING+UIConstant.MENU_BORDER_WIDTH))), 1.4, 4)

class PartyMenu(Menu):
	"""docstring for PartyMenu"""
	def __init__(self, party):
		party_elements = []
		for member in party.get_members():
			party_elements.append(BasicMenuItem(member.get_name()))
		super(PartyMenu, self).__init__(UIConstant.MENU_SPACING+UIConstant.MENU_BORDER_WIDTH, UIConstant.MENU_SPACING+UIConstant.MENU_BORDER_WIDTH, 1, len(party_elements), party_elements, 240, SCREEN_SIZE[1]-(50+(4*(UIConstant.MENU_SPACING+UIConstant.MENU_BORDER_WIDTH))), 1, 4)

itemuse_elements = [
	BasicMenuItem("Use"),
	BasicMenuItem("Examine"),
	BasicMenuItem("Equip"),
	BasicMenuItem("Give"),
	BasicMenuItem("Discard"),
]

class ItemUseMenu(Menu):
	"""docstring for ItemUseMenu"""
	def __init__(self, item):
		self.item = item
		super(ItemUseMenu, self).__init__(281, UIConstant.MENU_SPACING+UIConstant.MENU_BORDER_WIDTH, 1, len(itemuse_elements), itemuse_elements)

	def get_item(self):
		return self.item

spelluse_elements = [
	BasicMenuItem("Use"),
	BasicMenuItem("Description")
]

class SpellUseMenu(Menu):
	"""docstring for SpellUseMenu"""
	def __init__(self, spell):
		self.spell = spell
		super(SpellUseMenu, self).__init__(281, UIConstant.MENU_SPACING+UIConstant.MENU_BORDER_WIDTH, 1, len(spelluse_elements), spelluse_elements)

	def get_spell(self):
		return self.spell
		

class WhomUseMenu(Menu):
	"""docstring for WhomUseMenu"""
	def __init__(self, item, party):
		self.item = item
		whomuse_elements = []
		for party_member in party.get_members():
			whomuse_elements.append(BasicMenuItem(party_member.get_name()))
		super(WhomUseMenu, self).__init__(362, UIConstant.MENU_SPACING+UIConstant.MENU_BORDER_WIDTH, 1, len(whomuse_elements), whomuse_elements)

	def get_item(self):
		return self.item

class WhomSpellMenu(Menu):
	"""docstring for WhomSpellMenu"""
	def __init__(self, spell, party):
		self.spell = spell
		whomspell_elements = []
		for party_member in party.get_members():
			whomspell_elements.append(BasicMenuItem(party_member.get_name()))
		super(WhomSpellMenu, self).__init__(362, UIConstant.MENU_SPACING+UIConstant.MENU_BORDER_WIDTH, 1, len(whomspell_elements), whomspell_elements)

	def get_spell(self):
		return self.spell
		

class WhomEquipMenu(Menu):
	"""docstring for WhomEquipMenu"""
	def __init__(self, item, party):
		self.item = item
		whomequip_elements = []
		for party_member in party.get_members():
			whomequip_elements.append(BasicMenuItem(party_member.get_name()))
		super(WhomEquipMenu, self).__init__(362, UIConstant.MENU_SPACING+UIConstant.MENU_BORDER_WIDTH, 1, len(whomequip_elements), whomequip_elements)

	def get_item(self):
		return self.item

partyuse_elements = [
	BasicMenuItem("Status"),
	BasicMenuItem("Select"),
	BasicMenuItem("Unequip")
]		

class PartyUseMenu(Menu):
	"""docstring for PartyUseMenu"""
	def __init__(self, party_member):
		super(PartyUseMenu, self).__init__(281, UIConstant.MENU_SPACING+UIConstant.MENU_BORDER_WIDTH, 1, len(partyuse_elements), partyuse_elements)
	
	def get_party_member(self):
		return party_member

class UnequipMenu(Menu):
	"""docstring for UnequipMenu"""
	def __init__(self, items):
		unequip_elements = []
		for item in items:
			unequip_elements.append(BasicMenuItem(item.get_name()))
		super(UnequipMenu, self).__init__(362, UIConstant.MENU_SPACING+UIConstant.MENU_BORDER_WIDTH, 1, len(unequip_elements), unequip_elements)

battle_elements = [
	BasicMenuItem("Attack"),
	BasicMenuItem("Spells"),
	BasicMenuItem("Defend"),
	BasicMenuItem("Item"),
	BasicMenuItem("Run")
]

class BattleMenu(Menu):
	"""docstring for BattleMenu"""
	def __init__(self, user):
		super(BattleMenu, self).__init__(UIConstant.MENU_SPACING+UIConstant.MENU_BORDER_WIDTH, SCREEN_SIZE[1]-56, len(battle_elements), 1, battle_elements, SCREEN_SIZE[0]-224-32)
		self.user = user

	def get_user(self):
		return self.user

class BattleTargetMenu(Menu):
	"""docstring for BattleTargetMenu"""
	def __init__(self, targets, user, selected_option, spell=False, friendly=False):
		self.targets_elements = []
		for target in targets:
			self.targets_elements.append(BasicMenuItem(target.get_name()))
		super(BattleTargetMenu, self).__init__(128+UIConstant.MENU_SPACING+UIConstant.MENU_BORDER_WIDTH, UIConstant.MENU_SPACING+UIConstant.MENU_BORDER_WIDTH, 1, len(targets), self.targets_elements, 128)
		self.targets = targets
		self.user = user
		self.selected_option = selected_option
		self.spell = spell
		self.friendly = friendly

	def get_friendly(self):
		return self.friendly

	def get_spell(self):
		return self.spell		