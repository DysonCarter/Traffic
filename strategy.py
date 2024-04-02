import pygame
import random
from car import Car
from sys import exit

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
                car.speed += .001
            car.merge_left()
        elif should_pass and right_good:
            if not car.speed == car.initial_speed:
                car.speed += .001
            car.merge_right() 
        elif not should_pass:
            if car.speed < car.initial_speed:
                car.speed += .01
