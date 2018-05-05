#Sound effect loader
#Moderately Seafaring
import pygame
from random import randint

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.mixer.init()

menu = pygame.mixer.Sound("resources/aud/sfx/menu.wav")
confirm = pygame.mixer.Sound("resources/aud/sfx/confirm.wav")
back = pygame.mixer.Sound("resources/aud/sfx/back.wav")
attack = pygame.mixer.Sound("resources/aud/sfx/attack.wav")
attack_hard = pygame.mixer.Sound("resources/aud/sfx/attack_hard.wav")
attack_rocket = pygame.mixer.Sound("resources/aud/sfx/attack_rocket.wav")
buff = pygame.mixer.Sound("resources/aud/sfx/buff.wav")
nerf = pygame.mixer.Sound("resources/aud/sfx/nerf.wav")
death_short = pygame.mixer.Sound("resources/aud/sfx/death_short.wav")
death_long = pygame.mixer.Sound("resources/aud/sfx/death_long.wav")
health = pygame.mixer.Sound("resources/aud/sfx/health.wav")

pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.load("resources/aud/mus/The_High_Seas.wav")
pygame.mixer.music.play(-1)

def play_battle_music(enemy_name=False):
	if not enemy_name:
		result = randint(0,3)
	if result == 0:
		pygame.mixer.music.load("resources/aud/mus/Shwippity.wav")
	elif result == 1:
		pygame.mixer.music.load("resources/aud/mus/Specials_Bin.wav")
	elif result == 2:
		pygame.mixer.music.load("resources/aud/mus/8-180.wav")
	elif result == 3:
		pygame.mixer.music.load("resources/aud/mus/Fight!.wav")
	
	pygame.mixer.music.play(-1)

def play_overworld_music(area_name):
	if area_name == "sea":
		pygame.mixer.music.load("resources/aud/mus/I_See_the_Sea.wav")
	elif area_name == "fanfare":
		pygame.mixer.music.load("resources/aud/mus/Fanfare.wav")
	pygame.mixer.music.play(-1)