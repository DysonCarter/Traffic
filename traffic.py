# traffic.py by Dyson carter

import pygame
import random
from car import Car
from strategy import Dumb, Nice, Selfish
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
border_width = 10
strategy = Nice

# Create window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Traffic Pattern Simulation")
clock = pygame.time.Clock()

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
cars = [Car(random.randint(0, lane_count), strategy) for _ in range(car_count)]

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
