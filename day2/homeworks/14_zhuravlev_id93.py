# -*- coding: utf-8 -*-

import os
import random
import turtle

BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

window = turtle.Screen()
window.setup(1200 + 3, 800 + 3)
window.bgpic(os.path.join(BASE_PATH, "images", "background.png"))
window.screensize(1200, 800)
window.tracer(n=10)

ENEMY_COUNT = 5

BASE_X, BASE_Y = 0, -300


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


class Building(turtle.Turtle):

    def __init__(self, x, y):
        super().__init__()
        self.hideturtle()
        self.speed(0)
        self.penup()
        self.setpos(x, y)
        # задаем изображения для зданий:
        if x == BASE_X and y == BASE_Y:
            self.image = 'base.gif'
        else:
            self.image = random.choice(buildings_images)
        pic_path = os.path.join(BASE_PATH, "images", self.image.format('1'))
        window.register_shape(pic_path)
        self.shape(pic_path)
        self.showturtle()
        # задаем какое максимальное здоровье будет у различных зданий:
        if self.image in ('kremlin_1.gif', 'house_1.gif'):
            self.health = 1000
        elif self.image in ('nuclear_1.gif', 'skyscraper_1.gif'):
            self.health = 1500
        else:
            self.health = 2000
        self.x = x
        self.y = y

    def check_impact(self, enemy_missiles):
        """Метод проверяет, долетела ли вражеская ракета до здания,
        если да, то уменьшает здоровье здания на 100 единиц.

        Также метод подставляет изображение горящего или разрушенного
        здания в зависимости от уровня здоровья у здания.

        В случае если здоровье здания равно 0, то здание удаляется из
        списка зданий и ракеты больше не летят в его сторону"""

        global buildings
        for enemy_missile in enemy_missiles:
            if enemy_missile.state != 'explode':
                continue
            if enemy_missile.distance(self.x, self.y) < enemy_missile.radius * 10:
                self.health -= 100
        if self.health <= 0:
            buildings.remove(self)
            buildings_coordinates.remove((self.x, self.y))
        elif self.health <= 100:
            self.check_image(3)
        elif self.health <= 500:
            self.check_image(2)


    def check_image(self, number):
        pic_path = os.path.join(BASE_PATH, "images", self.image.format(str(number)))
        window.register_shape(pic_path)
        self.shape(pic_path)

def fire_missile(x, y):
    info = Missile(color='white', x=BASE_X, y=BASE_Y, x2=x, y2=y)
    our_missiles.append(info)


def fire_enemy_missile(target_x, target_y):
    x = random.randint(-600, 600)
    y = 400
    info = Missile(color='red', x=x, y=y, x2=target_x, y2=target_y)
    enemy_missiles.append(info)


def move_missiles(missiles):
    for missile in missiles:
        missile.step()

    dead_missiles = [missile for missile in missiles if missile.state == 'dead']
    for dead in dead_missiles:
        missiles.remove(dead)


def check_enemy_count():
    if len(enemy_missiles) < ENEMY_COUNT:
        x, y = random.choice(buildings_coordinates)
        fire_enemy_missile(target_x=x, target_y=y)


def check_interceptions():
    for our_missile in our_missiles:
        if our_missile.state != 'explode':
            continue
        for enemy_missile in enemy_missiles:
            if enemy_missile.distance(our_missile.x, our_missile.y) < our_missile.radius * 10:
                enemy_missile.state = 'dead'


def game_over():
    for item in buildings:
        if item.x == BASE_X:
            return item.health < 0


window.onclick(fire_missile)
# координаты зданий:
buildings_coordinates = [(-480, BASE_Y),
                         (-240, BASE_Y),
                         (BASE_X, BASE_Y),
                         (240, BASE_Y),
                         (480, BASE_Y)]
# пути к изображениям зданий:
buildings_images = ('house_{}.gif', 'nuclear_{}.gif', 'skyscraper_{}.gif', 'kremlin_{}.gif')

our_missiles = []
enemy_missiles = []

# генерируем список зданий:
buildings = [Building(x, y) for x, y in buildings_coordinates]

while True:
    print(len(buildings))
    for building in buildings:
        building.check_impact(enemy_missiles)
    window.update()
    if game_over():
        continue
    check_enemy_count()
    check_interceptions()
    move_missiles(missiles=our_missiles)
    move_missiles(missiles=enemy_missiles)