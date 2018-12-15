# -*- coding: utf-8 -*-

# Код не оптимизирован и не просушен (весь день в разъездах)

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

# координаты зданий (переделать на словарь)
BASE_X, BASE_Y = 0, -300
KREMLIN_X, KREMLIN_Y = -200, -300
NUCLEAR_X, NUCLEAR_Y = -400, -300
HOUSE_X, HOUSE_Y = 400, -300
SKYSCRAPER_X, SKYSCRAPER_Y = 200, -300

# картинки зданий (переделать на словарь)
BASE_PIC = "base.gif"
KREMLIN_PIC = "kremlin_1.gif"
NUCLEAR_PIC = "nuclear_1.gif"
HOUSE_PIC = "house_1.gif"
SKYSCRAPER_PIC = "skyscraper_1.gif"

# прочность зданий - предполагаем, что здания имеют разную прочность(переделать на словарь)
BASE_HEALTH = 2000
KREMLIN_HEALTH = 1500
NUCLEAR_HEALTH = 1000
HOUSE_HEALTH = 500
SKYSCRAPER_HEALTH = 500

# Здоровье необходимо считать по каждому зданию
building_health = 2000


class Building:

    def __init__(self, x, y, health, pic_name):
        self.health = health

        pen = turtle.Turtle()
        pen.hideturtle()
        pen.speed(0)
        pen.penup()
        pen.setpos(x=x, y=y)
        pic_path = os.path.join(BASE_PATH, "images", pic_name)
        window.register_shape(pic_path)
        pen.shape(pic_path)
        pen.showturtle()
        self.pen = pen

    @property
    def bld_health(self):
        return self.health


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


def setup_building(building_name):
    if building_name == "base":
        info = Building(x=BASE_X, y=BASE_Y, health=BASE_HEALTH, pic_name=BASE_PIC)
    elif building_name == "kremlin":
        info = Building(x=KREMLIN_X, y=KREMLIN_Y, health=KREMLIN_HEALTH, pic_name=KREMLIN_PIC)
    elif building_name == "nuclear":
        info = Building(x=NUCLEAR_X, y=NUCLEAR_Y, health=NUCLEAR_HEALTH, pic_name=NUCLEAR_PIC)
    elif building_name == "house":
        info = Building(x=HOUSE_X, y=HOUSE_Y, health=HOUSE_HEALTH, pic_name=HOUSE_PIC)
    elif building_name == "skyscraper":
        info = Building(x=SKYSCRAPER_X, y=SKYSCRAPER_Y, health=SKYSCRAPER_HEALTH, pic_name=SKYSCRAPER_PIC)
    our_buildings.append(info)


def fire_missile(x, y):
    info = Missile(color='white', x=BASE_X, y=BASE_Y, x2=x, y2=y)
    our_missiles.append(info)


def fire_enemy_missile():
    x = random.randint(-600, 600)
    y = 400
    # info = Missile(color='red', x=x, y=y, x2=BASE_X, y2=BASE_Y)
    info = Missile(color='red', x=x, y=y, x2=random.choice([BASE_X, KREMLIN_X, NUCLEAR_X, HOUSE_X, SKYSCRAPER_X]),
                   y2=random.choice([BASE_Y, KREMLIN_Y, NUCLEAR_Y, HOUSE_Y, SKYSCRAPER_Y]))
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


def game_over():
    return building_health < 0


def check_impact():
    global building_health
    for enemy_missile in enemy_missiles:
        if enemy_missile.state != 'explode':
            continue
        if enemy_missile.distance(BASE_X, BASE_Y) < enemy_missile.radius * 10:
            building_health -= 100
            # print('building_health', building_health)


setup_building(building_name="base")
setup_building(building_name="kremlin")
setup_building(building_name="nuclear")
setup_building(building_name="house")
setup_building(building_name="skyscraper")

while True:
    window.update()
    if game_over():
        continue
    check_impact()
    check_enemy_count()
    check_interceptions()
    move_missiles(missiles=our_missiles)
    move_missiles(missiles=enemy_missiles)
