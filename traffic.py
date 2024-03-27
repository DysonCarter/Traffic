# traffic.py by Dyson Carter

import pygame

pygame.init()

# Make Window
width = 1000
height = 500
screen = pygame.display.set_mode((width, height))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    pygame.display.update()