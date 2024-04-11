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
height = 400
lane_width = 5
lane_count = 2
lane_height = [50, 100, 150]
car_count = 8
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

# Define constants for the menu
menu_height = 200
menu_color = (50, 50, 50)
button_color = (100, 100, 100)
text_color = WHITE
button_width = 300
button_height = 150
button_margin = 20

# Function to draw menu
def draw_menu():
    pygame.draw.rect(screen, menu_color, (0, height - menu_height, width, menu_height))

    font = pygame.font.SysFont(None, 64)

    # Draw Reset button
    reset_button_rect = pygame.Rect(30, height - menu_height + button_margin, button_width, button_height)
    pygame.draw.rect(screen, (255,0,0), reset_button_rect)
    text_surface = font.render("Reset", True, text_color)
    text_rect = text_surface.get_rect(center=reset_button_rect.center)
    screen.blit(text_surface, text_rect)

# Function to handle button click events
def handle_menu_click(pos):
    global cars

    x, y = pos
    if height - menu_height <= y <= height:
        if 30 <= x <= 30 + button_width:
            # Reset simulation
            cars = [Car(random.randint(0, lane_count), strategy) for _ in range(car_count)]

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                handle_menu_click(event.pos)

    screen.fill(GRAY)  # Fill the screen with gray color
    draw_lanes()

    # Move and draw cars
    for car in cars:
        car.move()
        car.draw()
        car.strategy.run_strategy(car, cars)

    draw_menu()
    draw_border()

    pygame.display.update()
    clock.tick(100)

# Quit
pygame.quit()
exit()
