# traffic.py by Dyson carter

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
car_count = 8
border_width = 10

# Create window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Traffic Pattern Simulation")
clock = pygame.time.Clock()

# Class for cars
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

    # Movement
    def move(self):
        # Move horizontally
        self.x += self.speed
        if self.x > width:
            self.x = 0
    def merge_left(self):
        self.y -= 2
    def merge_right(self):
        self.y += 2

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

        return (other.y <= self.y) or (other.y > self.y + 50) or (distance > (200 + (200 * (speed_difference))) and (reverse_distance > (100 - (speed_difference * 50))))
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

        return (other.y >= self.y) or (other.y < self.y + 50) or (distance > (200 + (200 * (speed_difference))) and (reverse_distance > (100 - (speed_difference * 50))))
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

        return (other.y <= self.y) or (other.y > self.y + 50) or (distance > (50 + 100 * (self.speed - other.speed)) and reverse_distance > 50)
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

        return (other.y >= self.y) or (other.y < self.y - 50) or (distance > (50 + 100 * (self.speed - other.speed)) and reverse_distance > 50)

    # Checks if car will hit the car in front of it
    def will_collide(self, other):
        if self.speed <= other.speed:
            return False

        # Calculate distance considering looping
        if self.x <= other.x:
            distance = other.x - self.x
        else:
            distance = width - self.x + other.x

        if distance <= 50 and ( self.y + 50 > other.y > self.y - 50):
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

        if distance <= (100 * (self.initial_speed - other.speed)+50) and ( self.y + 50 > other.y > self.y - 50):
            return True
        return False

    # Draws the car
    def draw(self):
        pygame.draw.circle(screen, (85 * self.initial_speed, 0,0), (int(self.x), int(self.y)), car_radius)

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
# TODO Fix Logic so they dont jump like a bunny when merging right                
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
cars = [Car(random.randint(0, lane_count), Selfish) for _ in range(car_count)]

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
