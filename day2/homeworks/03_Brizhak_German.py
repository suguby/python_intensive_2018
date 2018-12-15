# -*- coding: utf-8 -*-

import os
import random
import turtle

BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

window = turtle.Screen()
window.setup(1200, 800)
window.bgpic(os.path.join(BASE_PATH, "images", "background.png"))
window.tracer(n=2)

ENEMY_COUNT = 5

BASE_X = 0
BUILDINGS_Y = -300

BUILDING_POSITIONS = (-400, -200, 0, 200, 400)


class Missile:

    def __init__(self, pos, color, target):
        self.color = color

        pen = turtle.Turtle(visible=False)
        pen.speed(0)
        # pic_path = os.path.join(BASE_PATH, "images", "missile.gif")
        # window.register_shape(pic_path)
        # pen.shape(pic_path)
        pen.color(color)
        pen.penup()
        pen.goto(pos)
        pen.pendown()
        heading = pen.towards(target)
        pen.setheading(heading)
        pen.showturtle()
        self.pen = pen

        self.state = 'launched'
        self.target = target
        self.radius = 0

    def step(self):
        if self.state == 'launched':
            self.pen.forward(4)
            if self.pen.distance(self.target) < 20:
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

    def distance(self, target):
        return self.pen.distance(target)

    @property
    def x(self):
        return self.pen.xcor()

    @property
    def y(self):
        return self.pen.ycor()


class Building:

    images = {
        'base': ('base.gif', 'base.gif', 'base.gif'),
        'house': ('house_1.gif', 'house_2.gif', 'house_3.gif'),
        'kremlin': ('kremlin_1.gif', 'kremlin_2.gif', 'kremlin_3.gif'),
        'nuclear': ('nuclear_1.gif', 'nuclear_2.gif', 'nuclear_3.gif'),
        'skyscraper': ('skyscraper_1.gif', 'skyscraper_2.gif', 'skyscraper_3.gif')
    }

    def __init__(self, pos, building_type, health):
        building = turtle.Turtle(visible=False)
        building.speed(0)
        building.penup()
        building.goto(pos)
        self.images = Building.images[building_type]
        pic_path = os.path.join(BASE_PATH, "images", self.images[0])
        window.register_shape(pic_path)
        building.shape(pic_path)
        building.showturtle()
        self.building = building

        self.pos = pos
        self.health = health
        self.full_health = health

    def check_impact(self):
        for enemy_missile in enemy_missiles:
            if enemy_missile.state != 'explode':
                continue
            if enemy_missile.distance(self.pos) < enemy_missile.radius * 10:
                self.health -= 100
                if self.health <= self.full_health // 2:
                    self.building.hideturtle()
                    pic_path = os.path.join(BASE_PATH, "images", self.images[1])
                    window.register_shape(pic_path)
                    self.building.shape(pic_path)
                    self.building.showturtle()
                if self.health < 0:
                    self.building.hideturtle()
                    pic_path = os.path.join(BASE_PATH, "images", self.images[2])
                    window.register_shape(pic_path)
                    self.building.shape(pic_path)
                    self.building.showturtle()

    def is_dead(self):
        return self.health < 0


def fire_missile(x, y):
    info = Missile(color='white', pos=(BASE_X, BUILDINGS_Y), target=(x, y))
    our_missiles.append(info)


def fire_enemy_missile():
    x = random.randint(-600, 600)
    y = 400
    info = Missile(color='red', pos=(x, y), target=(BUILDING_POSITIONS[random.randint(0, 4)], BUILDINGS_Y))
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
            if enemy_missile.distance((our_missile.x, our_missile.y)) < our_missile.radius * 10:
                enemy_missile.state = 'dead'


def draw_buildings():
    building_types = ('house', 'kremlin', 'nuclear', 'skyscraper')
    health = (1000, 5000, 4000, 3000)

    for x in BUILDING_POSITIONS:
        if x == 0:
            buildings.append(Building(pos=(BASE_X, BUILDINGS_Y), building_type='base', health=2000))
        else:
            n = random.randint(0, 3)
            buildings.append(Building(pos=(x, BUILDINGS_Y), building_type=building_types[n], health=health[n]))


def game_over():
    return all(building.is_dead() for building in buildings)


def check_impact():
    for building in buildings:
        building.check_impact()


our_missiles = []
enemy_missiles = []
buildings = []

window.onclick(fire_missile)

draw_buildings()

while True:
    window.update()
    if game_over():
        continue
    check_impact()
    check_enemy_count()
    check_interceptions()
    move_missiles(missiles=our_missiles)
    move_missiles(missiles=enemy_missiles)

