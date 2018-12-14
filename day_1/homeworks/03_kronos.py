# -*- coding: utf-8 -*-

import math
import random
import turtle

window = turtle.Screen()
window.setup(1200 + 3, 800 + 3)
window.bgpic("images/background.png")
window.screensize(1200, 800)
# window.tracer(n=2)

BASE_X, BASE_Y = 0, -300
SKY_X_MIN = -500
SKY_X_MAX = 500
SKY_Y = 500

def calc_heading(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    length = (dx ** 2 + dy ** 2) ** 0.5
    cos_alpha = dx / length
    alpha = math.acos(cos_alpha)
    alpha = math.degrees(alpha)
    if dy < 0:
        alpha = -alpha
    return alpha


def fire_missile(x, y):
    missile = turtle.Turtle(visible=False)
    missile.speed(0)
    missile.color('white')
    missile.penup()
    missile.setpos(x=BASE_X, y=BASE_Y)
    missile.pendown()
    heading = calc_heading(x1=BASE_X, y1=BASE_Y, x2=x, y2=y)
    missile.setheading(heading)
    missile.showturtle()
    info = {'missile': missile, 'target': [x, y],
            'state': 'launched', 'radius': 0}
    our_missiles.append(info)

window.onclick(fire_missile)

def generate_enemy_missile():
    x = random.randint(SKY_X_MIN, SKY_X_MAX)
    y = SKY_Y
    missile = turtle.Turtle(visible=False)
    missile.speed(0)
    missile.color('red')
    missile.penup()
    missile.setpos(x=x, y=y)
    missile.pendown()
    heading = calc_heading(x, y, x2=BASE_X, y2=BASE_Y)
    missile.setheading(heading)
    missile.showturtle()
    info = {'missile': missile, 'target': [BASE_X, BASE_Y],
            'state': 'launched', 'radius': 0}
    enemy_missiles.append(info)


our_missiles = []
enemy_missiles = []

numberTic = 0

def drawMissile(info):
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

while True:
    window.update()

    for info in our_missiles:
        drawMissile(info)
    for info in enemy_missiles:
        drawMissile(info)

    dead_missiles = [info for info in our_missiles if info['state'] == 'dead']
    for dead in dead_missiles:
        our_missiles.remove(dead)


    if  numberTic % random.randint(20, 100) == 0:
        generate_enemy_missile()
        numberTic = 0
    numberTic += 1
