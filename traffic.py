# traffic.py by Dyson Carter

import pygame
from sys import exit

pygame.init()

# Make Window
width = 1000
height = 500
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
    clock.tick(60);
