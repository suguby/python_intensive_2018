# -*- coding: utf-8 -*-

import turtle
import os
import random

BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

window = turtle.Screen()
window.setup(1200, 800)
window.bgpic(os.path.join(BASE_PATH, "images", "background.png"))
window.tracer(n=2)

BASE_X, BASE_Y = 0, -320
OUR_COLOR = 'yellow'
ENEMY_BASE_Y = 400
ENEMY_COUNT = 5
ENEMY_COLOR = 'red'

missile_speed = 4
derivation = 50


class Building:

    def __init__(self, x, y, health, picture_name):
        self.x = x
        self.y = y
        self.common_health = self.remain_health = health
        self.picture_name = picture_name
        building = turtle.Turtle()
        building.hideturtle()
        building.speed(0)
        building.penup()
        building.setpos(x=x, y=y)
        self.building = building
        self.set_picture()
        title = turtle.Turtle()
        title.hideturtle()
        title.speed(0)
        title.penup()
        title.setpos(x=x, y=y - 65)
        title.write(str(self.remain_health), align="center", font=["Arial", 10, "bold"])
        self.title = title

    def choose_picture(self):
        if self.picture_name == 'base':
            picture_name_string = "base.gif"
        else:
            picture_name_string = self.picture_name
            if self.remain_health < 0:
                picture_name_string += '_3'
            elif self.remain_health < self.common_health / 2:
                picture_name_string += '_2'
            else:
                picture_name_string += '_1'
            picture_name_string += '.gif'
        return os.path.join(BASE_PATH, "images", picture_name_string)

    def set_picture(self):
        self.building.hideturtle()
        building_pic = self.choose_picture()
        window.register_shape(building_pic)
        self.building.shape(building_pic)
        self.building.showturtle()

    def in_exploded_radius(self, exploded_missile):
        if exploded_missile.distance(self.x, self.y) < exploded_missile.radius * 10:
            self.remain_health -= 100
            self.set_picture()
            self.title.clear()
            self.title.write(str(self.remain_health), align="center", font=["Arial", 10, "bold"])


class Missile:

    def __init__(self, start_x, start_y, color, target_x, target_y):
        pen = turtle.Turtle(visible=False)
        pen.hideturtle()
        pen.speed(0)
        pen.color(color)
        pen.penup()
        pen.setpos(x=start_x, y=start_y)
        pen.pendown()
        pen.setheading(pen.towards(x=target_x, y=target_y))
        pen.showturtle()
        self.color = color
        self.start_x = start_x
        self.start_y = start_y
        self.target_x = target_x
        self.target_y = target_y
        self.state = 'launched'
        self.radius = 0
        self.pen = pen

    def step(self):
        if self.state == 'launched':
            self.pen.forward(missile_speed)
            if self.pen.distance(x=self.target_x, y=self.target_y) < 10:
                self.state = 'explode'
                self.pen.shape("circle")
        elif self.state == 'explode':
            self.radius += 1
            if self.radius > 5:
                self.state = 'dead'
            else:
                self.pen.shapesize(self.radius)
        elif self.state == 'dead':
            self.pen.clear()
            self.pen.hideturtle()
            return 'dead'

    def distance(self, x, y):
        return self.pen.distance(x=x, y=y)

    def in_exploded_radius(self, exploded_missile):
        if self.state == 'launched':
            if self.distance(exploded_missile.x(), exploded_missile.y()) <= exploded_missile.radius * 10:
                self.state = 'dead'

    def x(self):
        return self.pen.xcor()

    def y(self):
        return self.pen.ycor()


def fire_missile(x, y):
    info = Missile(color=OUR_COLOR, start_x=BASE_X, start_y=BASE_Y, target_x=x, target_y=y)
    all_missiles.append(info)


def fire_enemy_missile():
    max_x = window.window_width() / 2
    start_x = random.randint(-max_x, max_x)
    remain_buildings = [building for building in buildings if building.remain_health > 0]
    target = random.randint(0, len(remain_buildings) - 1)
    target_x = remain_buildings[target].x + random.randint(-derivation, derivation)
    target_y = remain_buildings[target].y
    info = Missile(color=ENEMY_COLOR, start_x=start_x, start_y=ENEMY_BASE_Y, target_x=target_x, target_y=target_y)
    all_missiles.append(info)


def move_missiles(missiles_list):
    dead_missiles = []
    for missile in missiles_list:
        if missile.step() == 'dead':
            dead_missiles.append(missile)
    for dead in dead_missiles:
        missiles_list.remove(dead)


def check_enemy_count():
    enemy_missiles = [missile for missile in all_missiles if missile.color == ENEMY_COLOR]
    if len(enemy_missiles) < ENEMY_COUNT:
        fire_enemy_missile()


def check_blows():
    for missile in all_missiles:
        if missile.state == 'explode':
            for other_missile in all_missiles:
                other_missile.in_exploded_radius(missile)
            for building in buildings:
                building.in_exploded_radius(missile)


def game_over():
    return buildings[0].remain_health < 0


window.onclick(fire_missile)

all_missiles = []
our_missiles = []
enemy_missiles = []

buildings = [
    Building(0, BASE_Y, 2000, 'base'),
    Building(-400, BASE_Y, 600, 'house'),
    Building(-200, BASE_Y, 600, 'skyscraper'),
    Building(400, BASE_Y, 600, 'kremlin'),
    Building(200, BASE_Y, 600, 'nuclear'),
]

while True:
    window.update()
    check_blows()
    if game_over():
        break
    check_enemy_count()
    move_missiles(missiles_list=all_missiles)