# -*- coding: utf-8 -*-

import math
import os
import turtle
import random
import array

# cylinder
# BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
# from array import *
# BASE_Y = array('i', [-550, -450, -300, 450, 550])


# Не успел сделать повреждения по другим зданиям, кроме основной базы


window = turtle.Screen()
window.setup(1200 + 3, 800 + 3)
window.bgpic("../../images/background.png")
window.screensize(1200, 800)
window.tracer(n=2)

from array import array

numbers = array('i', [-500, -250, 0, 250, 500])

ENEMY_COUNT = 5
BASE_Y,BASE_X = -300, 0
base_health = 2000


class Missile:

    def __init__(self, x, y, color, x2, y2):
        # self.x = x
        # self.y = y
        self.color = color

        pen = turtle.Turtle(visible=False)
        # pen.shape("images/missile.gif")
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
                self.state = "explode"
                self.pen.shape("circle")
        elif self.state == "explode":
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


class Building:

    def __init__(self, x, y, pic_path, base_health):
        base = turtle.Turtle()
        base.hideturtle()
        base.speed(0)
        base.penup()
        base.setpos(x=x, y=y)
        window.register_shape(pic_path)
        base.shape(pic_path)
        base.showturtle()
        self.base = base
        self.base_health = base_health


def building_position():
    base_health = 2000
    info = Building(x=numbers[2], y=BASE_Y, pic_path=('../../images/base.gif'), base_health=base_health)
    base_positions.append(info)


def house_building_position():
    base_health = 1000
    info = Building(x=numbers[0], y=BASE_Y, pic_path=('../../images/house_1.gif'), base_health=base_health)
    base_positions.append(info)


def kremlin_building_position():
    base_health = 1000
    info = Building(x=numbers[1], y=BASE_Y, pic_path=('../../images/kremlin_1.gif'), base_health=base_health)
    base_positions.append(info)


def nuclear_building_position():
    base_health = 1000
    info = Building(x=numbers[3], y=BASE_Y, pic_path=('../../images/nuclear_1.gif'), base_health=base_health)
    base_positions.append(info)


def scyscraper_building_position():
    base_health = 1000
    info = Building(x=numbers[4], y=BASE_Y, pic_path=('../../images/skyscraper_1.gif'), base_health=base_health)
    base_positions.append(info)


def fire_missile(x, y):
    info = Missile(color='white', x=numbers[2], y=BASE_Y, x2=x, y2=y)
    our_missiles.append(info)


def fire_enemy_missile():
    i = random.randint(0, 4)
    x = random.randint(-600, 600)
    y = 400
    BASE_X = numbers[i]
    info = Missile(color='red', x=x, y=y, x2=BASE_X, y2=BASE_Y)
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
base_positions = []
building_position()
house_building_position()
kremlin_building_position()
nuclear_building_position()
scyscraper_building_position()


def game_over():
    return base_health < 0


def check_impact():
    global base_health
    for enemy_missile in enemy_missiles:
        if enemy_missile.state != 'explode':
            continue
        if enemy_missile.distance(BASE_X, BASE_Y) < enemy_missile.radius * 10:
            base_health -= 100
            # print('base_health', base_health)


while True:
    window.update()
    if game_over():
        continue
    check_impact()
    check_enemy_count()
    check_interceptions()
    move_missiles(missiles=our_missiles)
    move_missiles(missiles=enemy_missiles)