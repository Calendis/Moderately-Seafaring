#Code for menus
import pygame
screen = pygame.display.set_mode()

from lib import Text

DEFAULT_COLOUR = (0, 0, 0)
SCREEN_SIZE = (900, 700)

class Menu(object):
	"""Easy-to-use Menu system for pygame.

		Initialize a menu according to the arguments in the init function (duh!)
		Use the move_selection functions based on user keystrokes. This will change the current menu selection.
		Getting the current menu selection is easy! get_selected will return the element, and get_selected_name will return its text!

	"""
	def __init__(self, x, y, width, height, elements, font_size=12):
		#Error handling to make sure valid arguments are used.
		if elements.__class__ != list:
			raise TypeError("Elements must be passed in in a list!")
		if len(elements) == 0:
			raise ValueError("Menu cannot have zero elements!")
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
		self.font_size = font_size

		strlen_elements = []
		for element in elements:
			strlen_elements.append(len(element.get_text()))

		self.xspacing = self.font_size*max(strlen_elements)
		#print(str(self)+"'s xspacing is "+str(self.xspacing))

		self.background_colour = (255, 0, 0)

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

	def draw(self): #This draws the menu and menu elements. It's hard to explain.
				
		menu_list_counter = 0
		menu_element_counter = -1
		for menu_element_list in self.get_menu_list():
			menu_list_counter += 1
			menu_element_counter = -1
			for menu_element in menu_element_list:
				menu_element_counter += 1
				menu_element_text = Text.sized_oxygen_font(self.font_size).render(menu_element.get_text(), 1, menu_element.get_colour())
				
				#The important bit
				screen.blit(menu_element_text, (self.get_position()["x"]+(self.get_xspacing()*menu_element_counter)-(0),
					self.get_position()["y"]+(menu_list_counter*self.font_size)))
				
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

class MenuItem(object):
	"""docstring for MenuItem"""
	def __init__(self, text, colour, image):
		super(MenuItem, self).__init__()

		self.text = str(text)
		self.colour = colour
		self.original_colour = colour
		self.selected_colour = ((255-self.colour[0]), (255-self.colour[1]), (255-self.colour[2]))
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
		return self.image

	def set_colour(self, new_colour):
		self.colour = new_colour

class BasicMenuItem(MenuItem):
	"""docstring for BasicMenuItem"""
	def __init__(self, text):
		self.colour = DEFAULT_COLOUR
		self.image = None
		self.text = text
		super(BasicMenuItem, self).__init__(self.text, self.colour, self.image)
		self.__class__ = MenuItem
		

main_elements = [
	BasicMenuItem("New Game"),
	BasicMenuItem("Load Game"),
	BasicMenuItem("Settings"),
	BasicMenuItem("Quit")
]

class MainMenu(Menu):
	"""docstring for MainMenu"""
	def __init__(self):
		super(MainMenu, self).__init__(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2, 1, len(main_elements), main_elements, 20)

start_elements = [
	BasicMenuItem("Items"),
	BasicMenuItem("Party"),
	BasicMenuItem("Spells"),
	BasicMenuItem("Skills"),
	BasicMenuItem("Save"),
	BasicMenuItem("Pause")
]

class StartMenu(Menu):
	"""docstring for StartMenu"""
	def __init__(self):
		super(StartMenu, self).__init__(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]-64, 3, 2, start_elements, 15)
		
file_elements = [
	BasicMenuItem("File 1"),
	BasicMenuItem("File 2"),
	BasicMenuItem("File 3")
]

class SaveMenu(Menu):
	"""docstring for SaveMenu"""
	def __init__(self):
		super(SaveMenu, self).__init__(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2, 1, len(file_elements), file_elements, 15)

class LoadMenu(Menu):
	"""docstring for LoadMenu"""
	def __init__(self):
		super(LoadMenu, self).__init__(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2+100, 1, len(file_elements), file_elements, 15)

class ItemMenu(Menu):
	"""docstring for ItemMenu"""
	def __init__(self, items):
		item_elements = []
		for item in items:
			item_elements.append(BasicMenuItem(item.get_name()))
		super(ItemMenu, self).__init__(16, SCREEN_SIZE[1]-64, 1, len(item_elements), item_elements, 15)

class PartyMenu(Menu):
	"""docstring for PartyMenu"""
	def __init__(self, party):
		party_elements = []
		for member in party:
			party_elements.append(BasicMenuItem(member.get_name()))
		super(PartyMenu, self).__init__(16, 64, len(party_elements), 1, party_elements, 20)
		