import pygame , sys

from pygame.locals import *
import math
from random import randint

class Ball:
	def __init__(self,width,height):
		self.width = width
		self.height = height
		self.x_pos = width//2
		self.y_pos = height//2
		self.rad = 10
		self.color =  (255,0,0) # red
		self.max_speed = 0.1
		self.speedx = 1*self.max_speed
		self.speedy = 1*self.max_speed

	def dist_sq(self,striker):
		x = self.x_pos-striker.x_pos
		y = self.y_pos - striker.y_pos

		return (x**2) + (y**2)

	def collision(self,striker):
		theta = math.atan((striker.y_pos-self.y_pos)/(striker.x_pos-self.x_pos))
		self.speedx = self.max_speed*(2**0.5)*math.cos(theta)
		self.speedy = self.max_speed*(2**0.5)*math.sin(theta)

		if self.x_pos<striker.x_pos:
			self.speedx =  -self.speedx
			self.speedy =  -self.speedy



	def update(self,striker,point,score):
		self.x_pos += self.speedx
		self.y_pos += self.speedy

		#check collision
		if self.dist_sq(striker) < (striker.rad + self.rad)**2:
			self.collision(striker)

		if self.dist_sq(point) < (self.rad+point.rad)**2:
			score.update(1)
			point.random()


		if self.x_pos+self.rad > width:
			self.x_pos = width - self.rad
			self.speedx = -self.speedx
			return True

		if self.x_pos - self.rad <0 :
			self.x_pos  = self.rad
			self.speedx = -self.speedx
			return True

		if self.y_pos+self.rad > height:
			self.y_pos = height-self.rad
			self.speedy = -self.speedy
			return False

		if self.y_pos -self.rad <0:
			self.y_pos = self.rad 
			self.speedy = -self.speedy

			return True
	def draw(self,pygame,DISPLAYSURF):
		pygame.draw.circle(DISPLAYSURF, self.color, (int(self.x_pos),int(self.y_pos)), self.rad, 0)


class Striker:
	def __init__(self,width,height):
		self.width = width
		self.height = height
		self.x_pos = width//2
		self.y_pos = height -50
		self.rad = 30
		self.color = (0,255,0)

	def update(self,mouse_pos):
		self.x_pos , _ = mouse_pos
		if self.x_pos+self.rad > width:
			self.x_pos = width - self.rad

		if self.x_pos - self.rad <0 :
			self.x_pos  = self.rad


	def draw(self,pygame,DISPLAYSURF):
		pygame.draw.circle(DISPLAYSURF, self.color, (int(self.x_pos),int(self.y_pos)), self.rad, 0)


class Point:
	def __init__(self,width,height):
		self.width = width
		self.height = height
		self.rad = 15
		self.x_pos = randint(self.rad,width-self.rad)
		self.y_pos = randint(self.rad,height -100-self.rad)
		
		self.color = (0,0,255)
	def random(self):
		self.x_pos = randint(self.rad,self.width-self.rad)
		self.y_pos = randint(self.rad,self.height -100-self.rad)
	def draw(self,pygame,DISPLAYSURF):
		pygame.draw.circle(DISPLAYSURF, self.color, (int(self.x_pos),int(self.y_pos)), self.rad, 0)


class Score:
	def __init__(self,pygame,width,height):
		self.width = width
		self.height = height
		self.score = 0
		self.color = (0,0,0)
		self.back = (255,255,255)
		self.fontObj = pygame.font.Font('freesansbold.ttf', 20)
		self.textSurfaceObj = self.fontObj.render(str(self.score), True, self.color, self.back)
		self.textRectObj = self.textSurfaceObj.get_rect()
		self.textRectObj.center = (self.width//2, 20)
		
	def update(self,a):
		self.score+=a
		self.textSurfaceObj = self.fontObj.render(str(self.score), True, self.color, self.back)
		self.textRectObj = self.textSurfaceObj.get_rect()
		self.textRectObj.center = (self.width//2, 20)
	def draw(self,pygame,DISPLAYSURF):
		# DISPLAYSURF.fill(self.back)
		DISPLAYSURF.blit(self.textSurfaceObj, self.textRectObj)
		


score =0

pygame.init()

width = 300
height = 600
DISPLAYSURF = pygame.display.set_mode((width,height))
pygame.display.set_caption('helloworls')

GREEN = (  0, 255,   0)
RED = (255,0,0)
WHITE = (0,0,0)
ball = Ball(width,height)
striker = Striker(width,height)
point = Point (width,height)
score = Score(pygame,width,height)
while True:
	DISPLAYSURF.fill(WHITE)
	bul = ball.update(striker,point,score)
	if bul == False:
		score.update(-1)
		del(ball)
		ball = Ball(width,height)
	ball.draw(pygame,DISPLAYSURF)
	striker.draw(pygame,DISPLAYSURF)
	point.draw(pygame,DISPLAYSURF)
	score.draw(pygame,DISPLAYSURF)
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == MOUSEMOTION:
			striker.update(event.pos)
			striker.draw(pygame,DISPLAYSURF)

	pygame.display.update()