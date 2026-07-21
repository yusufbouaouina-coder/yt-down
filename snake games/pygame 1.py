

import pygame
from joystick import read_joystick
import pyttsx3

engine = pyttsx3.init()
engine.say("welcome to an unoficial copy built from the ground up of xenoblade chronicles, this game includes the JCP or joystick conection protocall would you like to enable it?")
engine.runAndWait()
joystickread= str(input("for yes type y, for no type n:"))
if joystickread == "y":
    joystickread = True
else:
    joystickread = False




pygame.init()
pygame.display.set_caption("our xelnoblade chronicles at home")

scrn = (800, 600)
surface = pygame.display.set_mode(scrn)

global enemy_img
global enemy_hp
global attack_time

velocity_y = 0
hp = 100
hurt_until = 0
attack_time = 100
sprdir = "left"
enemy_hp = 100

clock = pygame.time.Clock()

# Load enemy image
enemy_img = pygame.image.load("enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (64, 64))


def img_load(hurtbool):
    global char_img
    global player_mask

    if hurtbool:
        char_img = pygame.image.load("char_hurt.png")
    else:
        char_img = pygame.image.load("char.png")

    char_img = pygame.transform.scale(char_img, (64, 64))

    if sprdir == "right":
        char_img = pygame.transform.flip(char_img, True, False)

    player_mask = pygame.mask.from_surface(char_img)


img_load(False)

player_rect = pygame.Rect(50, 50, 64, 64)
wall_rect = pygame.Rect(700, 500, 50, 100)
enemy_rect = pygame.Rect(600, 300, 64, 64)

enemy_mask = pygame.mask.from_surface(enemy_img)

gravity = 0.3

running = True
while running:
    if joystickread:
        x, y,   button = read_joystick()
        print(x, y, button)
    else:
        break


    player_hitrange = pygame.Rect(player_rect.x, player_rect.y, 80, 80)
    current_time = pygame.time.get_ticks()

    # ---------------- EVENTS ----------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ---------------- INPUT ----------------
    keys = pygame.key.get_pressed()

    # (Joystick reserved for later)
    # x, y, button = read_joystick()

    if keys[pygame.K_LEFT]:
        player_rect.x -= 8
        sprdir = "left"

    if keys[pygame.K_RIGHT]:
        player_rect.x += 8
        sprdir = "right"

    if keys[pygame.K_UP]:
        player_rect.y -= 8

    if keys[pygame.K_SPACE]:
        player_rect.y -= 8

    player_rect.clamp_ip(surface.get_rect())
    enemy_rect.clamp_ip(surface.get_rect())

    # Wall bounce
    if player_rect.colliderect(wall_rect):
        velocity_y = -9

    # Enemy follows player
    if player_rect.x < enemy_rect.x:
        enemy_rect.x -= 4
    elif player_rect.x > enemy_rect.x:
        enemy_rect.x += 4

    if player_rect.y < enemy_rect.y:
        enemy_rect.y -= 4
    elif player_rect.y > enemy_rect.y:
        enemy_rect.y += 4

    # ---------------- COLLISION DAMAGE ----------------
    offset = (
        enemy_rect.x - player_rect.x,
        enemy_rect.y - player_rect.y
    )

    if player_mask.overlap(enemy_mask, offset) and current_time >= hurt_until:
        hp -= 10
        print("HP:", hp)
        hurt_until = current_time + 1500

    # Gravity
    velocity_y += gravity
    player_rect.y += velocity_y

    # Stop at floor
    if player_rect.bottom >= scrn[1]:
        player_rect.bottom = scrn[1]
        velocity_y = 0

    # Sprite update
    if current_time < hurt_until:
        img_load(True)
    else:
        img_load(False)

    # Death
    if hp <= 0:
        running = False
        print("You've died")

    # ---------------- DRAW ----------------
    surface.fill((100, 216, 230))

    pygame.draw.rect(surface, (255, 0, 0), wall_rect)

    surface.blit(enemy_img, enemy_rect)
    surface.blit(char_img, player_rect)

    pygame.display.flip()
    clock.tick(100)

pygame.quit()