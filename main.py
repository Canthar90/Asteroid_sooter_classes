import pygame
import sys
import random


class Ship(pygame.sprite.Sprite):
    """Creates ship sprite object"""
    def __init__(self, groups):
        super().__init__(groups)
        
        self.image = pygame.image.load("images\spaceship.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80,90))
        self.rect = self.image.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT-100))
        self.can_shoot = True
        self.shoot_time = 0
        self.mask = pygame.mask.from_surface(self.image)
        
    def input_position(self):
        pos = pygame.mouse.get_pos()
        pos_x = pos[0]
        if pos_x > 20 and pos_x < WINDOW_WIDTH -20 and  self.rect.centerx != pos_x:
            if pos_x > self.rect.centerx:
                if pos_x - self.rect.centerx > 4 or pos_x - self.rect.centerx < -4:
                    self.rect.centerx += 4
                else:
                    self.rect.centerx += 1
            else:
                if pos_x - self.rect.centerx > 4 or pos_x - self.rect.centerx < -4:
                    self.rect.centerx -= 4
                else:
                    self.rect.centerx -= 1
                    
    def laser_shot(self):
        mouse = pygame.mouse.get_pressed()[0]
        delta = 380
        if mouse:
            if not self.can_shoot:
                current_time = pygame.time.get_ticks()
                if current_time - self.shoot_time > delta:
                    self.can_shoot = True
            else:
                laser = Laser(position=self.rect.midtop, groups=laser_group)
                self.shoot_time = pygame.time.get_ticks()
                self.can_shoot = False
                laser.sound.play()
                
    def meteor_collisions(self):
        if pygame.sprite.spritecollide(self, meteor_group,
                                       False, pygame.sprite.collide_mask):
            pygame.quit()
            sys.exit()
            
    def update(self):
        self.laser_shot()
        self.input_position()
        
        self.meteor_collisions()
        
        
class Laser(pygame.sprite.Sprite):
    """Creates laser object"""
    def __init__(self, position, groups):
        super().__init__(groups)
        
        self.image = pygame.image.load("images\laser2.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (15, 25))
        self.rect = self.image.get_rect(midbottom=(position))
        self.mask = pygame.mask.from_surface(self.image)
        # sound
        self.sound = pygame.mixer.Sound(r"sounds\blaster-2-81267.mp3")
        self.sound.set_volume(0.1)
        
        self.explosion_sound = pygame.mixer.Sound(r"sounds\blast-37988.mp3")
        self.explosion_sound.set_volume(0.7)
        # float base position
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(0, -1)
        self.speed = 520
        
    def meteor_colisions(self):
        if pygame.sprite.spritecollide(self, meteor_group,
                                       True, pygame.sprite.collide_mask):
            self.kill()
            self.explosion_sound.play()
        
    def update(self):
        self.pos += self.direction * self.speed *dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        self.meteor_colisions()
        if self.rect.bottom < 0:
            self.kill()
        
        
class Meteor(pygame.sprite.Sprite):
    """Creates meteor object"""
    def __init__(self, position, groups):
        super().__init__(groups)
        
        # randomizing meteot size
        w = random.randint(60, 120)
        
        self.image = pygame.image.load(r"images\asteroid.png").convert_alpha()
        self.scaled = pygame.transform.scale(self.image, (w, w))
        self.image = self.scaled
        self.rect = self.image.get_rect(midbottom=(position))
        # creating mask
        self.mask = pygame.mask.from_surface(self.image)
        # float base position
        self.pos = pygame.math.Vector2(self.rect.midbottom)
        self.direction = pygame.math.Vector2(random.randint(-1,1), 1)
        # random speed
        self.speed = random.randint(230, 400)
        
        # rotation logic
        self.rotation = 0
        self.rotation_speed = random.randint(20, 50)
        
    def rotate(self):
        self.rotation += self.rotation_speed * dt
        rotated_surf = pygame.transform.rotozoom(self.scaled, self.rotation,1)
        self.image = rotated_surf
        self.rect = self.image.get_rect(center=self.rect.center)
        
        
        
    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        self.rotate()
        if self.rect.top > WINDOW_HEIGHT + 200:
            self.kill()
        
        
class Score:
    def __init__(self):
        self.font = pygame.font.Font("images\subatomic.tsoonami.ttf", 40)
        
    def display(self):
        score_text = f"Score: {pygame.time.get_ticks()//1000}"
        text_surf = self.font.render(score_text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(midbottom = (WINDOW_WIDTH/2,
                                                    WINDOW_HEIGHT-20))
        display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(display_surface, (255,255,255), text_rect.inflate(30,30),
                         width=8, border_radius=3)


# base setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1290, 720
clock = pygame.time.Clock()
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Asteroid shooter V2")

# backgroun
background_surf = pygame.image.load(r"images\background.jpg").convert_alpha()
background_surf = pygame.transform.scale(background_surf, (WINDOW_WIDTH, WINDOW_HEIGHT))

# sprite groups
spaceship_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()

# sprite creation
ship = Ship(spaceship_group)

spawn_meteor = pygame.event.custom_type()
pygame.time.set_timer(spawn_meteor, 500)

score = Score()

background_music = pygame.mixer.Sound(r"sounds\tales-of-the-caped-crusader-theme-20391.mp3")
background_music.set_volume(0.6)
background_music.play(-1)

# game loop
while True:
    
    dt = clock.tick(120)/1000
    
    
    #inputs 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == spawn_meteor:
            position = (random.randint(-100, WINDOW_WIDTH+100),
                        random.randint(-150, -50))
            meteor = Meteor(position=position, groups=meteor_group)
            
            
    # background
    display_surface.blit(background_surf, (0,0))
    
    # graphics
    spaceship_group.draw(display_surface)
    spaceship_group.update()  
    laser_group.draw(display_surface)   
    laser_group.update()   
    meteor_group.draw(display_surface)
    meteor_group.update()
    score.display()
            
            
    pygame.display.update()