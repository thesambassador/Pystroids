import pygame
from vector import *

class movingObject(pygame.sprite.Sprite):
	def __init__(self, img, startX, startY, radius):
		pygame.sprite.Sprite.__init__(self)
		
		if type(img) == pygame.Surface:
			self.origImage = img
		else:
			self.origImage = pygame.Surface.convert(pygame.image.load(img))
			self.origImage.set_colorkey((0,0,0))
		
		self.image = self.origImage
		self.rect = self.image.get_rect()
		self.rect.center = (startX, startY)
		self.radius = radius
		self.pos = Vector(startX, startY) #float position, is translated to pixel position by update
		self.v = Vector() #used to calc next position
		self.a = Vector() #used to calc next velocity
		self.f = Vector() #used to calc next accel
		self.angV = 0 #used to calc next rot
		self.rot = 0
		self.mass = 1.0
		
	def update(self, ticks, screen):				
		#movement stuff
		self.rot += self.angV
		oldCent = self.rect.center
		newImage = pygame.transform.rotozoom(self.image, self.rot, 1)
		self.rect = newImage.get_rect()
		self.rect.center = oldCent
		
		self.a = self.a + Vector(self.f.x/self.mass, self.f.y/self.mass)
		self.v = self.v + self.a
		self.pos = self.pos + self.v
		self.rect.centerx = self.pos.x
		self.rect.centery = self.pos.y
		screen.blit(newImage, self.rect)
		self.a = Vector()
		
		#others
		if self.pos.x > screen.get_width()+50:
			self.pos.x = -50
		elif self.pos.x < -50:
			self.pos.x = screen.get_width()+50
		if self.pos.y > screen.get_height()+50:
			self.pos.y = -50
		elif self.pos.y < -50:
			self.pos.y = screen.get_height()+50
			