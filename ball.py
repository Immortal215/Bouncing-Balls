import pymunk
import pygame
import random
import math

pygame.init()

display = pygame.display.set_mode([600, 600])
clock = pygame.time.Clock()
space = pymunk.Space()
FPS = 60

white = (255, 255, 255)
black = (0, 0, 0)
ball_count = 2

space.gravity = (0, -200)

def convert_coordinates(points):
    return int(points[0]), 600 - int(points[1])

class Ball():
    def __init__(self, x, y, collision_type):
        self.body = pymunk.Body(mass=1, moment=pymunk.moment_for_circle(1, 0, 10))
        self.body.position = x, y
        self.body.velocity = random.randint(-400, 400), random.randint(-400, 400)
        self.shape = pymunk.Circle(self.body, 5)
        self.shape.elasticity = 1
        self.shape.density = 1
        self.shape.collision_type = collision_type
        space.add(self.body, self.shape)

    def draw(self):
        pygame.draw.circle(display, black, convert_coordinates(self.body.position), 5)

class Open_Circle():
    def __init__(self, collision_type, start_angle=0, end_angle=math.pi*2):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = 300, 300 
        
        self.segments = []
        self.radius = 250
        num_segments = 5000 

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
            
balls = [Ball(200 * (i+1), 200 * (i+1), 2) for i in range(2)] 

def collide(arbiter, space, data):
    global ball_count
    
    if ball_count < 500:
        ball_count += 1
        if len(balls) < ball_count:
            balls.append(Ball(random.randint(150, 400), random.randint(100, 400), 2)) 
            return True

def game():   
    open_circle = Open_Circle(1)  
    
    handler = space.add_collision_handler(2, 2)
    handler.post_solve = collide

    handler = space.add_wildcard_collision_handler(1)
    
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
