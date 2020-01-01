import pygame
import random
pygame.init()

win = pygame.display.set_mode((288,512))
pygame.display.set_caption("Flappy Bird")

# images
birdImg = [pygame.image.load("bird0.gif"),pygame.image.load("bird1.gif"),pygame.image.load("bird2.gif")]
pipeImg = [pygame.image.load("tube1.gif"),pygame.image.load("tube2.gif")]
bgImg   = [pygame.image.load("bg1.gif"),pygame.image.load("bg1.gif")]

clock = pygame.time.Clock()
score = 0
gap = 100
font = pygame.font.SysFont('comicsans', 30, True)

pipes = []

class bird(object):
	"""class to hold all info about the bird"""
	def __init__(self, x,y,width,height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.gravity = 2
		self.walkCount = 0
		self.jumpCount = 10
		self.isJump = False
		self.hitbox = (self.x, self.y, self.width, self.height)

	def draw(self, win):

		if self.isJump == False:
			if self.y < 500:
				self.y += ((self.gravity ** 2) * 0.05)
				self.gravity += 1

		if self.walkCount + 1 >= 9:
			self.walkCount = 0
		else:
			self.walkCount += 1
		self.hitbox = (self.x, self.y, 36, 24)
		win.blit(birdImg[self.walkCount // 3] , (self.x,self.y))
		# pygame.draw.rect(win, (255,0,0),self.hitbox,1)
	
class pipe(object):
	"""docstring for pipe"""
	def __init__(self, x, y, height, width, gap):
		self.x = x
		self.y = y
		self.height = height
		self.width = width
		self.gap = gap 
		self.vel = 5
		self.hitboxbot = (self.x, self.y, self.width, self.height)
		self.hitboxtop = (self.x , self.y - self.height - self.gap, self.width, self.height)
		self.passed = False

	def draw(self, win):
		self.move()
		self.hitboxbot = (self.x, self.y, self.width, self.height)
		self.hitboxtop = (self.x , self.y - self.height - self.gap, self.width, self.height)
		win.blit(pipeImg[1], (self.x, self.y))
		win.blit(pipeImg[0], (self.x , self.y - self.gap - self.height))
		# pygame.draw.rect(win, (255,0,0),self.hitboxbot,1)
		# pygame.draw.rect(win, (255,0,0),self.hitboxtop,1)

	def move(self):
		if self.x + self.width >= 0:
			self.x -= self.vel

		else: 
			pipes.pop(0)
			new_pipe = pipe(512,random.randint(192,400),320,52,gap)
			pipes.append(new_pipe)



def redrawGameWindow():
	win.blit(bgImg[1],(0,0))
	text = font.render('Score: ' + str(score), 1, (0,0,0))
	
	flappy.draw(win)
	for i in range(0,len(pipes)):
		pipes[i].draw(win)
	win.blit(text, (100, 10))
	pygame.display.update()

def hit():
	text = font.render("You Crashed" , 1, (0,0,0))
	extraText = font.render("Try Again Y/N" , 1, (0,0,0))
	win.blit(text, (75, 200))
	win.blit(extraText, (65, 250))
	pygame.display.update()
	while True:
		#*having difficuilty here***
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False # not working ?

		keys = pygame.key.get_pressed()
		if keys[pygame.K_y]:
			for i in range(0,len(pipes)):
				pipes.pop(0)

			new_pipe = pipe(512,300,320,52,gap)
			pipes.append(new_pipe) 
			score = 0 # not working ?
			break
		if keys[pygame.K_n]:
			run = False # not working ?
		#*****************************************#
		


#mainloop
flappy = bird(20,256,35,24)
new_pipe = pipe(512,300,320,52,gap)
pipes.append(new_pipe) 

run = True
while run == True:
	clock.tick(27)
	# check for collision
	for i in pipes:
		if flappy.hitbox[1] < i.hitboxtop[1] + i.hitboxtop[3] and flappy.hitbox[1] + flappy.hitbox[3] > i.hitboxtop[1]:			
			if flappy.hitbox[0] + flappy.hitbox[2] > i.hitboxtop[0] and flappy.hitbox[0] < i.hitboxtop[0] + i.hitboxtop[2]:
				print("hit")
				hit()
		if flappy.hitbox[1] < i.hitboxbot[1] + i.hitboxbot[3] and flappy.hitbox[1] + flappy.hitbox[3] > i.hitboxbot[1]:			
			if flappy.hitbox[0] + flappy.hitbox[2] > i.hitboxbot[0] and flappy.hitbox[0] < i.hitboxbot[0] + i.hitboxbot[2]:
				print("hit")
				hit()
		else:
			if i.passed == False:
				score += 1
			i.passed = True


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	keys = pygame.key.get_pressed()
	
	if flappy.isJump == False:
		if keys[pygame.K_SPACE]:
			flappy.isJump = True
			flappy.gravity = 2

	if flappy.isJump == True:
		flappy.jumpCount += 1
		if flappy.jumpCount < 6:
			flappy.y -= (flappy.jumpCount ** 2) * 0.5
		else:
			flappy.jumpCount = 0
			flappy.isJump = False


	if pipes[0].x <= 288 // 2 and len(pipes)  < 2:
		new_pipe = pipe(512,random.randint(192,400),320,52,gap)
		pipes.append(new_pipe)
		if pipes[1].x <= 288 // 2 and len(pipes) < 3:
			new_pipe = pipe(512,random.randint(192,400),320,52,gap)
			pipes.append(new_pipe)

	redrawGameWindow()

pygame.quit()