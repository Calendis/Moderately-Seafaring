#Code for buttons

import pygame
pygame.font.init()

screen = pygame.display.set_mode()

#The activate function should be called from the event loop!

FONT_SIZE = 14

oxygen_bold_path = "fonts/Oxygen-Bold.ttf"
oxygen_bold_font = pygame.font.Font(oxygen_bold_path, FONT_SIZE)

class Button(): #Base class for buttons
	"""docstring for Button"""
	def __init__(self, x, y, width, height, colour, text):
		super(Button, self).__init__()
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.colour = colour
		self.original_colour = self.colour
		self.hover_colour = (self.colour[0]+10, self.colour[1]+10, self.colour[2]+10)
		self.hovered = False
		self.text = text
		self.textlength = len(text)
		self.text = oxygen_bold_font.render(self.text,1,(0,0,0))

		if self.width < self.textlength*FONT_SIZE:
			self.width = self.textlength*FONT_SIZE

	def draw(self):
		pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))
		screen.blit(self.text, (self.x+self.width/2 - (self.textlength*FONT_SIZE)/4, self.y+FONT_SIZE/4+FONT_SIZE/2))

	def update(self):
		if pygame.Rect.colliderect(pygame.Rect(self.x, self.y, self.width, self.height), pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)):
			self.hovered = True
			self.colour = self.hover_colour
		else:
			self.hovered = False
			self.colour = self.original_colour

	def activate(self):
		print("Button "+str(self)+" activated.")

class ExitButton(Button):
	"""docstring for ExitButton"""
	def __init__(self, x, y, width, height, colour, text):
		super(ExitButton, self).__init__(x, y, width, height, colour, text)

class PlayButton(Button):
	"""docstring for PlayButton"""
	def __init__(self, x, y, width, height, colour, text):
		super(PlayButton, self).__init__(x, y, width, height, colour, text)
		
		

		