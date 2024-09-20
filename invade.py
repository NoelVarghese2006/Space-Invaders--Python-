# Reset aliens after all 30 are gone



import turtle
import winsound
import time
import random
import platform
import os


# Set up Screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders")
wn.bgpic("invade_bg.gif")
wn.tracer(0)

# Register Shape
wn.register_shape("invade_enemy.gif")
wn.register_shape("invade_player.gif")
# Draw Border
border_pen = turtle.Turtle()
border_pen.hideturtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)

# Score to 0
score = 0

# Count enemies
count = 0
diff = 0

# Draw score
score_pen = turtle.Turtle()
score_pen.hideturtle()
score_pen.penup()
score_pen.speed(0)
score_pen.color("white")
score_pen.setposition(-250, 275)
score_pen.write("Score: {}".format(score), align="center", font=("Courier", 14, "normal"))

# Create Player
player = turtle.Turtle()
player.color("blue")
player.shape("invade_player.gif")
player.penup()
player.speed(0)
player.setheading(90)
player.goto(0, -250)

player.speed = 0

enemy_speed = 0.2

# Chose # of enemies
num_of_enemies = 30
# Empty list
enemies = []

# Add enemies to list
for i in range(num_of_enemies):
    enemies.append(turtle.Turtle())
    count += 1

enemy_start_x = -225
enemy_start_y = 250
enemy_number = 0

for enemy in enemies:
    # Enemies
    enemy.color("red")
    enemy.shape("invade_enemy.gif")
    enemy.penup()
    enemy.speed(0)
    # x = random.randrange(-280, 280, 40)
    # y = random.randrange(100, 280, 40)
    x = enemy_start_x + (50 * enemy_number)
    y = enemy_start_y
    enemy.setpos(x, y)
    # Update enemy number
    enemy_number += 1
    if enemy_number == 10:
        enemy_start_y -= 40
        enemy_number = 0

# Weapon
bullet = turtle.Turtle()
bullet.setx(500)
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(stretch_wid=0.5, stretch_len=0.5)
bullet.hideturtle()

bullet_speed = 2

# Bullet state
# ready = ready to fire
# fire = firing
bullet_state = "ready"


# Moving the player
def move_left():
    player.speed = -1


def move_right():
    player.speed = 1


def move_player():
    x = player.xcor()
    x += player.speed
    if x < -280:
        x = -280
    if x > 280:
        x = 280
    player.setx(x)


def fire_bullet():
    global bullet_state
    # Move bullet to player
    if bullet_state == "ready":
        bullet_state = "fire"
        x = player.xcor()
        y = player.ycor()
        bullet.setpos(x, y+10)
        bullet.showturtle()
        play_sound("invade_laser.wav")


def play_sound(sound_file, time = 0):
    # Windows
    if platform.system() == "Windows":
        winsound.PlaySound(sound_file, winsound.SND_ASYNC)
    elif platform.system() == "Linux":
        os.system("aplay -q {}&".format(sound_file))
    else:
        os.system("afplay {}&".format(sound_file))

    if time > 0:
        turtle.ontimer(lambda: play_sound(sound_file, time), t=int(time * 1000))


wn.listen()
wn.onkeypress(move_left, "a")
wn.onkeypress(move_right, "d")
wn.onkeypress(fire_bullet, "w")

# Background music
# play_sound("invade_music.wav", 119)
# turtle.ontimer(lambda: play_sound("invade_music.wav", 119), t=int(119 * 1000))
winsound.PlaySound("invade_music.wav", winsound.SND_ASYNC)
# Main game loop
while True:
    wn.update()
    move_player()
    for enemy in enemies:
        # Moving the enemy

        x = enemy.xcor()
        x += enemy_speed
        enemy.setx(x)

        # Reverse and move all down
        if enemy.xcor() > 280 and enemy.ycor() < 500:
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            enemy_speed *= -1
        if enemy.xcor() < -280 and enemy.ycor() < 500:
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            enemy_speed *= -1
        # Turtle collision (bullet and enemy)
        if bullet.distance(enemy) < 20:
            # Reset bullet
            bullet.hideturtle()
            play_sound("invade_explode.wav")
            bullet_state = "ready"
            bullet.setposition(500, 280)
            # x = random.randrange(-280, 280, 40)
            # y = random.randrange(100, 280, 40)
            x = 0
            y = 10000
            enemy.setpos(x, y)
            enemies.remove(enemy)
            # Update Score
            score += 1
            count -= 1
            score_pen.clear()
            score_pen.write("Score: {}".format(score), align="center", font=("Courier", 14, "normal"))

        if count == 0:
            num_of_enemies += 1
            for i in range(num_of_enemies):
                enemies.append(turtle.Turtle())
                count += 1

            enemy_start_x = -225
            enemy_start_y = 250
            enemy_number = 0

            for enemy in enemies:
                # Enemies
                enemy.color("red")
                enemy.shape("invade_enemy.gif")
                enemy.penup()
                enemy.speed(0)
                # x = random.randrange(-280, 280, 40)
                # y = random.randrange(100, 280, 40)
                x = enemy_start_x + (50 * enemy_number)
                y = enemy_start_y
                enemy.setpos(x, y)
                # Update enemy number
                enemy_number += 1
                if enemy_number == 10:
                    enemy_start_y -= 40
                    enemy_number = 0

        if enemy.distance(player) < 30 or enemy.ycor() < -290:
            player.hideturtle()
            enemy.hideturtle()
            for i in range(3):
                play_sound("invade_explode.wav")
                time.sleep(1)
            quit(0)

    # Move Bullet
    if bullet.ycor() < 290:
        y = bullet.ycor()
        y += bullet_speed
        bullet.sety(y)

    # Bullet border check
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bullet_state = "ready"
