import pygame
from vector import *

class Projectile():
	def __init__(self, startVector, angle, vel, minVel, life):
		self.pos = startVector
		self.vel = create(angle, minVel)
		self.vel.y *= -1
		
		if (self.vel + vel).length() >= minVel:
			self.vel += vel
		
		self.life = life
		self.startLife = life
		self.color = pygame.Color('white')
		self.color.a = 255
	
	def update(self, ticks, screen):
		self.pos += self.vel
		
		if self.pos.x > screen.get_width()+50:
			self.pos.x = -50
		elif self.pos.x < -50:
			self.pos.x = screen.get_width()+50
		if self.pos.y > screen.get_height()+50:
			self.pos.y = -50
		elif self.pos.y < -50:
			self.pos.y = screen.get_height()+50
		
		if self.life < 10:
			self.color.r -= 28
			self.color.g -= 28
			self.color.b -= 28
			pass
		
		screen.set_at((int(self.pos.x), int(self.pos.y)), self.color)
		self.life -= 1