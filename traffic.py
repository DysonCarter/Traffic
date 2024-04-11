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
GREEN = (0, 255, 0)

# Define constants
width = 1400
height = 400
lane_width = 5
lane_count = 2
lane_height = [50, 100, 150]
car_count = 8
border_width = 10
running = True
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

# Car count slider constants
slider_bar_width = 20
slider_bar_height = 100
slider_button_width = 40
slider_button_height = 20
slider_color = (100, 100, 100)
slider_button_color = GREEN

# Car count slider variables
slider_width = 40  # Width of the slider bar and slider button combined
slider_x = button_width + 75
slider_y = height - menu_height + (menu_height - slider_bar_height) // 2  # Position the slider in the middle of the menu vertically
slider_value = 8  # Initial value for the slider
max_slider_value = 30

# Function to draw menu
def draw_menu():
    pygame.draw.rect(screen, menu_color, (0, height - menu_height, width, menu_height))

    font = pygame.font.SysFont(None, 64)

    # Draw Reset button
    reset_button_rect = pygame.Rect(30, height - menu_height + button_margin, button_width, button_height)
    pygame.draw.rect(screen, (255, 0, 0), reset_button_rect)
    text_surface = font.render("Reset", True, text_color)
    text_rect = text_surface.get_rect(center=reset_button_rect.center)
    screen.blit(text_surface, text_rect)

    # Draw Car Count Slider
    pygame.draw.rect(screen, slider_color, (slider_x, slider_y, slider_bar_width, slider_bar_height))
    slider_button_rect = pygame.Rect(slider_x - (slider_button_width - slider_bar_width) / 2, 
                                     slider_y + (slider_value / max_slider_value) * (slider_bar_height - slider_button_height), 
                                     slider_button_width, slider_button_height)
    pygame.draw.rect(screen, slider_button_color, slider_button_rect)

# Function to handle mouse click events
def handle_menu_click(pos):
    global cars, slider_value

    x, y = pos
    if height - menu_height <= y <= height:
        if 30 <= x <= 30 + button_width:
            # Reset simulation
            cars = [Car(random.randint(0, lane_count), strategy) for _ in range(slider_value)]
        elif slider_x <= x <= slider_x + slider_bar_width and slider_y <= y <= slider_y + slider_bar_height:
            slider_value = min(max(int((y - slider_y) / slider_bar_height * max_slider_value), 1), max_slider_value)

# Function to handle mouse drag events
def handle_mouse_drag(pos):
    global slider_value

    x, y = pos
    if slider_x <= x <= slider_x + slider_bar_width and slider_y <= y <= slider_y + slider_bar_height:
        # Calculate slider value based on mouse position
        slider_value = min(max(int((y - slider_y) / slider_bar_height * max_slider_value), 1), max_slider_value)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                handle_menu_click(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0] == 1:
                handle_mouse_drag(event.pos)

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
