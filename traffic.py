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
lane1_height = height * .15
lane2_height = height * .50
lane3_height = height * .85
car_radius = 10
car_count = 10

# Create window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Traffic Pattern Simulation")
clock = pygame.time.Clock()

class Car:
    def __init__(self, lane):
        # Pick a Lane
        lane = random.randint(1,3)
        if lane == 1:
            self.y = lane1_height
        elif lane == 2:
            self.y = lane2_height
        else:
            self.y = lane3_height
            
        self.lane = lane
        self.x = random.randint(0, int(width * 0.10))
        self.speed = random.uniform(0.1, 0.5)  # Random initial speed

    def move(self):
        # Move horizontally
        self.x += self.speed
        if self.x > width:
            self.x = 0

    def draw(self):
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), car_radius)

# Function to draw lanes
def draw_lanes():
    lane_height = lane_width
    lane_offset = (height - lane_height * lane_count) // (lane_count + 1)
    for i in range(lane_count):
        lane_x = i * lane_width
        lane_y = (i + 1) * lane_offset + i * lane_height
        pygame.draw.rect(screen, WHITE, (lane_x, lane_y, width, lane_height))

cars = [Car(random.randint(1, lane_count)) for _ in range(car_count)]
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
        # car.move()
        car.draw()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
exit()
