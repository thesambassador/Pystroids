import pygame
import random
from movingObject import *
from vector import *
from projectile import *

class Asteroid(movingObject):
	def __init__(self, screen, imgList, radius, player, objectList, startPos=Vector(-1, -1), startVel=Vector(0, 0)):
		self.screen = screen
		self.objs = objectList
		self.player = player
		self.imgList = imgList
		
		if startPos.x < 0:
			startPos = Vector(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()))
			while dist(player.pos, startPos) < player.radius + 100:
				startPos = Vector(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()))
		
		i = random.randint(0,9)
		
		if radius == 70:
			image = imgList[i]
		elif radius == 40:
			image = imgList[i+10]
		else:
			image = imgList[i+20]
			
		movingObject.__init__(self, image, startPos.x, startPos.y, radius)
		
		self.angV = random.uniform(-1, 1)
		
		if startVel.x == 0:
			self.v = Vector(random.choice((-1, 1))*random.randint(1, 2), random.choice((-1, 1))*random.randint(1, 2))
		else:
			self.v = startVel
		
	def destroy(self, hitPos):
		hitVect = self.pos - hitPos
		newPos1 = self.pos + create(hitVect.angle() + 90, 40)
		newPos2 = self.pos + create(hitVect.angle() - 90, 40)
		
		points = 0
		
		#print newPos1, newPos2, self.pos, hitPos, hitVect
		if self.radius == 70:
			offset = Vector(random.uniform(-.3, .3), random.uniform(-.3, .3))
			self.objs.add(Asteroid(self.screen, self.imgList, 40, self.player, self.objs, newPos1, self.v+offset))
			offset = Vector(random.uniform(-.3, .3), random.uniform(-.3, .3))
			self.objs.add(Asteroid(self.screen, self.imgList, 40, self.player, self.objs, newPos2, self.v+offset))
			self.objs.remove(self)
			points = 20
			
		elif self.radius == 40:
			newPos1.setMag(newPos1.length()-40)
			newPos2.setMag(newPos1.length()-40)
			print newPos1.length()
			offset = Vector(random.uniform(-.3, .3), random.uniform(-.3, .3))
			self.objs.add(Asteroid(self.screen, self.imgList, 20, self.player, self.objs, newPos1, self.v+offset))
			offset = Vector(random.uniform(-.3, .3), random.uniform(-.3, .3))
			self.objs.add(Asteroid(self.screen, self.imgList, 20, self.player, self.objs, newPos2, self.v+offset))
			self.objs.remove(self)
			points = 50
		else:
			self.objs.remove(self)
			points = 100
		
		dict = {'points': points}
		postPoints = pygame.event.Event(200, dict)
		pygame.event.post(postPoints)
		