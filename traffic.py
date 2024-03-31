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
lane_height = [50, 100, 150]
car_radius = 10
car_count = 7

# Create window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Traffic Pattern Simulation")
clock = pygame.time.Clock()

# Class for cars
class Car:
    def __init__(self, lane, strategy):
        if lane == 0:
            self.y = lane_height[0]
        elif lane == 1:
            self.y = lane_height[1]
        else:
            self.y = lane_height[2]
            
        self.lane = lane
        self.x = random.randint(0, int(width * .4)) # width * percent of screen to spawn in
        self.initial_speed = random.uniform(1, 3)  # Random initial speed
        self.speed = self.initial_speed
        self.strategy = strategy()

    def move(self):
        # Move horizontally
        self.x += self.speed
        if self.x > width:
            self.x = 0
    def merge_left(self):
        self.y -= 2
    def merge_right(self):
        self.y += 2

    def right_side_clear(self, other):
        # Calculate distance considering looping
        if self.x <= other.x:
            distance = other.x - self.x
        else:
            distance = width - self.x + other.x

        if other.x <= self.x:
            reverse_distance = self.x - other.x
        else:
            reverse_distance = width - other.x + self.x

        return (other.y <= self.y) or (other.y > self.y + 50) or ((distance > 100) and (reverse_distance > 70))
    def left_side_clear(self, other):
        # Calculate distance considering looping
        if self.x <= other.x:
            distance = other.x - self.x
        else:
            distance = width - self.x + other.x

        if other.x <= self.x:
            reverse_distance = self.x - other.x
        else:
            reverse_distance = width - other.x + self.x

        return (other.y >= self.y) or (other.y < self.y - 50) or ((distance > 100) and (reverse_distance > 70))

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

    def should_pass(self, other):
        if self.initial_speed < other.speed:
            return False

        # Calculate distance considering looping
        if self.x <= other.x:
            distance = other.x - self.x
        else:
            distance = width - self.x + other.x

        if distance <= (100 * self.initial_speed) and ( self.y + 50 > other.y > self.y - 50):
            return True
        return False

    def draw(self):
        pygame.draw.circle(screen, (85 * self.initial_speed, 0,0), (int(self.x), int(self.y)), car_radius)

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
        will_collide = False
        should_pass = False
        right_good = True
        left_good = True

        # Check for soon collision
        for other in cars:
            if car.will_collide(other) and (car != other):
                will_collide = True
                collision_car = other
                break
        # Check if car should pass soon
        for other in cars:
            if car.should_pass(other) and (car != other):
                should_pass = True
                break
        # Check if you can move right
        for other in cars:
            if not car.right_side_clear(other) or car.y == lane_height[2]:
                right_good = False
                break
        # Check if you can move left
        for other in cars:
            if not car.left_side_clear(other) or car.y == lane_height[0]:
                left_good = False
                break

        if will_collide:
            car.speed = collision_car.speed
        if should_pass and left_good:
            car.speed = car.initial_speed
            car.merge_left()
        elif right_good:
            car.merge_right()  
            
# Function to draw lanes
def draw_lanes():
    lane_heights = [75, 125]  # Heights for the two lanes
    for i, lane_y in enumerate(lane_heights):
        pygame.draw.rect(screen, WHITE, (0, lane_y - lane_width // 2, width, lane_width))



# Create all cars
cars = [Car(random.randint(0, lane_count), NiceStrategy) for _ in range(car_count)]

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
