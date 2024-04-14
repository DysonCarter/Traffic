import pygame
import random
from sys import exit

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Define constants
width = 1400
height = 200
lane_height = [50, 100, 150]

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
            elif car.speed <= car.initial_speed:
                car.speed += .01

# Nice Strategy Class
# Considerate of other cars - Only passes on the left - if the right lane is pretty open they'll get over
class Nice:
    def run_strategy(self, car, cars):
        will_collide = False
        should_pass = False
        right_good = True
        left_good = True

        # Check variables
        for other in cars:
            if car != other:
                # Check for imminent collision
                if car.will_collide(other) and not will_collide:
                    will_collide = True
                    collision_car = other

                # Check if car should pass soon
                if car.should_pass(other) and not should_pass:
                    should_pass = True

                # Check if you can move right
                if not car.right_side_very_clear(other) or car.y == lane_height[2]:
                    right_good = False

                # Check if you can move left
                if not car.left_side_clear(other) or car.y == lane_height[0]:
                    left_good = False

                # Break loop if all conditions are met
                if will_collide and should_pass and not right_good and not left_good:
                    break

        if will_collide:
            if car.speed >= collision_car.speed:
                car.speed = collision_car.speed
            car.speed -= .01
        elif should_pass and left_good:
            if car.speed < car.initial_speed:
                car.speed += .01
            car.merge_left()
        elif right_good:
            if car.speed < car.initial_speed:
                car.speed += .01
            car.merge_right() 
        elif should_pass and car.speed >= 1:
            car.speed -= .01
        elif not should_pass:
            if car.speed < car.initial_speed:
                car.speed = car.initial_speed
            
# Selfish Strategy Class
# Will only change lanes if they need to pass - Will pass on the right if neccessary         
class Selfish:
    def run_strategy(self, car, cars):
        will_collide = False
        should_pass = False
        right_good = True
        left_good = True

        # Iterate through cars
        for other in cars:
            if car != other:
                # Check for imminent collision
                if car.will_collide(other) and not will_collide:
                    will_collide = True
                    collision_car = other

                # Check if car should pass soon
                if car.should_pass(other) and not should_pass:
                    should_pass = True

                # Check if you can move right
                if not car.right_side_clear(other) or car.y == lane_height[2]:
                    right_good = False

                # Check if you can move left
                if not car.left_side_clear(other) or car.y == lane_height[0]:
                    left_good = False

                # Break loop if all conditions are met
                if will_collide and should_pass and not right_good and not left_good:
                    break

        if will_collide:
            if car.speed > collision_car.speed:
                car.speed = collision_car.speed
            car.speed -= .01
            return
        elif should_pass and left_good:
            if car.speed < car.initial_speed:
                car.speed += .01
            car.merge_left()
        elif should_pass and right_good:
            if car.speed < car.initial_speed:
                car.speed += .01
            car.merge_right() 
        elif should_pass and car.speed >= 1:
            car.speed -= .01
        elif not should_pass or not will_collide:
            if car.speed < car.initial_speed:
                car.speed += .01

# Segregated Strategy Class
# Selfish byt will high speed cars only use left 2 lanes and slow speed cars only use right 2 lanes         
class Segregated:
    def run_strategy(self, car, cars):
        will_collide = False
        should_pass = False
        right_good = True
        left_good = True
        slow = False
        fast = False

        # Iterate through cars
        if car.initial_speed >= 2.3:
            fast = True
            for other in cars:
                if car != other:
                    # Check for imminent collision
                    if car.will_collide(other) and not will_collide:
                        will_collide = True
                        collision_car = other

                    # Check if car should pass soon
                    if car.should_pass(other) and not should_pass:
                        should_pass = True

                    # Check if you can move right
                    if not car.right_side_clear(other) or car.y >= lane_height[1]:
                        right_good = False

                    # Check if you can move left
                    if not car.left_side_clear(other) or car.y == lane_height[0]:
                        left_good = False

                    # Break loop if all conditions are met
                    if will_collide and should_pass and not right_good and not left_good:
                        break
        elif car.initial_speed <= 1.7:
            slow = True
            for other in cars:
                if car != other:
                    # Check for imminent collision
                    if car.will_collide(other) and not will_collide:
                        will_collide = True
                        collision_car = other

                    # Check if car should pass soon
                    if car.should_pass(other) and not should_pass:
                        should_pass = True

                    # Check if you can move right
                    if not car.right_side_clear(other) or car.y == lane_height[2]:
                        right_good = False

                    # Check if you can move left
                    if not car.left_side_clear(other) or car.y <= lane_height[1]:
                        left_good = False

                    # Break loop if all conditions are met
                    if will_collide and should_pass and not right_good and not left_good:
                        break
        else:
            for other in cars:
                if car != other:
                    # Check for imminent collision
                    if car.will_collide(other) and not will_collide:
                        will_collide = True
                        collision_car = other

                    # Check if car should pass soon
                    if car.should_pass(other) and not should_pass:
                        should_pass = True

                    # Check if you can move right
                    if not car.right_side_clear(other) or car.y == lane_height[2]:
                        right_good = False

                    # Check if you can move left
                    if not car.left_side_clear(other) or car.y == lane_height[0]:
                        left_good = False

                    # Break loop if all conditions are met
                    if will_collide and should_pass and not right_good and not left_good:
                        break

        if will_collide:
            if car.speed > collision_car.speed:
                car.speed = collision_car.speed
            car.speed -= .01
            return
        elif (should_pass and left_good) or (fast and left_good and car.y > lane_height[1]):
            if car.speed < car.initial_speed:
                car.speed += .01
            car.merge_left()
        elif should_pass and right_good or (slow and right_good and car.y < lane_height[1]):
            if car.speed < car.initial_speed:
                car.speed += .01
            car.merge_right() 
        elif should_pass and car.speed >= 1:
            car.speed -= .01
        elif not should_pass or not will_collide:
            if car.speed < car.initial_speed:
                car.speed += .01

class Random:
    pass
