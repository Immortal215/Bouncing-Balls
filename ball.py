import pymunk
import pygame
import random
import math

pygame.init()

display = pygame.display.set_mode([600, 600])
clock = pygame.time.Clock()
space = pymunk.Space()
FPS = 60 # how fast it will run 

white = (255, 255, 255)
black = (0, 0, 0)
ball_count = 2 # change count to what you need                                     

space.gravity = (0, -300) # gravity, change second number for a stronger gravity 

def convert_coordinates(points):
    return int(points[0]), 600 - int(points[1])

class Ball():
    def __init__(self, x, y, collision_type):               
        # ball with gravity and collisions and bounciness 
        self.body = pymunk.Body(mass=1, moment=pymunk.moment_for_circle(1, 0, 10))
        self.body.position = x, y
        self.body.velocity = random.randint(-200, 200), -200 # x and y velocity of new balls                                                                                                             
        self.shape = pymunk.Circle(self.body, 5) # if you want to change ball size, change this radius and line 36
        self.shape.elasticity = 1 # bounciness
        self.shape.density = 1
        self.shape.collision_type = collision_type
        space.add(self.body, self.shape)
        
    def draw(self):
        pygame.draw.circle(display, black, convert_coordinates(self.body.position), 5) #  if you want to change ball size, change this radius and line 28

class Open_Circle():
    def __init__(self, collision_type, start_angle=0, end_angle=math.pi*2):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = 300, 300 
        
        self.segments = []
        self.radius = 250
        num_segments = 1000 # too many and it will lag 

        # create a circle using lines
        for i in range(num_segments):
            angle1 = start_angle + (end_angle - start_angle) * i / num_segments
            angle2 = start_angle + (end_angle - start_angle) * (i + 1) / num_segments

            p1 = (self.radius * math.cos(angle1), self.radius * math.sin(angle1))
            p2 = (self.radius * math.cos(angle2), self.radius * math.sin(angle2))

            segment = pymunk.Segment(self.body, p1, p2, 5)
            segment.elasticity = 1
            segment.collision_type = collision_type
            self.segments.append(segment)

        space.add(self.body, *self.segments)
    
    def draw(self):
        for segment in self.segments:
            p1 = convert_coordinates(segment.a + self.body.position)
            p2 = convert_coordinates(segment.b + self.body.position)
            pygame.draw.line(display, black, p1, p2, 5)

# organizes x point of balls to be in an order of equal divisions
rangesx = []
value = 425/min(ball_count, 10) 
for i in range((ball_count) // 10 + 1):
    for i in range(min(ball_count, 10)):
            rangesx.append(105 + (value * (i)))

# organizes y point of balls to make sure they are on seperate lines
rangesy = [] 
numberInBalls = 0
for i in range((ball_count) // 10 + 1):
    for i in range(min(ball_count, 10)):
        rangesy.append(400 - (50 * (numberInBalls)))
    numberInBalls += 1 
     
balls = [Ball(rangesx[i], rangesy[i], 2) for i in range(ball_count)] # first balls created 

# on collide, create new ball
def collide(arbiter, space, data):
    global ball_count
    
    if ball_count < 500: # change if you wanna crash your pc, sets a limit on the amount of balls you want to add 
        ball_count += 1
        if len(balls) < ball_count:
            balls.append(Ball(random.randint(100, 500), 450, 2)) 
            return True

def game():   
    open_circle = Open_Circle(1)  

    handler = space.add_collision_handler(2, 2) # any ball can collide with another ball, 2 is collision_type for ball
    handler.post_solve = collide # after colliding, specifically only balls, will run this function

    handler = space.add_wildcard_collision_handler(1) # everything collides with circle, 1 is collision_type for circle
    
    while True:            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
        
        display.fill(white)
        [ball.draw() for ball in balls]
        open_circle.draw()
        pygame.display.update()

        clock.tick(FPS)
        space.step(1/FPS)
        
        
game()
