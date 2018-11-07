# Useful stuff related to pygame text rendering

import pygame
from lib import UIConstant

import time
from random import randint

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
			self.height = len(self.text)*(self.longest_text_rendered.get_height())+2*UIConstant.MENU_TOP_BUFFER

	def get_width(self):
		return self.width

	def get_height(self):
		return self.height

	def get_position(self):
		return self.position

	def draw(self, surface):
		pygame.draw.rect(surface, self.box_colour, (self.position["x"], self.position["y"], self.width, self.height))
		
		for line in self.text:
			draw_text(surface, self.position["x"]+UIConstant.MENU_LEFT_BUFFER,
				self.position["y"]*(self.text.index(line)+1)+UIConstant.MENU_TOP_BUFFER,
				line, UIConstant.FONT_SIZE, self.text_colour)

		pygame.draw.rect(surface, UIConstant.MENU_UPPER_BORDER_COLOUR, ((self.get_position()["x"]-UIConstant.MENU_BORDER_WIDTH, self.get_position()["y"]-UIConstant.MENU_BORDER_WIDTH), (self.get_width()+2*UIConstant.MENU_BORDER_WIDTH, UIConstant.MENU_BORDER_WIDTH)))
		pygame.draw.rect(surface, UIConstant.MENU_RIGHT_BORDER_COLOUR, ((self.get_position()["x"]+self.get_width(), self.get_position()["y"]), (UIConstant.MENU_BORDER_WIDTH, self.get_height()+UIConstant.MENU_BORDER_WIDTH)))
		pygame.draw.rect(surface, UIConstant.MENU_LOWER_BORDER_COLOUR, ((self.get_position()["x"]+self.get_width(), self.get_position()["y"]+self.get_height()), (-self.get_width()+1, UIConstant.MENU_BORDER_WIDTH)))
		pygame.draw.rect(surface, UIConstant.MENU_LEFT_BORDER_COLOUR, ((self.get_position()["x"]-UIConstant.MENU_BORDER_WIDTH, self.get_position()["y"]+self.get_height()+UIConstant.MENU_BORDER_WIDTH-1), (UIConstant.MENU_BORDER_WIDTH, -self.get_height()-UIConstant.MENU_BORDER_WIDTH+1)))

	def shift_position(self, rel_x, rel_y):
		self.position["x"] += rel_x
		self.position["y"] += rel_y

	def centre_x(self):
		self.shift_position(-self.get_width()/2, 0)

class DialogueBox(TextBox):
	"""docstring for DialogueBox"""
	def __init__(self, text, x, y, line_delays, text_colour=UIConstant.FOREGROUND_COLOUR, box_colour = UIConstant.BACKGROUND_COLOUR):
		super(DialogueBox, self).__init__(text, x, y, UIConstant.DIALOGUE_WIDTH, UIConstant.DIALOGUE_HEIGHT, text_colour, box_colour)
		self.done_dialogue = False
		self.dialogue_lines = self.text[0].split("\n")
		self.line_delays = line_delays

	def draw(self, surface):
		pygame.draw.rect(surface, self.box_colour, (self.position["x"], self.position["y"], self.width, self.height))

		pygame.draw.rect(surface, UIConstant.MENU_UPPER_BORDER_COLOUR, ((self.get_position()["x"]-UIConstant.MENU_BORDER_WIDTH, self.get_position()["y"]-UIConstant.MENU_BORDER_WIDTH), (self.get_width()+2*UIConstant.MENU_BORDER_WIDTH, UIConstant.MENU_BORDER_WIDTH)))
		pygame.draw.rect(surface, UIConstant.MENU_RIGHT_BORDER_COLOUR, ((self.get_position()["x"]+self.get_width(), self.get_position()["y"]), (UIConstant.MENU_BORDER_WIDTH, self.get_height()+UIConstant.MENU_BORDER_WIDTH)))
		pygame.draw.rect(surface, UIConstant.MENU_LOWER_BORDER_COLOUR, ((self.get_position()["x"]+self.get_width(), self.get_position()["y"]+self.get_height()), (-self.get_width()+1, UIConstant.MENU_BORDER_WIDTH)))
		pygame.draw.rect(surface, UIConstant.MENU_LEFT_BORDER_COLOUR, ((self.get_position()["x"]-UIConstant.MENU_BORDER_WIDTH, self.get_position()["y"]+self.get_height()+UIConstant.MENU_BORDER_WIDTH-1), (UIConstant.MENU_BORDER_WIDTH, -self.get_height()-UIConstant.MENU_BORDER_WIDTH+1)))
		
		if not self.done_dialogue:
			for line in self.dialogue_lines:
				character_in_line = -1
				character_widths = []
				for character in line:
					character_in_line += 1
					draw_text(surface,
						self.position["x"]+UIConstant.MENU_LEFT_BUFFER+sum(character_widths),
						self.position["y"]+UIConstant.FONT_SIZE*(self.dialogue_lines.index(line))+UIConstant.MENU_TOP_BUFFER, 
						character, UIConstant.FONT_SIZE, self.text_colour)
					character_widths.append(get_text_width(character))

					pygame.display.flip()
					time.sleep(randint(UIConstant.LETTER_SCROLL_DELAY_MIN, UIConstant.LETTER_SCROLL_DELAY_MAX)/100)

				print(self.line_delays[self.dialogue_lines.index(line)])
				time.sleep(UIConstant.LINE_SCROLL_DELAY/100 * self.line_delays[self.dialogue_lines.index(line)])

			self.done_dialogue = True

		else:
			for line in self.dialogue_lines:
				draw_text(surface, self.position["x"]+UIConstant.MENU_LEFT_BUFFER,
					self.position["y"]+UIConstant.FONT_SIZE*(self.dialogue_lines.index(line))+UIConstant.MENU_TOP_BUFFER,
					line, UIConstant.FONT_SIZE, self.text_colour)

	def get_done_dialogue(self):
		return self.done_dialogue

	def set_done_dialogue(self, new_done_dialogue):
		self.done_dialogue = new_done_dialogue

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