import pygame
import random

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()

def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def draw_shield_bar(surface, x, y, percentage):
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (percentage / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN , fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("../assets/player.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT - 10
        self.speed_x = 0
        self.shielf = 100

    def update(self):
        self.speed_x = 0
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_LEFT]:
            self.speed_x = -5
        if key_state[pygame.K_RIGHT]:
            self.speed_x = 5

        self.rect.x += self.speed_x

        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        laser_sound.play()

class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(meteors_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WINDOW_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-140, -100)
        self.speed_y = random.randrange(1, 10)
        self.speed_x = random.randrange(-5, 5)

    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        if self.rect.top > WINDOW_HEIGHT + 10 or self.rect.left < -100 or self.rect.right > WINDOW_WIDTH + 100:
            self.rect.x = random.randrange(WINDOW_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(1, 10)

class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("../assets/laser1.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

meteors_images= []
meteor_list = ["../assets/meteorGrey_med1.png", "../assets/meteorGrey_med2.png",
               "../assets/meteorGrey_small1.png", "../assets/meteorGrey_small2.png",
               "../assets/meteorGrey_tiny1.png", "../assets/meteorGrey_tiny2.png",
               "../assets/meteorGrey_big1.png", "../assets/meteorGrey_big2.png",
               "../assets/meteorGrey_big3.png", "../assets/meteorGrey_big4.png"]

for image in meteor_list:
    meteors_images.append(pygame.image.load(image).convert())

background = pygame.image.load("../assets/background.png").convert()

laser_sound = pygame.mixer.Sound("../assets/laser5.ogg")
explosion_sound = pygame.mixer.Sound("../assets/explosion.wav")
pygame.mixer.music.load("../assets/music.ogg")
pygame.mixer.music.set_volume(0.2)


all_sprites = pygame.sprite.Group()
meteors_list = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(8):
    meteor = Meteor()
    all_sprites.add(meteor)
    meteors_list.add(meteor)

running = True
score = 0
pygame.mixer.music.play(loops=-1)

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    all_sprites.update()

    hits = pygame.sprite.groupcollide(meteors_list, bullets, True, True)
    for hit in hits:
        score += 10
        meteor = Meteor()
        all_sprites.add(meteor)
        meteors_list.add(meteor)
        explosion_sound.play()

    hits = pygame.sprite.spritecollide(player, meteors_list, True)

    if hits:
        player.shielf -= 20
        meteor = Meteor()
        all_sprites.add(meteor)
        meteors_list.add(meteor)
        if player.shielf <= 0:
            running = False

    screen.blit(background,[0,0])

    all_sprites.draw(screen)

    draw_text(screen, str(score), 18, WINDOW_WIDTH // 2, 10)

    draw_shield_bar(screen, 5, 5, player.shielf)

    pygame.display.flip()

pygame.quit()