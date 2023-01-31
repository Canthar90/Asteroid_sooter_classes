import pygame
import sys


# base setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1290, 720
clock = pygame.time.Clock()
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Asteroid shooter V2")


while True:
    
    dt = clock.tick(120)
    
    
    #inputs 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
            
            
            
    pygame.display.update()