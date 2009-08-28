import pygame
from constants import *

class Text():
	def __init__(self, screen, alignment=LEFT, color=(255,255,255,255), size=20, words="", yPos=0):
		if not pygame.font.get_init():
			pygame.font.init()
		self.font = pygame.font.Font(pygame.font.get_default_font(), size)
		self.screen = screen
		self.align = alignment
		self.color = color
		self.words = words
		self.yPos = yPos
		
	def setSize(self, size):
		self.font = pygame.font.Font(pygame.font.get_default_font(), size)
	
	def setAlignment(self, align):
		self.align = align
		
	def setColor(self, col):
		self.color = col
	
	def setWords(self, words):
		self.words = words
	
	def setyPos(self, yPos):
		self.yPos = yPos
	
	def update(self):
		xPos = (self.screen.get_width())/2.0*self.align - (self.align*.5*self.font.size(self.words)[0])
		self.screen.blit(self.font.render(self.words, 0, self.color), (xPos, self.yPos))