# -*- coding: utf-8 -*-

import math
import turtle
import random

window = turtle.Screen()
window.screensize(1200, 800)
window.setup(1200 + 25, 800 + 25)
window.bgpic('images/background.png')
window.tracer(2)

BASE_X, BASE_Y = 0, -300


def calc_heading(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    lenght = (dx ** 2 + dy ** 2) ** 0.5
    cos_alpha = dx / lenght
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
    # missile.forward(500)
    # missile.shape("circle")
    # missile.shapesize(2)
    # missile.shapesize(3)
    # missile.shapesize(4)
    # missile.shapesize(5)
    # missile.clear()
    # missile.hideturtle()
    info = {'missile': missile, 'target': [x, y], 'state': 'launched', 'radius': 0}
    missiles.append(info)

def enemy_fire_missile():
    enemy_missile = turtle.Turtle(visible=False)
    enemy_missile.speed(0)
    enemy_missile.color('red')
    enemy_missile.penup()
    x1 = random.randint(-550, 550)
    y1 = 300
    x2 = random.randint(-550, 550)
    y2 = -330
    enemy_missile.setpos(x=x1, y=y1)
    enemy_missile.pendown()
    heading = calc_heading(x1=x1, y1=y1, x2=x2, y2=y2)
    enemy_missile.setheading(heading)
    enemy_missile.showturtle()
    info = {'missile': enemy_missile, 'target': [x2, y2], 'state': 'launched', 'radius': 0}
    missiles.append(info)

window.onclick(fire_missile)

missiles = []

while True:
    window.update()

    en_fire = random.randint(1, 60)
    if en_fire ==1:
        enemy_fire_missile()

    for info in missiles:
        state = info['state']
        missile = info['missile']
        if state == 'launched':
            missile.forward(4)
            target = info['target']
            if missile.distance(x=target[0], y=target[1]) < 20:
                info['state'] = 'explode'
                missile.shape("circle")
        elif state == 'explode':
            info['radius'] += 1
            if info['radius'] > 4:
                info['state'] = 'dead'
                missile.clear()
                missile.hideturtle()
            else:
                missile.shapesize(info['radius'])

    dead_missiles = [info for info in missiles if info['state'] == 'dead']
    for dead in dead_missiles:
        missiles.remove(dead)