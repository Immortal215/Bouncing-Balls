import pymunk
import pygame
import random
import math

pygame.init()

display = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
space = pymunk.Space()
FPS = 60

white = (255, 255, 255)
black = (0, 0, 0)
ball_count = 2

def convert_coordinates(points):
    return int(points[0]), 600 - int(points[1])

class Ball():
    def __init__(self, x, y, collision_type):
        self.body = pymunk.Body()
        self.body.position = x, y
        self.body.velocity = random.uniform(-0.05, 0.05), random.uniform(-0.05, 0.05)
        self.shape = pymunk.Circle(self.body, 10)
        self.shape.elasticity = 1
        self.shape.density = 10
        self.shape.collision_type = collision_type
        space.add(self.body, self.shape)

    def draw(self):
        pygame.draw.circle(display, black, convert_coordinates(self.body.position), 10)

class Open_Circle():
    def __init__(self, collision_type, start_angle=0, end_angle=math.pi*2):
        # Create a static body at the center
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = 300, 300  # Center of the circle
        
        # Define the arc as a series of segments
        self.segments = []
        self.radius = 250
        num_segments = 250  # Number of segments to approximate the arc

        for i in range(num_segments):
            angle1 = start_angle + (end_angle - start_angle) * i / num_segments
            angle2 = start_angle + (end_angle - start_angle) * (i + 1) / num_segments

            p1 = (self.radius * math.cos(angle1), self.radius * math.sin(angle1))
            p2 = (self.radius * math.cos(angle2), self.radius * math.sin(angle2))

            segment = pymunk.Segment(self.body, p1, p2, 5)
            segment.elasticity = 1
            segment.collision_type = collision_type
            self.segments.append(segment)

        # Add all segments to the space
        space.add(self.body, *self.segments)
    
    def draw(self):
        for segment in self.segments:
            p1 = convert_coordinates(segment.a + self.body.position)
            p2 = convert_coordinates(segment.b + self.body.position)
            pygame.draw.line(display, black, p1, p2, 5)

def collide(arbiter, space, data):
    global ball_count
    
    if ball_count < 50:
        ball_count += 1
        return True

def game():   

    open_circle = Open_Circle(1)  # Use the Open_Circle class
    
    # Set up the collision handler to handle collisions between balls and the arc
    handler = space.add_collision_handler(1, 2)
    handler = space.add_wildcard_collision_handler(2)
    handler.separate = collide
    while True:
        balls = []
        for _ in range(ball_count):
            while True:
                x = random.randint(50, 550)
                y = random.randint(50, 550)
                if (x - 300) ** 2 + (y - 300) ** 2 <= 250 ** 2:
                    balls.append(Ball(x, y, 2))
                    break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        display.fill(white)
        [ball.draw() for ball in balls]
        open_circle.draw()
        
        pygame.display.update()
        clock.tick(FPS)
        space.step(1/FPS)
        
game()
pygame.quit()
