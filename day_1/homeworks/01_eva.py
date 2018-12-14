# -*- coding: utf-8 -*-

import math
import os
import turtle
import random
import time

BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

window = turtle.Screen()
window.setup(1200 + 3, 800 + 3)
window.bgpic(os.path.join(BASE_PATH, "images", "background.png"))
window.screensize(1200, 800)
# window.tracer(n=2)

BASE_X, BASE_Y = 0, -300


def calc_heading(x1, y1,x2, y2):
    dx = x2-x1
    dy = y2 - y1
    length = (dx ** 2 + (dy) ** 2) ** 0.5
    cos_alpha = dx / length
    alpha = math.acos(cos_alpha)
    alpha = math.degrees(alpha)
    if dy < 0:
        alpha =- alpha
    return alpha


def fire_missile(x, y):
    missile = turtle.Turtle(visible=False)
    missile.speed(0)
    missile.color("white")
    missile.penup()
    missile.setpos(x=BASE_X, y=BASE_Y)
    missile.pendown()
    heading = calc_heading(x1=BASE_X, y1=BASE_Y, x2=x, y2=y)
    missile.setheading(heading)
    missile.showturtle()
    info = {"missile": missile, "target": [x, y],
            "state": "launched", "radius": 0}
    our_missiles.append(info)

def against_missile():
    c = random.randint(-1000, 1000)
    m = turtle.Turtle(visible=False)
    m.speed(0)
    m.color("red")
    m.penup()
    m.setpos(x=c, y=800)
    m.pendown()
    m.showturtle()
    heading1 = calc_heading(x1=c, y1=800, x2=BASE_X, y2=BASE_Y)
    m.setheading(heading1)
    #while m.distance(x=BASE_X, y=BASE_Y) > 10:
    #    m.forward(4)
    a_info = {"missile": m, "target": [BASE_X, BASE_Y],
              "state": "launched", "radius": 0}
    a_missiles.append(a_info)

window.onclick(fire_missile)
our_missiles = []
a_missiles = []
for i in range(1,5,1):
    against_missile()
while True:
    window.update()
    for info in our_missiles:
        state = info["state"]
        missile = info["missile"]
        if state == "launched":
            missile.forward(4)
            target = info["target"]
            if missile.distance(x=target[0], y=target[1]) < 20:
                info["state"] = "explode"
                missile.shape("circle")
        elif state == "explode":
            info["radius"] += 1
            if info["radius"] > 5:
                missile.clear()
                missile.hideturtle()
                info['state'] = 'dead'
            else:
                missile.shapesize(info["radius"])

    for a_info in a_missiles:
        state = a_info["state"]
        m = a_info["missile"]
        if state == "launched":
            m.forward(4)
            target = a_info["target"]
            if m.distance(x=target[0], y=target[1]) < 20:
                info["state"] = "explode"
                m.shape("circle")
                a_missiles.remove(a_info)
                m.clear()
                m.hideturtle()
        elif state == "explode":
            a_info['state'] = 'dead'

    dead_missiles = [info for info in our_missiles if info['state'] == 'dead']
    for dead in dead_missiles:
        our_missiles.remove(dead)
