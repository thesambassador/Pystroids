import pygame
import math
import random

def create(ang, mag):
	return Vector(math.cos(math.radians(ang))*mag, math.sin(math.radians(ang))*mag)
def dist(p1, p2):
	diff = p1-p2
	diff.x, diff.y = math.fabs(diff.x), math.fabs(diff.y)
	return diff.length()
def randomVector((minX, maxX), (minY, maxY)):
	return Vector(random.uniform(minX, maxX), random.uniform(minY, maxY))

class Vector():
	def __init__(self, x=0.0, y=0.0):
		self.x = x
		self.y = y
	
	def __add__(self, other):
		return Vector(self.x + other.x, self.y + other.y)
	
	def __iadd__(self, other):
		return Vector(self.x + other.x, self.y + other.y)
		
	def __sub__(self, o):
		return Vector(self.x - o.x, self.y - o.y)
	
	def __div__(self, other):
		return Vector(self.x / other.x, self.y / other.y)
	
	def __mul__(self, other):
		return Vector(self.x * other.x, self.y * other.y)
		
	def __str__(self):
		return '(%f,%f)' % (self.x, self.y)
	
	def length(self):
		return math.hypot(self.x, self.y)
		
	def angle(self):
		if self.y == 0:
			if self.x >= 0:
				return 0.0
			else:
				return 180.0
		else:
			return math.degrees(math.atan(self.y/self.x))
	
	def toList(self):
		return (self.x, self.y)
	
	def setMag(self, mag):
		new = create(self.angle(), mag)
		self.x = new.x
		self.y = new.y