import pygame
import sys



pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1290, 720

clock = pygame.time.Clock()

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))



while True:
    
    dt = clock.tick(120)
    
    
    #inputs 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
            
            
            
    pygame.display.update()