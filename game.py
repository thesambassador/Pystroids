import pygame
import time
from movingObject import movingObject
from player import Player
from vector import *
from asteroid import Asteroid
from miscFunctions import *

pygame.init()

screen = pygame.display.set_mode((600,600))
clock = pygame.time.Clock()

running = 1
level = 0
lives = 3
extraLives = 1
scene = 0
name = ""
highScoreName = ""
highScore = 0


#gui stuff
pygame.font.init()
font = pygame.font.Font(pygame.font.get_default_font(), 20)
points = 0

livesImg = pygame.Surface((43,43), pygame.SRCALPHA)
livesImg.fill((0,0,0,0))
pygame.draw.line(livesImg, pygame.Color('white'), (21, 1), (7, 36), 2)
pygame.draw.line(livesImg, pygame.Color('white'), (21, 1), (32, 36), 2)
pygame.draw.line(livesImg, pygame.Color('white'), (10, 30), (30, 30), 2)
livesImg = pygame.transform.rotozoom(livesImg, 0, .75)

#Generate a list of random asteroid images (so it doens't have to generate a new one every time)
asteroidImgs = []
for i in range(0,10):
	asteroidImgs.append(generateAsteroid(70))
for i in range(0,10):
	asteroidImgs.append(generateAsteroid(40))
for i in range(0,10):
	asteroidImgs.append(generateAsteroid(20))

#Object lists... projectiles get their own
explosions = []
projs = []
objs = pygame.sprite.Group([])

player = Player(screen, projs)
	
#random asteroids in the background of the background!
for i in range(0, 6):
	objs.add(Asteroid(screen, asteroidImgs, 70, player, objs))

while running:
	
	ticks = clock.tick(50)
	
	#Menu Scene
	if scene == 0:
	
		screen.fill((0,0,0))
		objs.update(ticks, screen)
		
		#probably should write a class for this... Writes a few text lines to different places/sizes
		#wanted to condense writing multiple centered texts at multiple sizes and location.  UGLY!
		texts = []
		texts.append((pygame.font.Font(pygame.font.get_default_font(), 50), .75,"PYSTROIDS"))
		texts.append((pygame.font.Font(pygame.font.get_default_font(), 20), 1, "Press Space to Start"))
		texts.append((pygame.font.Font(pygame.font.get_default_font(), 15), 1.75, "High Score: " + highScoreName + " " + str(highScore)))
		
		for t in texts:
			font = t[0]
			mult = t[1]
			text = t[2]
			posX = screen.get_width()/2 - font.size(text)[0]/2
			posY = screen.get_height()/2*mult * .75 - font.size(text)[1]/2
			screen.blit(font.render(text, 0, (255,255,255,255)), (posX, posY))
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = 0
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					objs = pygame.sprite.Group([])
					font = pygame.font.Font(pygame.font.get_default_font(), 25)
					score = 0
					lives = 1
					extraLives = 1
					scene = 1
					projs = []
					explosions = []
					player = Player(screen, projs)
					
					
	#Game scene
	elif scene == 1:
		#Game Events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = 0
			elif event.type == pygame.KEYUP or event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_SPACE:
					player.keyEvent(event)
				elif event.key == pygame.K_ESCAPE:
					running = 0
			#next level
			elif event.type == pygame.USEREVENT+1:
				level += 1
				for i in range(0, level+2):
					objs.add(Asteroid(screen, asteroidImgs, 70, player, objs))
			#points
			elif event.type == pygame.USEREVENT+2:
				points += event.points
				
			#player dies
			elif event.type == pygame.USEREVENT+3:
				lives -= 1
				
		#update objects
		screen.fill((0,0,0))
		objs.update(ticks, screen)
		player.update(ticks, screen, objs)
		
		#draw explosion particles
		for i in explosions:
			if i.life <= 0:
				explosions.remove(i)
			else:
				i.update(ticks, screen)
		
		#check for projectile collisions
		for proj in projs:
			if proj.life <= 0:
				projs.remove(proj)
			else:
				proj.update(ticks, screen)
	
		#check collisions
		for obj in objs:
			for proj in projs:
				if dist(obj.pos, proj.pos) < obj.radius:
					obj.destroy(proj.pos)
					projs.remove(proj)
					explosion(proj.pos, 100, explosions)
					break
			if dist(obj.pos, player.pos) < obj.radius + player.radius:
				player.destroy()
		
		#update gui
		screen.blit(font.render(str(points), 0, (255,255,255,255)), (5, 5))
		for i in range(1, lives+1):
			screen.blit(livesImg, (screen.get_width() - (i*livesImg.get_width()), 5))
			
		#signal all asteroids destroyed:
		if len(objs) == 0:
			pygame.event.post(pygame.event.Event(pygame.USEREVENT+1, {}))
		
		#signal extra life:
		if points == 10000 * extraLives:
			lives += 1
			extraLives += 1
		
		#signal no lives left:
		if lives == 0:
			name = ""
			scene = 2
	#Game Over scene
	elif scene == 2:
		screen.fill((0,0,0))
		objs.update(ticks, screen)
		
		#probably should write a class for this... Writes a few text lines to different places/sizes
		#wanted to condense writing multiple centered texts at multiple sizes and location.  UGLY!
		texts = []
		texts.append((pygame.font.Font(pygame.font.get_default_font(), 50), .75,"GAME OVER"))
		texts.append((pygame.font.Font(pygame.font.get_default_font(), 20), 1,"Enter your Name"))
		texts.append((pygame.font.Font(pygame.font.get_default_font(), 15), 1.25,name))
		texts.append((pygame.font.Font(pygame.font.get_default_font(), 20), 1.5,"Score: "+str(score)))
		
		for t in texts:
			font = t[0]
			mult = t[1]
			text = t[2]
			posX = screen.get_width()/2 - font.size(text)[0]/2
			posY = screen.get_height()/2*mult * .75 - font.size(text)[1]/2
			screen.blit(font.render(text, 0, (255,255,255,255)), (posX, posY))
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = 0
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					highScore = score
					highScoreName = name
					scene = 0
				elif event.key == pygame.K_BACKSPACE and len(name) > 0:
					name = name[0:-1]
				elif event.key < 123 and event.key >= 97:
					name += pygame.key.name(event.key)
	pygame.display.flip()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	