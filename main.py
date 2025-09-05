import pygame
from os.path import join
from random import randint, uniform

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOWS_WIDTH / 2, WINDOWS_HEIGHT - 100))
        self.direction = pygame.Vector2()
        self.speed = 400
    

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]) 
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        laser_key = pygame.key.get_just_pressed()
        if laser_key[pygame.K_SPACE]:
            Laser(self.rect.midtop ,(all_sprites, laser_sprites))
            
class Star(pygame.sprite.Sprite):
    def __init__(self, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0, WINDOWS_WIDTH), randint(0, WINDOWS_HEIGHT)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'laser.png')).convert_alpha()
        self.rect = self.image.get_frect(midbottom = pos)

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.top < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = 400

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if self.rect.top > WINDOWS_HEIGHT:
            self.kill()

def collision():
    global running
    global score
    crash = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask)
    if crash:
        running = 0
    for laser in laser_sprites:
        hit = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if hit:
            score += 1
            laser.kill()

def display_score(score):
    text_surf = font.render(str(score), True, 'black')
    text_rect = text_surf.get_frect(center = (WINDOWS_WIDTH / 2, WINDOWS_HEIGHT - 70))        
    screen.blit(text_surf, text_rect)
    pygame.draw.rect(screen, (240,240,230), text_rect.inflate(20, 10).move(0, -5), 5, 10)


# setup      
pygame.init()
running = True
WINDOWS_WIDTH, WINDOWS_HEIGHT = 1280, 720
screen = pygame.display.set_mode((WINDOWS_WIDTH, WINDOWS_HEIGHT))
clock = pygame.time.Clock()
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
pygame.display.set_caption("Ezedin's Game")
score = 0

font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'))

# sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

for i in range(20):
    Star(star_surf, all_sprites)
player = Player(all_sprites)

meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

while running:
    dt = clock.tick() / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == meteor_event:
            x, y = randint(0, WINDOWS_WIDTH), randint(-200, -100)
            Meteor((x,y), (all_sprites, meteor_sprites))

    collision()
    screen.fill('#9abaed')
    display_score(score)

    all_sprites.update(dt)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
