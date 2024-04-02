# traffic.py by Dyson carter

import pygame
import random
from car import Car
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
car_count = 15
border_width = 10

# Create window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Traffic Pattern Simulation")
clock = pygame.time.Clock()

# Basic Strategy Class
# Grin and Bare it Strategy - No Changing Lanes
class Dumb: 
    def run_strategy(self, car, cars):
        for other in cars:
            if car.will_collide(other) and (car != other):
                car.speed = other.speed
                break

# Nice Strategy Class
# Considerate of other cars - Only passes on the left - if the right lane is pretty open they'll get over
class Nice:
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
            if not car.right_side_very_clear(other) or car.y == lane_height[2]:
                right_good = False
                break
        # Check if you can move left
        for other in cars:
            if not car.left_side_clear(other) or car.y == lane_height[0]:
                left_good = False
                break

        if will_collide:
            if car.speed > collision_car.speed:
                car.speed = collision_car.speed
            car.speed -= .01
        elif should_pass and left_good:
            if not car.speed == car.initial_speed:
                car.speed += .01
            car.merge_left()
        elif right_good:
            if not car.speed == car.initial_speed:
                car.speed += .01
            car.merge_right() 
        elif not should_pass:
            if not car.speed == car.initial_speed:
                car.speed = car.initial_speed
            
# Selfish Strategy Class
# Will only change lanes if they need to pass - Will pass on the right if neccessary         
class Selfish:
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
            if car.speed > collision_car.speed:
                car.speed = collision_car.speed
            car.speed -= .01
            return
        elif should_pass and left_good:
            if not car.speed == car.initial_speed:
                car.speed += .01
            car.merge_left()
        elif should_pass and right_good:
            if not car.speed == car.initial_speed:
                car.speed += .01
            car.merge_right() 
        elif not should_pass:
            if not car.speed == car.initial_speed:
                car.speed = car.initial_speed

# Function to draw lanes
def draw_lanes():
    lane_heights = [75, 125]  # Heights for the two lanes
    lane_width = 5  # Width of each lane

    for lane_y in lane_heights:
        # Draw the lane rectangle
        pygame.draw.rect(screen, WHITE, (0, lane_y - lane_width // 2, width, lane_width))

def draw_border():
    # Draw the black border around the screen
    pygame.draw.rect(screen, BLACK, (0, 0, width, border_width))  # Top border
    pygame.draw.rect(screen, BLACK, (0, height - border_width, width, border_width))  # Bottom border
    pygame.draw.rect(screen, BLACK, (0, 0, border_width, height))  # Left border
    pygame.draw.rect(screen, BLACK, (width - border_width, 0, border_width, height))

# Create all cars
cars = [Car(random.randint(0, lane_count), Nice) for _ in range(car_count)]

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

    draw_border()

    pygame.display.update()
    clock.tick(100)

# Quit
pygame.quit()
exit()
