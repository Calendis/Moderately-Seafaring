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

def draw_text(x, y, text, antialiased=1, colour=(0, 0, 0)):
	rendered_text = sized_oxygen_font(15).render(text, antialiased, colour)
	screen.blit(rendered_text, (x, y))

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

	def draw(self):
		pygame.draw.rect(screen, self.box_colour, (self.position["x"], self.position["y"], self.width, self.height))
		
		for line in self.text:
			draw_text(self.position["x"]+8, self.position["y"]*(self.text.index(line)+1)+8, line, 1, self.text_colour)