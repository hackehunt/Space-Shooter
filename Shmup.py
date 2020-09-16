# Shmup game
# Code written by Prince/hackehunt
# Art by kenney.nl
# Hardmoon / Arjen Schumacher
# MUSIC BY OBLIDIVM http://oblidivmmusic.blogspot.com.es/

# Importing modules
import pygame
import random
from os import path

Width = 480
Height = 600
fps = 60
Powertime = 5000

# Configuring colors
White = (255, 255, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)

# Highscore
with open("highscore.txt", "r") as f:
    highscore = f.read()


font_name = pygame.font.match_font('Alien Encounters')
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, White)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

font_name2 = pygame.font.match_font('Consolas')
def draw_text2(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, White)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# Initializing pygame window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()

img_dir = path.join(path.dirname(__file__), "img")
sound_dir = path.join(path.dirname(__file__), "sound")


def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shieldbar(surface, x, y, value):
    if value < 0:
        value = 0

    Bar_Length = 100
    Bar_Height = 10
    fill = (value / 100) * Bar_Length
    outline_rect = pygame.Rect(x, y, Bar_Length, Bar_Height)
    fill_rect = pygame.Rect(x, y, fill, Bar_Height)
    pygame.draw.rect(surface, Red, fill_rect)
    pygame.draw.rect(surface, White, outline_rect, 2)

def draw_lives(surface, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 40 * i
        img_rect.y = y
        surface.blit(img, img_rect)

class Player(pygame.sprite.Sprite):  
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 50))
        self.image.set_colorkey(Black)
        self.rect = self.image.get_rect()
        self.radius = 25
        # pygame.draw.circle(self.image, Red, self.rect.center, self.radius)
        self.rect.centerx = Width / 2
        self.rect.bottom = Height - 25
        self.speedx = 0
        self.speedy = 0
        self.shield = 100
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.pick_time = pygame.time.get_ticks()
        self.pick = 1

    def update(self):
        # Shoot power time
        if self.pick >= 2 and pygame.time.get_ticks() - self.pick_time > Powertime:
            self.pick -= 1
            self.pick_time = pygame.time.get_ticks()
        # Unhide the player if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = Width / 2
            self.rect.bottom = Height - 25
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedx = -5


        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedx = 5

        if self.rect.right > Width:
            self.rect.right = Width

        if self.rect.left < 0:
            self.rect.left = 0


        self.rect.x += self.speedx
        self.rect.y += self.speedy
    
    def pickup(self):
        self.pick += 1
        self.pick_time = pygame.time.get_ticks()

    def shoot(self):
        if self.pick == 1:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()
        if self.pick == 2:
            bullet1 = Bullet(self.rect.left, self.rect.centery)
            bullet2 = Bullet(self.rect.right, self.rect.centery)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            bullets.add(bullet1)
            bullets.add(bullet2)
            shoot_sound.play()
        if self.pick >= 3:
            bullet1 = Bullet(self.rect.centerx, self.rect.top)
            bullet2 = Bullet(self.rect.left, self.rect.centery)
            bullet3 = Bullet(self.rect.right, self.rect.centery)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            all_sprites.add(bullet3)
            bullets.add(bullet1)
            bullets.add(bullet2)
            bullets.add(bullet3)
            shoot_sound.play()


    def hide(self):
        # Hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (Width / 2, Height + 500)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(Black)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.6 / 2)
        # pygame.draw.circle(self.image, Red, self.rect.center, self.radius)
        self.rect.x = random.randrange(Width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(3, 10)
        self.speedx = random.randrange(-2, 4)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > Height + 10 or self.rect.left < -30 or self.rect.right > Width + 30:
            self.rect.x = random.randrange(Width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 9)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = lazer_img
        self.image.set_colorkey(Black)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # Kill the bullet if it goes up the screen
        if self.rect.bottom < 0:
            self.kill()


class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['gun', 'shield', 'life'])
        self.image = powerups_img[self.type]
        self.image.set_colorkey(Black)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        # Kill the bullet if it goes up the screen
        if self.rect.bottom < 0:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1

            if self.frame == len(explosion_anim[self.size]):
                self.kill()

            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


def game_over_screen():
    pygame.mixer.music.load(path.join(sound_dir, 'over.ogg'))
    pygame.mixer.music.play()
    draw_text(screen, "Game_Over", 50,  Width / 2, Height / 5)
    draw_text(screen, "Press_Enter_To_Continue", 30,  Width / 2, Height / 3)
    draw_text(screen, f"Score: {Score}", 30,  Width / 2, Height / 2.5)
    draw_text(screen, f"Highscore: {highscore}", 30,  Width / 2, Height / 2)
    pygame.display.flip()
    WAIT = True
    while WAIT:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    WAIT = False


def intro():
    global Intro
    while Intro:
        draw_text(screen, "Welcome to Shmup!", 40, Width / 2, 20)
        draw_text2(screen, "Press 'arrow key' or 'A' and 'D' for movement", 19, Width / 2, Height / 5.5)
        draw_text2(screen, "Press 'P' for pause and enter to resume", 21, Width / 2, Height / 4)
        draw_text2(screen, "Press 'Space' to shoot", 21, Width / 2, Height / 3)
        draw_text2(screen, f"Highscore: {highscore}", 20, Width / 2, Height / 2.5)
        draw_text2(screen, "Press 'Enter' to continue", 18, Width / 2, Height / 2)
        pygame.display.flip()
        WAIT = True
        while WAIT:
            clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        WAIT = False
                        Intro = False



# All game graphics
background = pygame.image.load(path.join(img_dir, "bg.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "fighter2.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (30, 30))
player_mini_img.set_colorkey(Black)
enemy_img = pygame.image.load(path.join(img_dir, "asteroid.png"))
lazer_img = pygame.image.load(path.join(img_dir, "lazer.png"))
meteor_images = []
meteor_list = ["1asteroid.png","1asteroid.png","1asteroid.png","1asteroid.png","asteroid.png","asteroid.png","asteroid.png", "asteroid.png", "asteroid_60.png"]

for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)))

explosion_anim = {}
explosion_anim['sonic'] = []
explosion_anim['large'] = []
explosion_anim['small'] = []

for i in range(9):
    filename = 'boom0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(Black)
    img_sonic = pygame.transform.scale(img, (300, 300))
    explosion_anim['sonic'].append(img_sonic)
    img_large = pygame.transform.scale(img, (70, 70))
    explosion_anim['large'].append(img_large)
    img_small = pygame.transform.scale(img, (30, 30))
    explosion_anim['small'].append(img_small)

powerups_img = {}
powerups_img['life'] = pygame.image.load(path.join(img_dir, 'life.png')).convert()
powerups_img['gun'] = pygame.image.load(path.join(img_dir, 'bolt.png'))
powerups_img['shield'] = pygame.image.load(path.join(img_dir, 'shield.png'))

# Load all sounds
shoot_sound = pygame.mixer.Sound(path.join(sound_dir, 'Laser_Shoot.wav'))
gunpower_sound = pygame.mixer.Sound(path.join(sound_dir, 'power1.ogg'))
lifepower_sound = pygame.mixer.Sound(path.join(sound_dir, 'power2.ogg'))
score_sound = pygame.mixer.Sound(path.join(sound_dir, 'power3.ogg'))
over = pygame.mixer.Sound(path.join(sound_dir, 'over.ogg'))
pygame.mixer.music.load(path.join(sound_dir, 'Battle in the Stars.ogg'))
pygame.mixer.music.set_volume(0.5)
explosions = []
for sound in ['Explosion15.wav', 'Explosion16.wav']:
    explosions.append(pygame.mixer.Sound(path.join(sound_dir, sound)))
death_sound = pygame.mixer.Sound(path.join(sound_dir, 'rumble1.ogg'))
# Load all sprites
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
powerups = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

for i in range(1, 14):
    newmob()

Score = 0
pygame.mixer.music.play(loops=-1)


# Game loop
Intro = True
game_over = False
Running = True
pause = False

while Running:
    while Intro:
        intro()
        Intro = False
    if game_over:
        if Score > int(highscore):
            highscore = Score
        with open("highscore.txt", "w") as f:
            f.write(str(highscore))
        game_over_screen()
        game_over = False
        # Load all sprites
        pygame.mixer.music.load(path.join(sound_dir, 'Battle in the Stars.ogg'))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)

        for i in range(1, 14):
            newmob()

        Score = 0
        pygame.mixer.music.play(loops=-1)
    # Game Speed
    clock.tick(fps)
    # Pause code
    if pause == True:
        while True:
            pygame.mixer.music.pause()
            event = pygame.event.poll()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pause = False
                    pygame.mixer.music.unpause()
                    break
                elif event.key == pygame.K_ESCAPE or event.key == pygame.QUIT:
                    running = False
                    pygame.quit()

            else:
                draw_text2(screen, "Game Paused...", 25, Width/2, Height/2)
                draw_text(
                    screen, "Press [ENTER] to resume game", 25, Width/2, (Height/2)+40)
                draw_text2(screen, "or [ESC] to exit game",
                          25, Width/2, (Height/2)+80)
                pygame.display.update()

    # Input process(events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

            if event.key == pygame.K_RETURN:
                pause = True
    
    # Update
    all_sprites.update()
    # Check for collision between enemy and bullets
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        Score += 50 - hit.radius
        random.choice(explosions).play()
        explosion = Explosion(hit.rect.center, 'large')
        all_sprites.add(explosion)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()
    # Check for collision between player and enemy
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        explosion = Explosion(hit.rect.center, 'small')
        all_sprites.add(explosion)
        newmob()
        if player.shield <= 0:
            death_sound.play()
            death_explosion = Explosion(player.rect.center, 'sonic')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100
    # If player hit a powerup
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'life':
            lifepower_sound.play()
            player.shield += 15
            if player.shield >= 100:
                player.shield = 100
        
        if hit.type == 'gun':
            gunpower_sound.play()
            player.pickup()

        if hit.type == 'shield':
            score_sound.play()
            Score += 500
    # if the player shield is over and the burst explosion is also over then we will quit the game
    if player.lives < 1 and not death_explosion.alive():
        game_over = True

    # New
    if Score > 1000:
        mobs.speedx = random.randrange(3, 10)
        mobs.speedx = random.randrange(3, 10)

    # Draw/render
    screen.fill(Black)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(Score), 25, Width / 2, 10 )
    draw_shieldbar(screen, 5, 5, player.shield)
    draw_lives(screen, Width - 130, 10, player.lives, player_mini_img)
    # *after* drawing everything flip the display
    pygame.display.flip()
    
pygame.quit()
