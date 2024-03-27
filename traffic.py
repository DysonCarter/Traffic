# traffic.py by Dyson carter

import pygame
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
lane_padding = 0

# Create window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Traffic Simulation")
clock = pygame.time.Clock()

# Function to draw lanes
def draw_lanes():
    lane_height = lane_width
    lane_offset = (height - lane_height * lane_count) // (lane_count + 1)
    for i in range(lane_count):
        lane_x = lane_padding
        lane_y = (i + 1) * lane_offset + i * lane_height
        pygame.draw.rect(screen, WHITE, (lane_x, lane_y, width - 2 * lane_padding, lane_height))


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(GRAY)  # Fill the screen with black color
    draw_lanes()  # Draw lanes

    pygame.display.update()
    clock.tick(60)

pygame.quit()
exit()
