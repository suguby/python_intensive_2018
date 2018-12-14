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


def fire_missile(x, y):
    missile = turtle.Turtle(visible=False)
    missile.speed(0)
    missile.color('white')
    missile.penup()
    missile.setpos(x=BASE_X, y=BASE_Y)
    missile.pendown()
    heading = missile.towards(x, y)
    missile.setheading(heading)
    missile.showturtle()
    info = {'missile': missile, 'target': [x, y],
            'state': 'launched', 'radius': 0}
    our_missiles.append(info)


def fire_enemy_missile():
    missile = turtle.Turtle(visible=False)
    missile.speed(0)
    missile.color('red')
    missile.penup()
    x = random.randint(-600, 600)
    y = 400
    missile.setpos(x=x, y=y)
    missile.pendown()
    heading = missile.towards(BASE_X, BASE_Y)
    missile.setheading(heading)
    missile.showturtle()
    info = {'missile': missile, 'target': [BASE_X, BASE_Y],
            'state': 'launched', 'radius': 0}
    enemy_missiles.append(info)


window.onclick(fire_missile)

our_missiles = []
enemy_missiles = []

while True:
    window.update()

    for info in our_missiles:
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

    dead_missiles = [info for info in our_missiles if info['state'] == 'dead']
    for dead in dead_missiles:
        our_missiles.remove(dead)

    if len(enemy_missiles) < ENEMY_COUNT:
        fire_enemy_missile()

    for info in enemy_missiles:
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

    dead_missiles = [info for info in enemy_missiles if info['state'] == 'dead']
    for dead in dead_missiles:
        enemy_missiles.remove(dead)
