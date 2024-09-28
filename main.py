import pygame
import random
import math
from pygame import mixer

# initialize the pygame module
pygame.init()

# Creating the game window
game_window = pygame.display.set_mode((800, 600))

# Setting game title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship_icon.png")
pygame.display.set_icon(icon)

# background image
background_img = pygame.image.load("background.png")

# background music
mixer.music.load('Free Game Loop.wav')
mixer.music.play(-1)  # keeps on playing the music in a loop

## Setting up the sprites/moving objects

# setting up the player's spaceship
player_img = pygame.image.load("spaceship.png")  # load the player's sprite
player_x = 370  # x-coord of the player
player_y = 480  # y-coord of the player
player_x_speed = 0  # speed of player in x-coordinate
player_y_speed = 0  # speed of player in x-coordinate

# setting up lists for multiple enemies
# start with empty lists, so we can keep adding to them later
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_speed = []
enemy_y_speed = []
no_of_enemies = 6  # change this as you like

# setting up the enemy
for i in range(no_of_enemies):
    enemy_img.append(pygame.image.load("ufo.png"))  # load the enemy sprite
    enemy_x.append(random.randint(0, 736))  # spawns the enemy with a random x-coord
    enemy_y.append(random.randint(10, 150))  # spawns the enemy with a random y-coord
    enemy_x_speed.append(7)  # speed of enemy in x-axis
    enemy_y_speed.append(40)  # speed of enemy in y-axis

# setting up the bullet
bullet_img = pygame.image.load("bullet.png")  # load the bullet
bullet_x = 0  # starting x coord of bullet
bullet_y = 480  # starting y coord of bullet
bullet_x_speed = 0  # bullet never moves horizontally
bullet_y_speed = 20  # vertical speed of bullet
bullet_state = "ready"  # the bullet has 2 states - "ready" and "fire"

# keeping track of the score
score = 0
font = pygame.font.Font('freesansbold.ttf', 25)  # loading the font and setting the size of the text

# setting the location of the text
text_x = 650
text_y = 10

# game_over_text
over_font = pygame.font.Font('freesansbold.ttf', 64)  # loading the font and size of the game over text


##creating supporting functions

# function which displays the score during the game
def show_score(x, y):
    # we have to render the text and assign a color to it
    score_val = font.render("Score: " + str(score), True, (255, 255, 255))
    game_window.blit(score_val, (x, y))  # draws the score on our game window


# function which prints a game over message when the game is over
def game_over():
    # rendering the text and assigning a color to it
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    game_window.blit(over_text, (200, 250))  # drawing the message on the screen


# function which draws the player's sprite on the sreen
def player(x, y):
    game_window.blit(player_img, (x, y))  # draws the player on our game window


# function which draws our enemies on the screen
def enemy(x, y, i):
    # takes in the number of enemies and draws each one
    game_window.blit(enemy_img[i], (x, y))


# function to change our bullet state
def fire(x, y):
    # we have to call global in order to locally change the global variable bullet_state
    global bullet_state
    bullet_state = "fire"
    game_window.blit(bullet_img, (x + 16, y + 10))  # draws our bullet on the screen when we fire our bullet


# calculates the distance and returns true if the distance between sprites is less than a certin permissible distance
def has_collided(x1, y1, x2, y2):
    # takes in the coordinates of two poins and calcutates the distace
    distance = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))  # distance formula
    return distance < 27


# Main game loop to keep the game running
playing = True  # game variable
while playing:

    # color of the screen(red,green,blue)
    game_window.fill((255, 255, 255))  # white screen

    # draw our background image
    game_window.blit(background_img, (0, 0))  # 0,0 is the origin which is at the top left of the screen

    # assigning keys from the keyboard to different actions
    for event in pygame.event.get():  # loops through all the events in our game
        if event.type == pygame.QUIT:  # closes the game window when the cross button is pressed
            playing = False  # when cross is presses break out of the loop

        # assigning movement keys
        if event.type == pygame.KEYDOWN:  # activated when any key on the keyboard is pressed

            if event.key == pygame.K_LEFT or event.key == ord('a'):  # left arrow and 'A' key
                player_x_speed = -8  # set player speed in left direction

            if event.key == pygame.K_RIGHT or event.key == ord('d'):  # right arrow and 'D' key
                player_x_speed = 8  # set player speed in right direction

            if event.key == pygame.K_UP or event.key == ord('w'):  # up arrow and 'W' key
                player_y_speed = -8  # set player speed in upward direction

            if event.key == pygame.K_DOWN or event.key == ord('s'):  # down arrow and 'S' key
                player_y_speed = 8  # set player speed in downward direction

            # firing the bullet
            if event.key == pygame.K_SPACE:  # spacebar

                if bullet_state == "ready":  # fires only when our bullet has been fired and is not on the screen
                    bullet_sound = mixer.Sound('laser.wav')  # load the bullet sound
                    bullet_sound.play()  # play the bullet sound

                    # code which enables the bullet to be fired from the player no matter where the player is located
                    bullet_x = player_x  # assigns the current x value of the player to the bullet
                    bullet_y = player_y  # assigns the current y value of the player to the bullet

                    # calling the bullet function
                    fire(bullet_x, bullet_y)

        # letting go of our keys
        if event.type == pygame.KEYUP:  # responds when our keyboard key is released

            # this is what will happen when any of the keys are released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or \
                    event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == ord('a') \
                    or event.key == ord('d') or event.key == ord('w') or event.key == ord('s'):
                # when the key is released the players speed is set to zero so that the player stops moving
                player_x_speed = 0
                player_y_speed = 0

    # updating the player's speed
    player_x += player_x_speed
    player_y += player_y_speed

    # setting boundaries so that our player does no exit the screen area
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:  # 736b because our player's image is 64 pixels in length
        player_x = 736

    player_y += player_y_speed
    if player_y <= 0:
        player_y = 0
    elif player_y >= 480:
        player_y = 480

    # setting up the enemy movement
    for i in range(no_of_enemies):

        # setting the game over scenario when there is a collision between the enemy and the player
        collision1 = has_collided(enemy_x[i], enemy_y[i], player_x, player_y)  # loops through all the enemies

        if enemy_y[i] > 480 or collision1:  # if the enemies manage to come down to a y coord of 480 or they collide with the player, then the game is over
            for j in range(no_of_enemies):
                enemy_y[j] = 2000  # makes the enemies disappear when the game is over
            game_over()  # prints game over
            break

        # setting up the enemy movement
        enemy_x[i] += enemy_x_speed[i]

        if enemy_x[i] <= 0:
            enemy_x_speed[i] = 7  # starts moving towards the right

            enemy_y[i] += enemy_y_speed[i]  # the enemies move down when they hit the boundary

        elif enemy_x[i] >= 736:
            enemy_x_speed[i] = -7  # starts moving towards the right
            enemy_y[i] += enemy_y_speed[i]  # the enemies move down when they hit the boundary

        # bullet-enemy collision
        # detect bullet enemy collision and updates the score
        collision2 = has_collided(enemy_x[i], enemy_y[i], bullet_x, bullet_y)

        if collision2:
            collision_sound = mixer.Sound('long explosion.wav')  # load the sound of collision
            collision_sound.play()  # play the sound when there is a collision

            # reset the bullet
            bullet_y = 480
            bullet_state = "ready"
            score += 1  # update score when there is a hit

            # when the bullet hits the enemy spawn them at a random location
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(0, 150)

        enemy(enemy_x[i], enemy_y[i], i)  # spawns all the enemies

    # bullet fire
    if bullet_y <= 0:
        # reset bullet when it reaches the top of the screen
        bullet_y = 480
        bullet_state = "ready"

    # fire the bullet
    if bullet_state == "fire":
        fire(bullet_x, bullet_y)  # put the bullet on the game_window
        bullet_y -= bullet_y_speed  # send the bullet updwards

    # display the player
    player(player_x, player_y)

    # print the score
    show_score(text_x, text_y)

    # update the game window
    pygame.display.update()

#programmed by Rik Ganguli Biswas
