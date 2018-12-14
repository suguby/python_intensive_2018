# -*- coding: utf-8 -*-

import math
import os
import random
import turtle

BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

window = turtle.Screen()
window.bgpic(os.path.join(BASE_PATH, "images", "background.png"))
window.setup(1200 + 3, 800 + 3)
window.screensize(1200, 800)
#window.tracer(n=2)

BASE_X, BASE_Y = 0, -300


# def calc_heading(x1, y1, x2, y2):
#     dx = x2-x1
#     dy = y2-y1
#     length = (dx ** 2 + dy ** 2) ** 0.5
#     cos_alpha = dx / length
#     alpha = math.acos(cos_alpha)
#     alpha = math.degrees(alpha)
#     if dy < 0:
#         alpha = -alpha
#     return alpha


def create_missile(side, x1, y1, x2, y2):
    missile = turtle.Turtle(visible=False)
    missile.speed(0)
    if side == 'our':
        missile.color('white')
    elif side == 'enemy':
        missile.color('red')
    missile.penup()
    missile.setpos(x=x1, y=y1)
    missile.pendown()
    # heading = calc_heading(x1=x1, y1=y1, x2=x2, y2=y2)
    heading = missile.towards(x2, y2)
    missile.setheading(heading)
    missile.showturtle()
    info = {'missile': missile, 'target': [x2, y2],
            'state': 'launched', 'radius': 0,
            'side': side}
    missiles.append(info)


def fire_our_missile(x, y):
    create_missile(side='our', x1=BASE_X, y1=BASE_Y, x2=x, y2=y)


def fire_enemy_missile():
    half_width = divmod(window.window_width(), 2)[0]
    half_height = divmod(window.window_height(), 2)[0]
    x1 = random.randint(-half_width, half_width)
    y1 = half_height
    create_missile(side='enemy', x1=x1, y1=y1, x2=BASE_X, y2=BASE_Y)


missiles = []

window.onclick(fire_our_missile)
for i in range(random.randint(3, 5)):
    fire_enemy_missile()

while True:
    window.update()

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
