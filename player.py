import pygame
import random
import sys
import time
import math
import os
from movingObject import *
from vector import *
from projectile import *

class Player(movingObject):
	def __init__(self, screen, projectiles):
		
		image = pygame.Surface((43,37), pygame.SRCALPHA)
		
		image.fill((0,0,0,0))
		
		pygame.draw.line(image, pygame.Color('white'), (21, 1), (7, 36), 2)
		pygame.draw.line(image, pygame.Color('white'), (21, 1), (32, 36), 2)
		pygame.draw.line(image, pygame.Color('white'), (10, 30), (30, 30), 2)
		image = pygame.transform.rotozoom(image, -90, 1)
		
		movingObject.__init__(self, image, 300, 300, 18)
		
		self.rot = 90
		self.mass = 10
		self.alive = 1
		self.screen = screen
		self.thrust = 1
		self.rotSpeed = 7
		self.keyUp = 0
		self.frame = 0
		self.projs = projectiles
		self.respawnTime = 100
		self.keyLeft = 0
		self.keyRight = 0
		
	def keyEvent(self, event):
		if self.alive:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					self.keyUp = 1
				elif event.key == pygame.K_LEFT:
					self.keyLeft = self.rotSpeed
				elif event.key == pygame.K_RIGHT:
					self.keyRight = -self.rotSpeed
				elif event.key == pygame.K_SPACE:
					shipTip = create(self.rot, 22)
					shipTip.y *= -1
					shipTip += self.pos
					if len(self.projs) < 6:
						self.projs.append(Projectile(shipTip, self.rot, self.v, 4, 70))
					
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_UP:
					self.keyUp = 0
				if event.key == pygame.K_LEFT:
					self.keyLeft = 0
				if event.key == pygame.K_RIGHT:
					self.keyRight = 0
		
	def update(self, ticks, screen, objs):
		if self.alive:
			if self.keyUp:
				self.f = create(self.rot, self.thrust)
				self.f.y *= -1
				
				if self.frame == 0:
					self.frame = 1
				else:
					self.frame = 0
			else:
				self.f = Vector()
				self.image = self.origImage
			
			self.angV = self.keyRight + self.keyLeft
		else:
			if self.respawnTime > 0:
				self.respawnTime -= 1
			else:
				for obj in objs:
					if dist(obj.pos, self.pos) < obj.radius + self.radius:
						break
				else:
					self.alive = 1
					self.respawnTime = 100
					
					pygame.draw.line(self.image, pygame.Color('white'), (21, 1), (7, 36), 2)
					pygame.draw.line(self.image, pygame.Color('white'), (21, 1), (32, 36), 2)
					pygame.draw.line(self.image, pygame.Color('white'), (10, 30), (30, 30), 2)
					self.image = pygame.transform.rotozoom(self.image, -90, 1)
					self.origImage = self.image
				
			
		movingObject.update(self, ticks, screen)
		
	def destroy(self):
		if self.alive:
			self.__init__(self.screen, self.projs)
			self.image.fill((0,0,0,0))
			self.alive = 0
			
			dead = pygame.event.Event(pygame.USEREVENT+3, pos = self.pos)
			pygame.event.post(dead)
			
		