import pygame, sys, random

#tao ham cho tro choi
def draw_floor():
		screen.blit(floor,(floor_x_pos,650))
		screen.blit(floor,(floor_x_pos+432,650))
def create_pipe():
	random_pipe_pos = random.choice(pipe_height)
	bottom_pipe = pipe_surface.get_rect(midtop = (500,random_pipe_pos))
	top_pipe = pipe_surface.get_rect(midtop = (500,random_pipe_pos-700))
	return bottom_pipe, top_pipe
def move_pipe(pipes):
	for pipe in pipes : 
		pipe.centerx -= 5
	return pipes
def draw_pipe(pipes):
	for pipe in pipes:
		if pipe.bottom >= 600:
			screen.blit(pipe_surface,pipe)
		else:
			flip_pipe = pygame.transform.flip(pipe_surface,False,True)
			screen.blit(flip_pipe,pipe)
def check_collision(pipes):
	for pipe in pipes:
		if bird_rect.colliderect(pipe):
			return False
	if bird_rect.top <= -75 or bird_rect.bottom >= 650:
		return False
	return True
def rotate_bird(bird1):
	new_bird = pygame.transform.rotozoom(bird1, -bird_movement*3, 1)
	return new_bird
def birdAnimation():
	new_bird = bird_list[bird_index]
	new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
	return new_bird, new_bird_rect
def score_display(gameState):
	if gameState == 'main game':
		score_surface = gameFont.render(str(int(score)), True, (255, 255, 255))
		scoreRect = score_surface.get_rect(center = (216, 100))
		screen.blit(score_surface, scoreRect)
	if gameState == 'game over':
		score_surface = gameFont.render(f'Score: {int(score)}', True, (255, 255, 255))
		scoreRect = score_surface.get_rect(center = (216, 100))
		screen.blit(score_surface, scoreRect)

		highest_score_surface = gameFont.render(f'High Score: {int(highestScore)}', True, (255, 255, 255))
		highest_scoreRect = highest_score_surface.get_rect(center = (216, 630))
		screen.blit(highest_score_surface, highest_scoreRect)
def update_score(score, highestScore):
	if score > highestScore:
		highestScore = score
	return highestScore

#pygame.mixer.pre_init()
pygame.init()
screen= pygame.display.set_mode((432,768))#tao man hinh
clock = pygame.time.Clock()
gravity = 0.2 #trong luc
gameactive = True
gameFont = pygame.font.Font('D:/FileGameFlappyBird/FileGame/04B_19.ttf', 40)
score = 0
highestScore = 0 

#chen background
bg = pygame.image.load('D:/FileGameFlappyBird/FileGame/assets/background-night.png').convert()
bg = pygame.transform.scale2x(bg)

#chen san
floor = pygame.image.load('D:/FileGameFlappyBird/FileGame/assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

#tao chim
#bird = pygame.image.load('D:/FileGameFlappyBird/FileGame/assets/yellowbird-midflap.png').convert_alpha()
#bird = pygame.transform.scale2x(bird)
bird_movement = 0
bird_down = pygame.transform.scale2x(pygame.image.load('D:/FileGameFlappyBird/FileGame/assets/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('D:/FileGameFlappyBird/FileGame/assets/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('D:/FileGameFlappyBird/FileGame/assets/yellowbird-upflap.png').convert_alpha())
bird_list = [ bird_down, bird_mid, bird_up] #0 1 2
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center = (100,384))

#tao timer cho bird
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap, 200)

#tao ong
pipe_surface = pygame.image.load('D:/FileGameFlappyBird/FileGame/assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

#tao timer cho ong
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)

pipe_height = [200,300,400]

#tao man hinh ket thuc
game_over_surface = pygame.transform.scale2x(pygame.image.load('D:/FileGameFlappyBird/FileGame/assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (216, 384))

#chen am thanh
flap_sound = pygame.mixer.Sound('D:/FileGameFlappyBird/FileGame/sound/sfx_wing.wav')

#while loop cua game
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				bird_movement = 0
				bird_movement = -7
				flap_sound.play()
			if event.key == pygame.K_SPACE and gameactive == False:
				gameactive = True
				pipe_list.clear()
				bird_rect.center = (100,384)
				bird_movement = 0
				score = 0
		if event.type == spawnpipe:
			pipe_list.extend(create_pipe())
		if event.type == birdflap:
			if bird_index < 2:
				bird_index += 1
			else:
				bird_index = 0
			bird, bird_rect = birdAnimation()		

	screen.blit(bg,(0,0))
	if gameactive:#game hoat dong 
		#hanh vi cua chim
		bird_movement += gravity
		rotated_bird = rotate_bird(bird)
		bird_rect.centery += bird_movement
		screen.blit(rotated_bird, bird_rect)

		#hanh vi cua ong
		pipe_list = move_pipe(pipe_list)
		draw_pipe(pipe_list)
		gameactive = check_collision(pipe_list)
		score += 0.01
		score_display('main game')
	else:
		screen.blit(game_over_surface, game_over_rect)
		highestScore = update_score(score, highestScore)
		score_display('game over')

	#hanh vi cua san 
	floor_x_pos -= 1
	draw_floor()
	if floor_x_pos <= -432:
		floor_x_pos = 0
	pygame.display.update()
	clock.tick(120)
