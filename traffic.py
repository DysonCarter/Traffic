# traffic.py by Dyson carter

'''
TODO:
CHANGE Methods of mirror checks and will collide to only check if a car is in that area, relegate speed checks to the strategies.
also we should not compare lanes between two cars
'''

import pygame
import random
from sys import exit

pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Define constants
width = 1400
height = 200
lane_width = 5
lane_count = 2
lane1_height = 200 * .15
lane2_height = 200 * .50
lane3_height = 200 * .85
lane_height = [height * .15, height * .5, height * .85]
car_radius = 10
car_count = 15

# Create window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Traffic Pattern Simulation")
clock = pygame.time.Clock()

# Class for cars
class Car:
    def __init__(self, strategy):
        # Pick a Lane
        lane = random.randint(0, lane_count)
        if lane == 1:
            self.y = lane1_height
        elif lane == 2:
            self.y = lane2_height
        else:
            self.y = lane3_height
            
        self.lane = lane
        self.x = random.randint(0, int(width * 1)) # width * percent of screen to spawn in
        self.initial_speed = random.uniform(1, 3)  # Random initial speed
        self.speed = self.initial_speed
        self.strategy = strategy()

    def move(self):
        # Move horizontally
        self.x += self.speed
        if self.x > width:
            self.x = 0
    def merge_left(self):
        self.y -= 1
    def merge_right(self):
        self.y += 1

    def right_side_clear(self, other):
        # Calculate distance considering looping
        if self.x <= other.x:
            distance = other.x - self.x
        else:
            distance = width - self.x + other.x
        return (other.y <= self.y) or (distance >= 70)
    def left_side_clear(self, other):
        # Calculate distance considering looping
        if self.x <= other.x:
            distance = other.x - self.x
        else:
            distance = width - self.x + other.x
        return (other.y >= self.y) or (distance >= 70)

    # Checks if car will hit the car in front of it
    def will_collide(self, other):
        if self.speed <= other.speed:
            return False

        # Calculate distance considering looping
        if self.x <= other.x:
            distance = other.x - self.x
        else:
            distance = width - self.x + other.x

        if distance <= 70 and ( self.y + 50 > other.y > self.y - 50):
            return True
        return False
    
    def draw(self):
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), car_radius)

# Basic Strategy Class
# Grin and Bare it Strategy - No Changing Lanes
class BasicStrategy: 
    def run_strategy(self, car, cars):
        for other in cars:
            if car.will_collide(other) and (car != other):
                car.speed = other.speed
                break

class NiceStrategy:
    def run_strategy(self, car, cars):
        right_good = True
        for other in cars:
            if car.will_collide(other) and (car != other):
                car.speed = other.speed
                break
        for other in cars:
            if not car.right_side_clear(other) or car.y == lane_height[2]:
                right_good = False
                break
        if right_good:
            car.merge_right()

# Function to draw lanes
def draw_lanes():
    lane_height = lane_width
    lane_offset = (height - lane_height * lane_count) // (lane_count + 1)
    for i in range(lane_count):
        lane_x = 0
        lane_y = (i + 1) * lane_offset + i * lane_height
        pygame.draw.rect(screen, WHITE, (lane_x, lane_y, width, lane_height))

# Create all cars
cars = [Car(NiceStrategy) for _ in range(car_count)]

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(GRAY)  # Fill the screen with black color
    draw_lanes()  # Draw lanes

    # Move and draw cars
    for car in cars:
        car.move()
        car.draw()
        car.strategy.run_strategy(car, cars)

    pygame.display.update()
    clock.tick(60)

# Quit
pygame.quit()
exit()
