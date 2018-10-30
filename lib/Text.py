#Useful stuff related to pygame text rendering
import pygame
from lib import UIConstant

pygame.font.init()
font_path = "resources/fonts/advanced_pixel-7.ttf"

#Helper function for rendering and blitting pygame text in one.
def draw_text(surface, x, y, text, size=UIConstant.FONT_SIZE, colour=UIConstant.FONT_COLOUR, antialiased=1):
	rendered_text = sized_font(size).render(text, antialiased, colour)
	surface.blit(rendered_text, (x, y))

	# Draws a box around the text for debug purposes
	# pygame.draw.rect(surface, (0, 0, 255), (x, y, rendered_text.get_width(), rendered_text.get_height()), 1)

def sized_font(x):
	return pygame.font.Font(font_path, x)

def get_text_width(text, size=UIConstant.FONT_SIZE):
	rendered_text = sized_font(size).render(text, 1, UIConstant.FONT_COLOUR)
	return rendered_text.get_width()

def get_text_height(text, size=UIConstant.FONT_SIZE):
	rendered_text = sized_font(size).render(text, 1, UIConstant.FONT_COLOUR)
	return rendered_text.get_height()

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

		
		#Remove None type from the text lines.
		#None will be passed as part of spell descriptions for spells that do not restore any hp
		for item in self.text:
			if item == None:
				self.text.remove(item)

		self.longest_text_rendered = sized_font(UIConstant.FONT_SIZE).render(text[text.index(max(text, key=len))], 1, (0, 0, 0))

		if not self.width:
			self.width = self.longest_text_rendered.get_width()+UIConstant.MENU_LEFT_BUFFER*2

		if not self.height:
			self.height = len(self.text)*(self.longest_text_rendered.get_height())+UIConstant.MENU_TOP_BUFFER

	def get_width(self):
		return self.width

	def get_height(self):
		return self.height

	def get_position(self):
		return self.position

	def draw(self, surface):
		pygame.draw.rect(surface, self.box_colour, (self.position["x"], self.position["y"], self.width, self.height))
		
		for line in self.text:
			draw_text(surface, self.position["x"]+8, self.position["y"]*(self.text.index(line)+1)+8, line, UIConstant.FONT_SIZE, self.text_colour)

		pygame.draw.rect(surface, UIConstant.MENU_UPPER_BORDER_COLOUR, ((self.get_position()["x"]-UIConstant.MENU_BORDER_WIDTH, self.get_position()["y"]-UIConstant.MENU_BORDER_WIDTH), (self.get_width()+2*UIConstant.MENU_BORDER_WIDTH, UIConstant.MENU_BORDER_WIDTH)))
		pygame.draw.rect(surface, UIConstant.MENU_RIGHT_BORDER_COLOUR, ((self.get_position()["x"]+self.get_width(), self.get_position()["y"]), (UIConstant.MENU_BORDER_WIDTH, self.get_height()+UIConstant.MENU_BORDER_WIDTH)))
		pygame.draw.rect(surface, UIConstant.MENU_LOWER_BORDER_COLOUR, ((self.get_position()["x"]+self.get_width(), self.get_position()["y"]+self.get_height()), (-self.get_width()+1, UIConstant.MENU_BORDER_WIDTH)))
		pygame.draw.rect(surface, UIConstant.MENU_LEFT_BORDER_COLOUR, ((self.get_position()["x"]-UIConstant.MENU_BORDER_WIDTH, self.get_position()["y"]+self.get_height()+UIConstant.MENU_BORDER_WIDTH-1), (UIConstant.MENU_BORDER_WIDTH, -self.get_height()-UIConstant.MENU_BORDER_WIDTH+1)))

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
	
	def draw(self, surface):
		draw_text(surface, self.x, self.y, self.text, self.size, self.colour, self.antialiased)