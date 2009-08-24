import pygame
import random
from vector import *
from projectile import *

def generateAsteroid(r):
	image = pygame.Surface((r*2+5, r*2+5), pygame.SRCALPHA)
	image.fill((0, 0, 0, 0))
	cent = Vector(r, r)
	
	
	#init point list with first point (first point is at 0 degrees and r length)
	pl = []
	pl.append((cent+Vector(r, 0)).toList())
	
	#num is the number of lines to create the asteroid with
	num = 30
	
	#generate the point list
	for i in range(1, num):
		l = random.uniform(r-r*.2, r)
		pl.append((cent+create(360.0/num*i, l)).toList())
	
	#image.set_at(cent.toList(), pygame.Color('white'))
	pygame.draw.lines(image, (255, 255, 255), 1, pl, 2)
	
	#fill the inside:
	fill(image, (0,0,0,255))
	
	return image
		
def fill(image, color):
	draw = 0
	onWhite = 0
	for y in range(0, image.get_height()-1):
		for x in range(0, image.get_width()-1):
			if onWhite:
				if image.get_at((x,y)) == (255,255,255,255):
					continue
				else:
					draw = 1
					onWhite = 0
			if draw:
				if image.get_at((x,y)) == (255,255,255,255):
					draw = 0
				else:
					image.set_at((x,y), color)
					
			else:
				if image.get_at((x,y)) == (255,255,255,255):
					onWhite = 1
				
		#if draw is still set at the end of the row, fill back the pixels
		if draw:
			x = image.get_width()-1
			while image.get_at((x,y)) != (255,255,255,255):
				image.set_at((x,y), (0,0,0,0))
				x -= 1
			draw = 0
		onWhite = 0

def explosion(start, num, list):
	for i in range (0, num):
		list.append(Projectile(start, random.uniform(0,360), randomVector((-3, 3), (-3, 3)), 1, 30))
	
	
	
	
	
	
	
	
	
	
	
	
	