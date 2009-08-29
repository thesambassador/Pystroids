import pygame
import time
import cPickle
from text import Text
from movingObject import movingObject
from player import Player
from vector import *
from asteroid import Asteroid
from constants import *
from miscFunctions import *
from highscore import *

pygame.init()

screen = pygame.display.set_mode((600,600))
clock = pygame.time.Clock()

running = 1
level = 0
lives = 3
extraLives = 1
scene = 0
name = ""
highScores = HighScoreTable()

try:
	hsfile = open("highScores.dat")
	unpickler = cPickle.Unpickler(hsfile)
	highScores = unpickler.load()
except:
	print "bla"
	highScores = HighScoreTable()

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

#ZOMG GAME LOOP
while running:
	
	ticks = clock.tick(50)
	
	#Menu Scene
	if scene == 0:
	
		screen.fill((0,0,0))
		objs.update(ticks, screen)
		
		#I don't know a better way to handle basic texts... this class kinda sucks. 
		texts = []
		
		texts.append(Text(screen, CENTER, (255,255,255,255), 50, "PYSTROIDS", .75*screen.get_height()/2))
		texts.append(Text(screen, CENTER, (255,255,255,255), 20, "Press Space to Start", screen.get_height()/2))
	
		
		for t in texts:
			t.update()
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = 0
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					objs = pygame.sprite.Group([])
					font = pygame.font.Font(pygame.font.get_default_font(), 25)
					points = 0
					lives = 1
					level = 1
					extraLives = 1
					scene = 1
					projs = []
					explosions = []
					player = Player(screen, projs)
				elif event.key == pygame.K_h:
					scene = 3
					
	
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
			elif event.type == LEVELUP:
				level += 1
				for i in range(0, level+2):
					objs.add(Asteroid(screen, asteroidImgs, 70, player, objs))
			#points
			elif event.type == POINTS:
				points += event.points
				
			#player dies
			elif event.type == PLAYERDEAD:
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
		
		texts.append(Text(screen, CENTER, (255,255,255,255), 50, "GAME OVER", .75*screen.get_height()/2))
		texts.append(Text(screen, CENTER, (255,255,255,255), 20, "Enter your Name", screen.get_height()/2))
		texts.append(Text(screen, CENTER, (255,255,255,255), 15, name, 1.25*screen.get_height()/2))
		texts.append(Text(screen, CENTER, (255,255,255,255), 20, "Score: "+str(points), 1.5*screen.get_height()/2))
		
		for t in texts:
			t.update()
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = 0
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					highScores.addScore(HighScore(points, name))
					print highScores
					scene = 0
				elif event.key == pygame.K_BACKSPACE and len(name) > 0:
					name = name[0:-1]
				elif event.key < 123 and event.key >= 97:
					name += pygame.key.name(event.key).upper()
	
	#High Scores scene
	elif scene == 3:
		screen.fill((0,0,0))
		objs.update(ticks, screen)
		
		#I don't know a better way to handle basic texts... this class kinda sucks. 
		texts = []
		texts.append(Text(screen, CENTER, (255,255,255,255), 40, "High Scores", 20))
		texts.append(Text(screen, CENTER, (255,255,255,255), 20, "Press Space to Return to the Menu", screen.get_height() - 50))
		
		for i in range(1, 11):
			num = Text(screen)
			num.setWords(str(i)+".")
			num.setX(100 - num.font.size(num.words)[0])
			num.setyPos(100+25*i)
			texts.append(num)
		
		i = 1
		for score in highScores.scores:
			name = Text(screen)
			points = Text(screen)
			
			name.setWords(score.name)
			name.setX(150 - name.font.size(num.words)[0])
			name.setyPos(100+25*i)
			
			points.setWords(str(score.score))
			points.setAlignment(RIGHT)
			points.setX(-100)
			points.setyPos(100+25*i)
			
			texts.append(points)
			texts.append(name)
			i+= 1
			
		
		for t in texts:
			t.update()
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = 0
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					scene = 0
	
	
	pygame.display.flip()
	
	
	
	
	
	
	
	
	
	
	