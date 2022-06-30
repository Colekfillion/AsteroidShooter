import math
import random

import pygame
from pygame.locals import FULLSCREEN

pygame.init()
screen_width, screen_height = 1535, 863
screen = pygame.display.set_mode((0, 0), FULLSCREEN)
pygame.display.set_caption("Asteroid Miner")
# bullet_sound = pygame.mixer.Sound('')
# asteroid_destroy_sound = pygame.mixer.Sound('')
# player_collision_sound = pygame.mixer.Sound('')
pygame.mixer.music.load('slow-2021-08-30_-_Boss_Time_-_www.FesliyanStudios.com.wav')
pygame.mixer.music.play(-1)
font = pygame.font.SysFont("arial", 50)


def draw(img, x, y):
    # Don't draw if offscreen
    if screen_width > x > 0 and screen_height > y > 0:
        screen.blit(img, (x, y))


class Player:
    img = pygame.image.load("player.png")
    img_thrust = pygame.image.load("player_thrust.png")
    angle = 0
    x, y = (screen_width / 2) - 16, (screen_height / 2) - 16
    x_change, y_change = 0, 0
    speed = 0.001 * 4
    score = 0

    def rotate(self, angle, img=img):
        screen.blit(pygame.transform.rotate(img, angle), ((screen_width / 2) - 16, (screen_height / 2) - 16))

    def move(self, angle, divisor):
        self.x_change -= (player.speed/divisor) * math.sin(math.radians(angle))
        self.y_change -= (player.speed/divisor) * math.cos(math.radians(angle))


class Bullet:
    img = pygame.Surface((8, 8))
    x, y = 0, 0
    x_change, y_change = 0, 0
    speed = 0.5 * 3


class Asteroid:
    img = pygame.Surface((20, 20))
    x, y = 0, 0
    x_change, y_change = 0, 0
    speed = 0.5 * 3


class Trail:
    img = pygame.Surface((6, 6))
    x, y = 0, 0
    decay_time = 500


player = Player()
bullets = []
asteroids = []
trails = []
i = 0
ii = 0

# game loop
running = True
while running:

    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                bullet = Bullet()
                bullet.x, bullet.y = screen_width / 2, screen_height / 2
                bullet.x_change = player.x_change - (bullet.speed * math.sin(math.radians(player.angle)))
                bullet.y_change = player.y_change - (bullet.speed * math.cos(math.radians(player.angle)))
                bullets.append(bullet)
                pygame.draw.circle(bullet.img, pygame.Color(255, 255, 255), (4, 4), 4)
                # bullet_sound.play()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                player.x_change, player.y_change = 0, 0

    keys = pygame.key.get_pressed()
    if not keys[pygame.K_x]:
        # Controlling player movement
        if keys[pygame.K_w]:
            player.move(player.angle, 1)
            screen.blit(pygame.transform.rotate(player.img_thrust, player.angle),
                        ((screen_width / 2) - 16, (screen_height / 2) - 16))
            if ii == 18:
                # Every 18 frames that W is held, spawn a trail particle
                trail = Trail()
                trail.x, trail.y = screen_width/2, screen_height/2
                trails.append(trail)
                pygame.draw.circle(trail.img, pygame.Color(20, 20, 255), (3, 3), 3)
                ii = 0
            else:
                ii += 1
        if keys[pygame.K_s]:
            player.move(player.angle-180, 1)
        # Moving left and right is slower than forward and backwards
        if keys[pygame.K_a]:
            player.move(player.angle+90, 2)
        if keys[pygame.K_d]:
            player.move(player.angle-90, 2)

    for bullet in bullets:
        bullet.x += bullet.x_change - player.x_change
        bullet.y += bullet.y_change - player.y_change
        draw(bullet.img, bullet.x, bullet.y)

        # Remove old bullets and ones offscreen
        if len(bullets) >= 30 or not (screen_width * 2 > bullet.x > -screen_width or
                                      screen_height * 2 > bullet.y > -screen_height):
            bullets.remove(bullet)

        # Asteroid-bullet collision checking based on distance
        for asteroid in asteroids:
            distance = (((((bullet.x + 4) - (asteroid.x + 10)) ** 2) + (
                        ((bullet.y + 4) - (asteroid.y + 10)) ** 2)) ** 0.5)
            if distance < 15:
                # asteroid_destroy_sound.play()
                bullets.remove(bullet)
                asteroids.remove(asteroid)
                player.score += 5

    for asteroid in asteroids:
        asteroid.x += asteroid.x_change - player.x_change
        asteroid.y += asteroid.y_change - player.y_change
        draw(asteroid.img, asteroid.x, asteroid.y)

        # Remove old asteroids and ones offscreen
        if len(asteroids) >= 20 or not (screen_width * 2 > asteroid.x > -screen_width or
                                        screen_height * 2 > asteroid.y > -screen_height):
            asteroids.remove(asteroid)

        # Asteroid-player collision checking by distance
        distance = ((((((screen_width/2) + 16) - (asteroid.x + 10)) ** 2) + (
                (((screen_height/2) + 16) - (asteroid.y + 10)) ** 2)) ** 0.5)
        if distance < 26:
            asteroids.remove(asteroid)
            player.score -= 20
            # player_collision_sound.play()
            if player.score < 0:
                # Game closes if score is below 0
                running = False

    for trail in trails:
        trail.x -= player.x_change
        trail.y -= player.y_change
        trail.decay_time -= 1
        # Remove old trails and ones offscreen
        if trail.decay_time == 0 or not (screen_width > trail.x > 0 or screen_height > trail.y > 0):
            trails.remove(trail)
        draw(trail.img, trail.x, trail.y)

    # Asteroids spawn more often in higher scores
    asteroidFreq = (750-player.score)
    if asteroidFreq <= 0:
        asteroidFreq == 100
    if i == asteroidFreq:
        asteroid = Asteroid()

        # Places the asteroid offscreen on a designated side
        which = random.randint(1, 4)
        if which == 1:
            asteroid.x, asteroid.y = random.randrange(screen_width), random.randrange(int(screen_height/4))*-1
        elif which == 2:
            asteroid.x, asteroid.y = random.randrange(int(screen_width/6))*-1, random.randrange(screen_height)
        elif which == 3:
            asteroid.x, asteroid.y = random.randint(screen_width, int(screen_width*1.2)), random.randrange(screen_height)
        elif which == 4:
            asteroid.x, asteroid.y = random.randrange(screen_width), random.randint(screen_height, int(screen_height*1.2))

        angle_to_player = math.degrees(math.atan2(asteroid.x - (screen_width/2), asteroid.y - (screen_height/2)))
        if angle_to_player < 0:
            # I don't know
            angle_to_player += 360
        # Asteroids move faster with higher score
        asteroid.x_change = player.x_change - (((30+player.score)/50) * math.sin(math.radians(angle_to_player+random.randint(-10, 10))))
        asteroid.y_change = player.y_change - (((30+player.score)/50) * math.cos(math.radians(angle_to_player+random.randint(-10, 10))))
        asteroids.append(asteroid)
        pygame.draw.circle(asteroid.img, pygame.Color(97, 78, 29), (10, 10), 10)
        i = 0
    else:
        i += 1

    # Update angle of player sprite based on mouse position, always points to sprite
    mouseX, mouseY = pygame.mouse.get_pos()
    player.x += player.x_change
    player.y += player.y_change
    player_angle = math.degrees(math.atan2((screen_width / 2) - mouseX, (screen_height / 2) - mouseY))
    if player_angle < 0:
        player_angle += 360
    player.angle = player_angle
    player.rotate(player.angle)
    score_surface = font.render(str(player.score), False, (255, 255, 255))
    screen.blit(score_surface, (0, 0))

    pygame.display.update()
