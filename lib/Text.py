#Useful stuff related to pygame text rendering
import pygame

pygame.font.init()

oxygen_font_path = "resources/fonts/Oxygen-Regular.ttf"
oxygen_font = pygame.font.Font(oxygen_font_path, 12)
screen = pygame.display.set_mode()

#Helper function for rendering and blitting pygame text in one.

def draw_text(x, y, text, antialiased=1, colour=(0, 0, 0)):
	rendered_text = oxygen_font.render(text, antialiased, colour)
	screen.blit(rendered_text, (x, y))