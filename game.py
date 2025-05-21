import pgzrun
import random
import sys
from helpers import *

WIDTH=800
HEIGHT=600

# creates a player sprite
player = Actor('tank_blue.png')
player.position = (3,8)     # ONLY edit the x,y cordinate, NOT the player.x and player.y
player.x = player.position[0]*50 + 25
player.y = player.position[1]*50 + 25
player.angle = 90
player.scale = 1

background = Actor('grass.png')
background.scale = 1

wall_map = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1]
    ]

# setup walls
walls=[]
for x in range(len(wall_map)):
    for y in range(len(wall_map[0])):
        if wall_map[x][y] == 1:
            wall = Actor('wall.png')
            wall.x = y * 50 + 25
            wall.y = x * 50 + 25
            walls.append(wall)


# setup player bullets
bullets = []
bullet_holdoff = 0
bullet_speed = 20

# setup enemy bullets
enemy_bullets = []

# setup enemy
enemy = Actor('tank_red.png')
enemy.position = (14,5)
enemy.x = enemy.position[0]*50 + 25
enemy.y = enemy.position[1]*50 + 25
enemy.angle = 270
enemy.move_count = 0

game_running = True

def draw():
    # CONTROLS WHAT IS DRAWN EACH FRAME OF THE GAME

    screen.clear()

    if game_running == True:
        background.draw()
        player.draw()

        enemy.draw()

        for wall in walls:
            wall.draw()

        for bullet in bullets:
            bullet.draw()

        for bullet in enemy_bullets:
            bullet.draw()
    else:
        screen.fill((149, 161, 171))
        screen.draw.text(f"GAME OVER", centerx=(WIDTH / 2) + 100, centery=HEIGHT / 2)

def player_movement():
    # CONTROLS HOW THE PLAYER MOVES

    original_x = player.x
    original_y = player.y

    # Move the player if keys are pressed
    if keyboard.a and player.left >0:
        player.x = player.x - 2
        player.angle = 180
    elif keyboard.d and player.right < WIDTH:
        player.x = player.x + 2
        player.angle = 0
    elif keyboard.w  and player.top > 0:
        player.y = player.y - 2
        player.angle = 90
    elif keyboard.s and player.bottom < HEIGHT:
        player.y = player.y + 2
        player.angle = 270



    ## prevent player from colliding into walls
    if player.collidelist(walls) != -1:
        player.x = original_x
        player.y = original_y

def player_bullets_movement():
    # CONTROLS HOW THE PLAYER BULLETS MOVES

    global bullet_holdoff  

    if bullet_holdoff == 0:
        if keyboard.space:
            bullet = Actor('blue_laser.png')
            bullet.angle = player.angle
            bullet.x = player.x
            bullet.y = player.y
            bullets.append(bullet)
            bullet_holdoff = bullet_speed
    else:
        bullet_holdoff = bullet_holdoff - 1

    # controls moving the bullets
    for bullet in bullets:
        if bullet.angle == 0:
            bullet.x = bullet.x + 5
        elif bullet.angle == 90:
            bullet.y = bullet.y - 5
        elif bullet.angle == 180:
            bullet.x = bullet.x - 5
        elif bullet.angle == 270:
            bullet.y = bullet.y + 5

def player_bullets_collision():
    # CONTROLS WHEN THE PLAYER BULLET COLLIDES WITH A WALL OR ENEMY

    bullets_to_remove = []

    for bullet in bullets:
        # removes wall if it is hit by bullet
        wall_index = bullet.collidelist(walls)
        if wall_index != -1:
            del walls[wall_index]
            bullets_to_remove.append(bullet)

        # removes bullet if it is off the screen
        if bullet.x < 0 or bullet.x > 800 or bullet.y < 0 or bullet.y > 600:
            bullets_to_remove.append(bullet)


        # if a bullet hits the enemy, it respawns
        if bullet.colliderect(enemy):
            enemy.x = random.randint(1,3) * 50 + 25  #only edit the numbers in the brackets 
            enemy.y = random.randint(1,3)  * 50 + 25

            while enemy.collidelist(walls) != -1:
                enemy.x = random.randint(1,3) * 50 + 25  #only edit the numbers in the brackets 
                enemy.y = random.randint(1,3)  * 50 + 25
              
            bullets_to_remove.append(bullet)

    # Remove bullets after iteration
    for bullet in bullets_to_remove:
        bullets.remove(bullet)


def control_enemy():
    # CONTROLS ENEMY MOVEMENT 

    global game_running

    # Movement 
    choice = random.randint(0, 2)
    if enemy.move_count > 0:
        enemy.move_count = enemy.move_count - 1

        original_x = enemy.x
        original_y = enemy.y
        if enemy.angle == 0:
            enemy.x = enemy.x + 2
        elif enemy.angle == 90:
            enemy.y = enemy.y - 2
        elif enemy.angle == 180:
            enemy.x = enemy.x - 2
        elif enemy.angle == 270:
            enemy.y = enemy.y + 2

        if enemy.collidelist(walls) != -1:
            enemy.x = original_x
            enemy.y = original_y
            enemy.move_count = 0

        if enemy.x < 0 or enemy.x > 800 or enemy.y < 0 or enemy.y > 600:
            enemy.x = original_x
            enemy.y = original_y
            enemy.move_count = 0

    elif choice == 0:
        enemy.move_count = 20

    elif choice == 1:
        enemy.angle = random.randint(0, 3) * 90         # rotation

    else:   # if enemy shoots a bullet
        bullet = Actor('blue_laser.png')
        bullet.angle = enemy.angle
        bullet.x = enemy.x
        bullet.y = enemy.y
        enemy_bullets.append(bullet)

    for bullet in enemy_bullets:
        if bullet.angle == 0:
            bullet.x = bullet.x + 5
        elif bullet.angle == 90:
            bullet.y = bullet.y - 5
        elif bullet.angle == 180:
            bullet.x = bullet.x - 5
        elif bullet.angle == 270:
            bullet.y = bullet.y + 5

    # how the bullet moves
    for bullet in enemy_bullets:
        wall_index = bullet.collidelist(walls)

        if bullet.x < 0 or bullet.x > 800 or bullet.y < 0 or bullet.y > 600 or wall_index != -1:
            enemy_bullets.remove(bullet)

        # if bullet his player
        if bullet.colliderect(player):
            game_running = True

def update():
    # CONTROLS WHAT HAPPENS EACH FRAME OF THE GAME

    global bullet_holdoff

    player_movement()

    if game_running == True:    
        player_bullets_movement()
        player_bullets_collision()

        control_enemy()


# runs the game
pgzrun.go()
