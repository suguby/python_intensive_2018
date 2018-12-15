# -*- coding: utf-8 -*-

import math
import os
import random
import turtle

BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

window = turtle.Screen()
window.setup(1200 + 3, 800 + 3)
window.bgpic(os.path.join(BASE_PATH, "images", "background.png"))
window.screensize(1200, 800)
window.tracer(n=2)

ENEMY_COUNT = 5

BASE_X, BASE_Y = 0, -300
BASE_HEALH = 1000

class Base:
    def __init__(self, x, y, base_name, index):
        self.x = x
        self.y = y
        self.base_health = BASE_HEALH
        self.index = index
        base = turtle.Turtle()
        base.hideturtle()
        base.speed(0)
        base.penup()
        base.setposition(x=x, y=y-70)
        base.color('white')
        base.write(arg=self.base_health, align="center", font = ("Arial", 12))
        base.setposition(x=x, y=y)
        pic_path = os.path.join(BASE_PATH, "images", base_name)
        window.register_shape(pic_path)
        base.shape(pic_path)
        base.showturtle()
        self.base = base


class Missile:

    def __init__(self, x, y, color, x2, y2):
        self.color = color

        pen = turtle.Turtle(visible=False)
        pen.speed(0)
        pen.color(color)
        pen.penup()
        pen.setpos(x=x, y=y)
        pen.pendown()
        heading = pen.towards(x2, y2)
        pen.setheading(heading)
        pen.showturtle()
        self.pen = pen

        self.state = 'launched'
        self.target = x2, y2
        self.radius = 0

    def step(self):
        if self.state == 'launched':
            self.pen.forward(4)
            if self.pen.distance(x=self.target[0], y=self.target[1]) < 20:
                self.state = 'explode'
                self.pen.shape('circle')
        elif self.state == 'explode':
            self.radius += 1
            if self.radius > 5:
                self.pen.clear()
                self.pen.hideturtle()
                self.state = 'dead'
            else:
                self.pen.shapesize(self.radius)
        elif self.state == 'dead':
            self.pen.clear()
            self.pen.hideturtle()

    def distance(self, x, y):
        return self.pen.distance(x=x, y=y)

    @property
    def x(self):
        return self.pen.xcor()

    @property
    def y(self):
        return self.pen.ycor()


def fire_missile(x, y):
    info = Missile(color='white', x=BASE_X, y=BASE_Y, x2=x, y2=y)
    our_missiles.append(info)


def fire_enemy_missile():
    x = random.randint(-600, 600)
    y = 400
    info = Missile(color='red', x=x, y=y, x2=random.randint(BASE_X-400, BASE_X+400), y2=BASE_Y)
    enemy_missiles.append(info)


def move_missiles(missiles):
    for missile in missiles:
        missile.step()

    dead_missiles = [missile for missile in missiles if missile.state == 'dead']
    for dead in dead_missiles:
        missiles.remove(dead)


def check_enemy_count():
    if len(enemy_missiles) < ENEMY_COUNT:
        fire_enemy_missile()


def check_interceptions():
    for our_missile in our_missiles:
        if our_missile.state != 'explode':
            continue
        for enemy_missile in enemy_missiles:
            if enemy_missile.distance(our_missile.x, our_missile.y) < our_missile.radius * 10:
                enemy_missile.state = 'dead'


window.onclick(fire_missile)

our_missiles = []
enemy_missiles = []
our_bases_name = [[-400, 'kremlin_1.gif', 'kremlin_2.gif', 'kremlin_3.gif'], \
                  [-200, 'house_1.gif', 'house_2.gif', 'house_3.gif'], \
                  [BASE_X, 'base.gif', 'base.gif', 'base.gif'], \
                  [200, 'nuclear_1.gif', 'nuclear_2.gif', 'nuclear_3.gif'], \
                  [400, 'skyscraper_1.gif', 'skyscraper_2.gif', 'skyscraper_3.gif']]


def game_over():
    result = True
    for base_info in base:
        result = result and (base_info.base_health <0)
    return result


def base_new_name(base_info, index):
    if index != base_info.index:
        base_info.base.hideturtle()
        pic_path = os.path.join(BASE_PATH, "images", our_bases_name[base_info.index][index])
        window.register_shape(pic_path)
        base_info.base.shape(pic_path)
        base_info.base.showturtle()

def check_impact():
    #global base
    for enemy_missile in enemy_missiles:
        if enemy_missile.state != 'explode':
            continue
        for base_info in base:
            if enemy_missile.distance(base_info.x, BASE_Y) < enemy_missile.radius * 10:
                base_info.base_health -= 100
                base_info.base.setposition(base_info.x, base_info.y-70)
                base_info.base.clear()
                base_info.base.write(base_info.base_health, align="center", font = ("Arial", 12))
                base_info.base.setposition(base_info.x, base_info.y)
                if base_info.base_health<=0:
                    base_new_name(base_info, 3)
                elif base_info.base_health<=BASE_HEALH//2:
                    base_new_name(base_info, 2)
                # print('base_health', base_health)

i = 0
base = []
for base_name in our_bases_name:
    base.append(Base(x=base_name[0], y=BASE_Y, base_name=base_name[1], index=i))
    i += 1


while True:
    window.update()
    if game_over():
        continue
    check_impact()
    check_enemy_count()
    check_interceptions()
    move_missiles(missiles=our_missiles)
    move_missiles(missiles=enemy_missiles)
