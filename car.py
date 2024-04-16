# Class for cars
import pygame
import random

from strategy import Selfish, Nice, Dumb

# Define constants
width = 1400
height = 200
lane_width = 5
lane_count = 2
lane_height = [50, 100, 150]
car_radius = 19
car_count = 15
border_width = 10
collision_distance = 50
clear_distance = 150

# Create window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Traffic Pattern Simulation")
clock = pygame.time.Clock()

class Car:
    # Construction
    def __init__(self, lane, strategy):
        if lane == 0:
            self.y = lane_height[0]
        elif lane == 1:
            self.y = lane_height[1]
        else:
            self.y = lane_height[2]
            
        self.lane = lane
        self.x = random.randint(0, int(width * 1)) # width * percent of screen to spawn in
        self.initial_speed = random.uniform(1, 3)  # Random initial speed
        self.speed = self.initial_speed
        self.strategy = strategy()
        self.strategyName = str(strategy)

    # Movement
    def move(self):
        # Move horizontally
        self.x += self.speed*2
        if self.x > width:
            self.x = 0
    def merge_left(self):
        self.y -= 5
    def merge_right(self):
        self.y += 5

    # Lane checks
    # Very Clear
    def right_side_very_clear(self, other):
        # Difference in speed // How much faster the car is compared to other
        # Max speed is 3 and Min speed is 1 so 
        # Max diff is 2 and Min Diff is -2
        speed_difference = self.speed - other.speed

        # Calculate distance considering looping
        if self.x <= other.x:
            distance = other.x - self.x
        else:
            distance = width - self.x + other.x

        if other.x <= self.x:
            reverse_distance = self.x - other.x
        else:
            reverse_distance = width - other.x + self.x

        if speed_difference > 0:
            return (other.y <= self.y) or (other.y > self.y + 50) or ((distance > clear_distance*1.5) and (reverse_distance > collision_distance))
        else:
            return (other.y <= self.y) or (other.y > self.y + 50) or ((distance > collision_distance) and (reverse_distance > clear_distance*1.5))
    def left_side_very_clear(self, other):
        # Difference in speed // How much faster the car is compared to other
        # Max speed is 3 and Min speed is 1 so 
        # Max diff is 2 and Min Diff is -2
        speed_difference = self.speed - other.speed

        # Calculate distance considering looping
        if self.x <= other.x:
            distance = other.x - self.x
        else:
            distance = width - self.x + other.x

        if other.x <= self.x:
            reverse_distance = self.x - other.x
        else:
            reverse_distance = width - other.x + self.x

        if speed_difference > 0:
            return (other.y >= self.y) or (other.y < self.y + 50) or ((distance > 300) and (reverse_distance > collision_distance))
        else:
            return (other.y >= self.y) or (other.y < self.y + 50) or ((distance > collision_distance) and (reverse_distance > 300))
    # Good to pass
    def right_side_clear(self, other):
        # Difference in speed // How much faster the car is compared to other
        # Max speed is 3 and Min speed is 1 so 
        # Max diff is 2 and Min Diff is -2
        speed_difference = self.speed - other.speed

        # Calculate distance considering looping
        if self.x <= other.x:
            distance = other.x - self.x
        else:
            distance = width - self.x + other.x

        if other.x <= self.x:
            reverse_distance = self.x - other.x
        else:
            reverse_distance = width - other.x + self.x

        # return (other.y <= self.y) or (other.y > self.y + 50) or (distance > (50 + 100 * (self.speed - other.speed)) and reverse_distance > 50)
        if speed_difference > 0:
            return (other.y <= self.y) or (other.y > self.y + 50) or ((distance > clear_distance) and (reverse_distance > collision_distance))
        else:
            return (other.y <= self.y) or (other.y > self.y + 50) or (((distance > collision_distance) and (reverse_distance > clear_distance)))
    def left_side_clear(self, other):
        # Difference in speed // How much faster the car is compared to other
        # Max speed is 3 and Min speed is 1 so 
        # Max diff is 2 and Min Diff is -2
        speed_difference = self.speed - other.speed

        # Calculate distance considering looping
        if self.x <= other.x:
            distance = other.x - self.x
        else:
            distance = width - self.x + other.x

        if other.x <= self.x:
            reverse_distance = self.x - other.x
        else:
            reverse_distance = width - other.x + self.x

        # return (other.y >= self.y) or (other.y < self.y - 50) or (distance > (50 + 100 * (self.speed - other.speed)) and reverse_distance > 50)
        if speed_difference > 0:
            return (other.y >= self.y) or (other.y < self.y - 50) or ((distance > clear_distance) and reverse_distance > collision_distance)
        else:
            return (other.y >= self.y) or (other.y < self.y - 50) or ((distance > collision_distance) and reverse_distance > clear_distance)

    # Checks if car will hit the car in front of it
    def will_collide(self, other):
        if self.speed <= other.speed:
            return False

        # Calculate distance considering looping
        if self.x <= other.x:
            distance = other.x - self.x
        else:
            distance = width - self.x + other.x

        if distance <= collision_distance and ( self.y + 50 > other.y > self.y - 50):
            return True
        return False

    # Wants to pass
    def should_pass(self, other):
        if self.initial_speed <= other.speed:
            return False

        # Calculate distance considering looping
        if self.x <= other.x:
            distance = other.x - self.x
        else:
            distance = width - self.x + other.x

        # if distance <= (100 * (self.initial_speed - other.speed)+50) and ( self.y + 50 > other.y > self.y - 50):
        if distance <= clear_distance and ( self.y + 50 > other.y > self.y - 50):
            return True
        return False

    # Draws the car
    def draw(self):
        if self.strategyName == "<class 'strategy.Selfish'>":
            color = (85 * self.initial_speed, 0, 0)
        elif self.strategyName == "<class 'strategy.Nice'>":
            color = (0, 30 * self.initial_speed, 85 * self.initial_speed)     
        elif self.strategyName == "<class 'strategy.Dumb'>":
            color = (40 * self.initial_speed, 30 * self.initial_speed, 10 * self.initial_speed)
        else:
            color = (self.initial_speed * 40, 0, self.initial_speed*85)  # Purplegit

        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), car_radius)
