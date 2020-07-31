import pygame
import sys
import random
import os
import neat
from neat.math_util import softmax
import numpy as np

class Snake():
    def __init__(self, food):
        self.length = 2
        self.positions = [((screen_width/2), (screen_height/2))]
        self.direction = up
        self.color = (17, 24, 47)
        # Special thanks to YouTubers Mini - Cafetos and Knivens Beast for raising this issue!
        # Code adjustment courtesy of YouTuber Elija de Hoog
        self.food_position=food.position

        self.dir_up=1
        self.dir_down=0
        self.dir_right=0
        self.dir_left=0
        
        self.down_closest_distance=20.0
        self.up_closest_distance=480.0
        self.right_closest_distance=480.0
        self.left_closest_distance=480.0

        self.food_right_distance=0.0
        self.food_left_distance=0.0
        self.food_up_distance=0.0
        self.food_down_distance=0.0
        
        if (self.food_position[0]>self.positions[0][0]):
        	self.food_right_distance=self.food_position[0]-self.positions[0][0]
        	self.food_left_distance=480.0-self.food_right_distance
        elif (self.food_position[0]<self.positions[0][0]):
        	self.food_left_distance=self.positions[0][0]-self.food_position[0]
        	self.food_right_distance=480.0-self.food_left_distance
        else:
        	self.food_left_distance=0.0
        	self.food_right_distance=0.0
        if (self.food_position[1]>self.positions[0][1]):
        	self.food_down_distance=self.food_position[1]-self.positions[0][1]
        	self.food_up_distance=480.0-self.food_down_distance
        elif (self.food_position[1]<self.positions[0][1]):
        	self.food_up_distance=self.positions[0][1]-self.food_position[1]
        	self.food_down_distance=480.0-self.food_up_distance
        else:
        	self.food_up_distance=0.0
        	self.food_down_distance=0.0
        

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        else:
            self.direction = point
            if (point == up):
                self.dir_up=1
                self.dir_down=0
                self.dir_right=0
                self.dir_left=0
            elif (point == down):
                self.dir_down=1
                self.dir_up=0
                self.dir_right=0
                self.dir_left=0
            elif (point ==right):
                self.dir_right=1
                self.dir_left=0
                self.dir_up=0
                self.dir_down=0
            else:
                self.dir_left=1
                self.dir_right=0
                self.dir_up=0
                self.dir_down=0

    def collide(self):
        if len(self.positions) > 2 and self.get_head_position() in self.positions[2:]:
            return True


    def move(self):
        cur = self.get_head_position()
        x,y = self.direction
        new = (((cur[0]+(x*gridsize))%screen_width), (cur[1]+(y*gridsize))%screen_height)
        
        if len(self.positions) == self.length:
        	self.positions.pop()
        self.positions.insert(0, new)

        cur = self.get_head_position()
        self.down_closest_distance=480.0
        self.up_closest_distance=480.0
        self.right_closest_distance=480.0
        self.left_closest_distance=480.0	

        for p in self.positions[1:]:
        	if cur[1]==p[1]:
        		if cur[0]>p[0]:
        			if (cur[0]-p[0])<self.left_closest_distance:
        				self.left_closest_distance=cur[0]-p[0]
        			if (480-(cur[0]-p[0]))<self.right_closest_distance:	
        				self.right_closest_distance=480.0-(cur[0]-p[0])
        		elif cur[0]<p[0]:
        			if (p[0]-cur[0])<self.right_closest_distance:
        				self.right_closest_distance=p[0]-cur[0]
        			if (480-(p[0]-cur[0]))<self.left_closest_distance:	
        				self.left_closest_distance=480.0-(p[0]-cur[0])
        	elif cur[0]==p[0]:
        		if cur[1]>p[1]:
        			if (cur[1]-p[1])<self.up_closest_distance:
        				self.up_closest_distance=cur[1]-p[1]
        			if (480-(cur[1]-p[1]))<self.down_closest_distance:
        				self.down_closest_distance=480.0-(cur[1]-p[1])
        		elif cur[1]<p[1]:
        			if (p[1]-cur[1])<self.down_closest_distance:
        				self.down_closest_distance=p[1]-cur[1]
        			if (480-(p[1]-cur[1]))<self.up_closest_distance:
        				self.up_closest_distance=480.0-(p[1]-cur[1])

        if (self.food_position[0]>self.positions[0][0]):
            self.food_right_distance=self.food_position[0]-self.positions[0][0]
            self.food_left_distance=480.0-self.food_right_distance
        elif (self.food_position[0]<self.positions[0][0]):
            self.food_left_distance=self.positions[0][0]-self.food_position[0]
            self.food_right_distance=480.0-self.food_left_distance
        else:
            self.food_left_distance=0.0
            self.food_right_distance=0.0
        if (self.food_position[1]>self.positions[0][1]):
            self.food_down_distance=self.food_position[1]-self.positions[0][1]
            self.food_up_distance=480.0-self.food_down_distance
        elif (self.food_position[1]<self.positions[0][1]):
            self.food_up_distance=self.positions[0][1]-self.food_position[1]
            self.food_down_distance=480.0-self.food_up_distance
        else:
            self.food_up_distance=0.0
            self.food_down_distance=0.0
        
    def reset(self):
        self.length = 2
        self.positions = [((screen_width/2), (screen_height/2))]
        self.direction = up
        self.score = 0
        self.down_closest_distance=20
        self.up_closest_distance=480
        self.right_closest_distance=480
        self.left_closest_distance=480

    def draw(self,surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (gridsize,gridsize))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (93,216, 228), r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)

class Food():
    def __init__(self):
        self.position = (0,0)
        self.color = (223, 163, 49)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, grid_width-1)*gridsize, random.randint(0, grid_height-1)*gridsize)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)

def drawGrid(surface):
    for y in range(0, int(grid_height)):
        for x in range(0, int(grid_width)):
            if (x+y)%2 == 0:
                r = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize))
                pygame.draw.rect(surface,(93,216,228), r)
            else:
                rr = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize))
                pygame.draw.rect(surface, (84,194,205), rr)

screen_width = 480
screen_height = 480

gridsize = 20
grid_width = screen_width/gridsize
grid_height = screen_height/gridsize

up = (0,-1)
down = (0,1)
left = (-1,0)
right = (1,0)

def main(genomes, config):
    pygame.init()
    myfont = pygame.font.SysFont("monospace",16)
    nets = []
    ge = []
    snakes = []
    foods =[]

    for _, g in genomes:  #genome is a tuple, id and the object
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        foods.append(Food())
        snakes.append(Snake(foods[-1]))
        g.fitness = 0
        ge.append(g)

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    run = True
    numberOfIterations=0
    while run:
        clock.tick(5) #at most 10 ticks at second.
        drawGrid(surface)
        numberOfIterations+=1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()    
        max_fitness=-2000
        best_individual=0
        for x, snake in enumerate(snakes):
            output = nets[x].activate((snake.dir_up, snake.dir_down, snake.dir_right, snake.dir_left, snake.up_closest_distance/480.0, snake.down_closest_distance/480.0, snake.right_closest_distance/480.0, snake.left_closest_distance/480.0, snake.food_up_distance/480.0, snake.food_down_distance/480.0, snake.food_right_distance/480.0, snake.food_left_distance/480.0))
            
            softmax_result=softmax(output)
            decision=np.argmax(((softmax_result / np.max(softmax_result)) == 1).astype(int))

            if decision==0:
                if snake.direction!=down and snake.food_up_distance<240.0:
                    ge[x].fitness+=0.5
                else:
                    ge[x].fitness-=0.3
                snake.turn(up)
            elif decision==1:
                if snake.direction!=up and snake.food_down_distance<240.0:
                    ge[x].fitness+=0.5
                else:
                    ge[x].fitness-=0.3
                snake.turn(down)
            elif decision==2:
                if snake.direction!=left and snake.food_right_distance<240.0:
                    ge[x].fitness+=0.5
                else:
                    ge[x].fitness-=0.3
                snake.turn(right)
            else:
                if snake.direction!=right and snake.food_left_distance<240.0:
                    ge[x].fitness+=0.5
                else:
                    ge[x].fitness-=0.3
                snake.turn(left)

            snake.move()
            ge[x].fitness-=0.2

            if ge[x].fitness>=max_fitness:
                max_fitness=ge[x].fitness
                best_individual=x

        for x, snake in enumerate(snakes):
            if snake.collide():
                ge[x].fitness-=1.0
                snakes.pop(x)
                foods.pop(x)
                nets.pop(x)
                ge.pop(x)
            elif snake.get_head_position() == foods[x].position:
                snake.length+=1
                ge[x].fitness+=20.0
                while True:
                    foods[x].randomize_position()
                    snake.food_position=foods[x].position
                    if snake.food_position not in snake.positions:
                        break

        if len(snakes)==0 or numberOfIterations==1200:
            run=False
            break

        snakes[best_individual].draw(surface)
        foods[best_individual].draw(surface)
        screen.blit(surface, (0, 0))
        text=myfont.render("fitness {0}".format(ge[best_individual].fitness), 1, (0,0,0))
        text1= myfont.render("up_closest_distance {0}".format(snakes[best_individual].up_closest_distance), 1, (0, 0, 0))
        text2= myfont.render("down_closest_distance {0}".format(snakes[best_individual].down_closest_distance), 1, (0, 0, 0))
        text3= myfont.render("right_closest_distance {0}".format(snakes[best_individual].right_closest_distance), 1, (0, 0, 0))
        text4= myfont.render("left_closest_distance {0}".format(snakes[best_individual].left_closest_distance), 1, (0, 0, 0))
        text5= myfont.render("food_up_distance {0}".format(snakes[best_individual].food_up_distance), 1, (0, 0, 0))
        text6= myfont.render("food_down_distance {0}".format(snakes[best_individual].food_down_distance), 1, (0, 0, 0))
        text7= myfont.render("food_right_distance {0}".format(snakes[best_individual].food_right_distance), 1, (0, 0, 0))
        text8= myfont.render("food_left_distance {0}".format(snakes[best_individual].food_left_distance), 1, (0, 0, 0))
        screen.blit(text, (5, 10))
        screen.blit(text1, (5, 20))
        screen.blit(text2, (5, 30))
        screen.blit(text3, (5, 40))
        screen.blit(text4, (5, 50))
        screen.blit(text5, (5, 60))
        screen.blit(text6, (5, 70))
        screen.blit(text7, (5, 80))
        screen.blit(text8, (5, 90))
        pygame.display.update()


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 10)

if __name__ == "__main__":
    local_dir=os.path.dirname(__file__)
    config_path=os.path.join(local_dir, "configuration.txt")
    run(config_path)
