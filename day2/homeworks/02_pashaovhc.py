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
BASE_BUILDINGS = [['house_1.gif', 'house_2.gif', 'house_3.gif'], ['kremlin_1.gif', 'kremlin_2.gif', 'kremlin_3.gif'],
                  ['base.gif', 'base.gif', 'base.gif'], ['nuclear_1.gif', 'nuclear_2.gif', 'nuclear_3.gif'],
                  ['skyscraper_1.gif', 'skyscraper_2.gif', 'skyscraper_3.gif']]


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


class Buildings:

    def __init__(self, x, y, health, picture):

        self.x = x
        self.y = y
        self.health = health
        self.picture = picture

        pic_path = os.path.join(BASE_PATH, "images", self.picture[0])
        window.register_shape(pic_path)
        building = turtle.Turtle()
        building.hideturtle()
        building.speed(0)
        building.penup()
        building.setpos(x=x, y=y)
        building.shape(pic_path)
        building.showturtle()

        self.building = building

    def check_health(self):  # Не знаю как это упростить
        if (self.health <= 1400 and self.health) > 0:
            pic_path = os.path.join(BASE_PATH, "images", self.picture[1])
            window.register_shape(pic_path)
            self.building.shape(pic_path)
        elif self.health < 0:
            pic_path = os.path.join(BASE_PATH, "images", self.picture[2])
            window.register_shape(pic_path)
            self.building.shape(pic_path)


def game_map():
    x = -400
    health = 2100
    for pictures in BASE_BUILDINGS:
        info = Buildings(x=x, y=BASE_Y, health=health, picture=pictures)
        our_buildings.append(info)
        x += 200


def game_over():
    return our_buildings[2].health < 0


def check_impact():
    for enemy_missile in enemy_missiles:
        if enemy_missile.state != 'explode':
            continue
        for building in our_buildings:
            building.check_health()
            if enemy_missile.distance(building.x, BASE_Y) < enemy_missile.radius * 10:
                building.health -= 100
                # print('base_health', base_health)


def fire_missile(x, y):
    info = Missile(color='white', x=BASE_X, y=BASE_Y, x2=x, y2=y)
    our_missiles.append(info)


def fire_enemy_missile():
    x = random.randint(-600, 600)
    y = 400
    xrange = random.randrange(-400, 400, 200)
    info = Missile(color='red', x=x, y=y, x2=xrange, y2=BASE_Y)
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
our_buildings = []

game_map()


while True:
    window.update()

    if game_over():
        continue

    check_impact()
    check_enemy_count()
    check_interceptions()
    move_missiles(missiles=our_missiles)
    move_missiles(missiles=enemy_missiles)
