#Code for selector objects (just animated images essentially)
#Moderately Seafaring
import pygame
from lib import UIImage

class Selector():
	"""docstring for Selector"""
	def __init__(self, x, y):
		super(Selector, self).__init__()
		self.x = x
		self.y = y
		self.frame = 0
		self.images = [None]
		self.image = self.images[self.frame]

	def update(self):
		self.frame += 1
		if self.frame > len(self.images) -1:
			self.frame = 0
		self.image = self.images[self.frame]

	def set_pos(self, new_x, new_y):
		self.x = new_x
		self.y = new_y

	def get_pos(self):
		return (self.x, self.y)

	def get_image(self):
		return self.image

class SelectorTopLeft(Selector):
	"""docstring for SelectorTopLeft"""
	def __init__(self, x, y):
		super(SelectorTopLeft, self).__init__(x, y)
		self.images = UIImage.select_top_left_images

class SelectorTopRight(Selector):
	"""docstring for SelectorTopRight"""
	def __init__(self, x, y):
		super(SelectorTopRight, self).__init__(x, y)
		self.images = UIImage.select_top_right_images

class SelectorBottomLeft(Selector):
	"""docstring for SelectorBottomLeft"""
	def __init__(self, x, y):
		super(SelectorBottomLeft, self).__init__(x, y)
		self.images = UIImage.select_bottom_left_images

class SelectorBottomRight(Selector):
	"""docstring for SelectorBottomRight"""
	def __init__(self, x, y):
		super(SelectorBottomRight, self).__init__(x, y)
		self.images = UIImage.select_bottom_right_images
		