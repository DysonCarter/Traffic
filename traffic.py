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
lane1_height = height * .15
lane2_height = height * .50
lane3_height = height * .85
lane_height = [height * .15, height * .5, height * .85]
car_radius = 10
car_count = 10

# Create window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Traffic Pattern Simulation")
clock = pygame.time.Clock()

# Class for cars
class Car:
    def __init__(self, lane, strategy):
        # Pick a Lane
        lane = random.randint(1,3)
        if lane == 1:
            self.y = lane1_height
        elif lane == 2:
            self.y = lane2_height
        else:
            self.y = lane3_height
            
        self.lane = lane
        self.x = random.randint(0, int(width * 1))
        self.initial_speed = random.uniform(1, 3)  # Random initial speed
        self.speed = self.initial_speed
        self.strategy = strategy()
        self.lane_change_delay = 30  # Delay in frames before another lane change is allowed
        self.lane_change_timer = 0    # Timer to track the delay
        self.lane_change_step = 1     # Step size for lane change

    def move(self):
        # Move horizontally
        self.x += self.speed
        if self.x > width:
            self.x = 0

    def draw(self):
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), car_radius)

    # Checks if car will hit the car in front of it
    def will_collide(self, other_car):
        if self.speed <= other_car.speed:
            return False

        # Calculate distance considering looping
        if self.x <= other_car.x:
            distance = other_car.x - self.x
        else:
            distance = width - self.x + other_car.x

        if distance <= 100 and ( self.y + 50 > other_car.y > self.y - 50):
            return True
        return False

    
    # Checks to see if lane change can commence
    # Returns true if it is ok, returns false if the other car is there
    def check_left_mirror(self, other_car):
        if other_car.lane != (self.lane - 1):
            return True

        # Calculate distance considering screen looping
        if self.x <= other_car.x:
            distance_x = other_car.x - self.x
        else:
            distance_x = width - self.x + other_car.x

        if self.y <= other_car.y:
            distance_y = other_car.y - self.y
        else:
            distance_y = height - self.y + other_car.y

        if distance_x <= 200 and distance_y <= 200:
            return False

        return True

    def check_right_mirror(self, other_car):
        if other_car.lane != (self.lane + 1):
            return True

        # Calculate distance considering screen looping
        if self.x <= other_car.x:
            distance_x = other_car.x - self.x
        else:
            distance_x = width - self.x + other_car.x

        if self.y <= other_car.y:
            distance_y = other_car.y - self.y
        else:
            distance_y = height - self.y + other_car.y

        if distance_x <= 200 and distance_y <= 200:
            return False

        return True
    
    def try_lane_change_left(self):
        if self.lane == 1 or self.lane_change_timer > 0:
            return
        target_lane = self.lane - 1
        if self.y > lane_height[target_lane - 1]:
            self.y -= self.lane_change_step
        else:
            self.lane -= 1
            self.lane_change_timer = self.lane_change_delay  # Start the delay timer

    def try_lane_change_right(self):
        if self.lane == 3 or self.lane_change_timer > 0:
            return
        target_lane = self.lane + 1
        if self.y < lane_height[target_lane - 1]:
            self.y += self.lane_change_step
        else:
            self.lane += 1
            self.lane_change_timer = self.lane_change_delay  # Start the delay timer

    def update_lane_change_timer(self):
        if self.lane_change_timer > 0:
            self.lane_change_timer -= 1

# Basic Strategy Class
# Grin and Bare it Strategy - No Changing Lanes
class BasicStrategy: 
    def run_strategy(self, car, cars):
        for other_car in cars:
            if car.will_collide(other_car) and (car != other_car):
                car.speed = other_car.speed
                break

class NiceStrategy:
    def run_strategy(self, car, cars):
        right_lane_good = True
        left_lane_good = True
        for other_car in cars:
            if not car.check_right_mirror(other_car):
                right_lane_good = False
            if not car.check_left_mirror(other_car):
                left_lane_good = False
        if right_lane_good:
            car.try_lane_change_right()

        for other_car in cars:
            if car.will_collide(other_car) and (car != other_car):
                if left_lane_good:
                    car.try_lane_change_left()
                else:
                    car.speed = other_car.speed
                break

# Function to draw lanes
def draw_lanes():
    lane_height = lane_width
    lane_offset = (height - lane_height * lane_count) // (lane_count + 1)
    for i in range(lane_count):
        lane_x = 0
        lane_y = (i + 1) * lane_offset + i * lane_height
        pygame.draw.rect(screen, WHITE, (lane_x, lane_y, width, lane_height))

# Create all cars
cars = [Car(random.randint(1, lane_count), BasicStrategy) for _ in range(car_count)]

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
        car.update_lane_change_timer()

    pygame.display.update()
    clock.tick(60)

# Quit
pygame.quit()
exit()
