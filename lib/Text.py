#Useful stuff related to pygame text rendering
import pygame

from lib import UIConstant
from lib import Menu

pygame.font.init()

crux_font_path = "resources/fonts/coders_crux.ttf"
oxygen_font_path = "resources/fonts/Oxygen-Regular.ttf"
oxygen_font = pygame.font.Font(oxygen_font_path, 12)
screen = pygame.display.set_mode()

#Helper function for rendering and blitting pygame text in one.

def draw_text(x, y, text, size=15, colour=(0, 0, 0), surface=screen, antialiased=1):
	rendered_text = sized_oxygen_font(size).render(text, antialiased, colour)
	surface.blit(rendered_text, (x, y))

def sized_oxygen_font(x):
	return pygame.font.Font(crux_font_path, x)

class TextBox():
	"""docstring for TextBox"""
	def __init__(self, text, x, y, width=False, height=False, text_colour=UIConstant.FOREGROUND_COLOUR, box_colour=UIConstant.BACKGROUND_COLOUR):
		super(TextBox, self).__init__()
		self.text = text
		self.position = {"x": x, "y": y}
		self.width = width
		self.height = height
		self.text_colour = text_colour
		self.box_colour = box_colour

		if not self.width:
			self.width = len(self.text[0])*8
		if not self.height:
			self.height = len(self.text)*(16)+16

		#Remove None type from the text lines.
		#None will be passed as part of spell descriptions for spells that do not restore any hp
		for item in self.text:
			if item == None:
				self.text.remove(item)

	def get_width(self):
		return self.width

	def draw(self):
		pygame.draw.rect(screen, self.box_colour, (self.position["x"], self.position["y"], self.width, self.height))
		
		for line in self.text:
			draw_text(self.position["x"]+8, self.position["y"]*(self.text.index(line)+1)+8, line, 15, self.text_colour)

	def shift_position(self, rel_x, rel_y):
		self.position["x"] += rel_x
		self.position["y"] += rel_y

	def centre_x(self):
		self.shift_position(-self.get_width()/2, 0)

class FloatingText():
	"""Lifetime is expressed in frames. The game runs at about 60 FPS I think."""
	def __init__(self, x, y, text, size, colour, lifetime, antialiased=1):
		super(FloatingText, self).__init__()
		self.x = x
		self.y = y
		self.text = text
		self.size = size
		self.colour = colour
		self.lifetime = lifetime
		self.antialiased = antialiased

		self.alive = True
		self.age = 0

	def update(self):
		self.age += 1
	
	def draw(self, surface=screen):
		draw_text(self.x, self.y, self.text, self.size, self.colour, surface, self.antialiased)