import math
import os
import random
import turtle

BASE_PATH = os.path.dirname(os.path.dirname(__file__))

window = turtle.Screen()
window.setup(1200 + 3, 800 + 3)
window.bgpic(os.path.join(BASE_PATH, "images", "background.png"))
window.screensize(1200, 800)
window.tracer(n=2)

ENEMY_COUNT = 5

BASE_X, BASE_Y = 0, -300


def create_missile(color, x, y, x2, y2):
    missile = turtle.Turtle(visible=False)
    missile.speed(0)
    missile.color(color)
    missile.penup()
    missile.setpos(x=x, y=y)
    missile.pendown()
    heading = missile.towards(x2, y2)
    missile.setheading(heading)
    missile.showturtle()
    info = {'missile': missile, 'target': [x2, y2],
            'state': 'launched', 'radius': 0}
    return info


def fire_missile(x, y):
    info = create_missile(color='white', x=BASE_X, y=BASE_Y, x2=x, y2=y)
    our_missiles.append(info)


def fire_enemy_missile():
    x = random.randint(-600, 600)
    y = 400
    info = create_missile(color='red', x=x, y=y, x2=BASE_X, y2=BASE_Y)
    enemy_missiles.append(info)


def move_missiles(missiles):
    for info in missiles:
        state = info['state']
        missile = info['missile']
        if state == 'launched':
            missile.forward(4)
            target = info['target']
            if missile.distance(x=target[0], y=target[1]) < 20:
                info['state'] = 'explode'
                missile.shape('circle')
        elif state == 'explode':
            info['radius'] += 1
            if info['radius'] > 5:
                missile.clear()
                missile.hideturtle()
                info['state'] = 'dead'
            else:
                missile.shapesize(info['radius'])

    dead_missiles = [info for info in missiles if info['state'] == 'dead']
    for dead in dead_missiles:
        missiles.remove(dead)


window.onclick(fire_missile)

our_missiles = []
enemy_missiles = []

while True:
    window.update()

    if len(enemy_missiles) < ENEMY_COUNT:
        fire_enemy_missile()

    move_missiles(missiles=our_missiles)
    move_missiles(missiles=enemy_missiles)
