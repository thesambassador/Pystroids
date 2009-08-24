import pygame
import time
from movingObject import movingObject
from player import Player
from vector import *
from asteroid import Asteroid
from miscFunctions import *

screen = pygame.display.set_mode((600,600))
clock = pygame.time.Clock()

running = 1
level = 0
lives = 3

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

#Start level 1
pygame.event.post(pygame.event.Event(202, {}))
	
print len(asteroidImgs)
#group.add(test)

while running:
	
	ticks = clock.tick(50)
	
	#events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = 0
		elif event.type == pygame.KEYUP or event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_SPACE:
				player.keyEvent(event)
			elif event.key == pygame.K_ESCAPE:
				running = 0
		#points
		elif event.type == 200:
			points += event.points
			
		#player dies
		elif event.type == 201:
			lives -= 1
			
		#next level
		elif event.type == 202:
			level += 1
			for i in range(0, level+2):
				objs.add(Asteroid(screen, asteroidImgs, 70, player, objs))
				
	
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
	
	#signal all asteroids destroyed:
	if len(objs) == 0:
		pygame.event.post(pygame.event.Event(202, {}))
	
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
	
	pygame.display.flip()
	