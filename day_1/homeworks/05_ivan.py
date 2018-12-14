# -*- coding: utf-8 -*-

from math import degrees, acos
from turtle import Screen, Turtle
from random import randint


# координаты базы:
BASE_X, BASE_Y = 0, -300
# зададим уровень сложности (максимальное количество вражеских ракет):
N = 10


class Missile(Turtle):
    """Класс, который создает объект ракеты.
    По умолчанию создаются ракеты, запускаемые с базы.

    Для создания вражеских ракет нужно передать в
    конструктор класса все параметры:
        x, y - координаты базы (BASE_X и BASE_Y);
        pos_x, pos_y - начальные координаты ракеты;
        color='red' - задаст для вражеских ракет красный цвет
    """
    def __init__(self, x, y, pos_x=BASE_X, pos_y=BASE_Y, color='white'):
        # начальные настройки:
        super().__init__(visible=False)
        self.penup()
        self.speed(0)
        self.color = self.color(color)
        self.target = (x, y)
        self.setpos(pos_x, pos_y)
        # изменяемые атрибуты:
        self.state = 'launched'
        self.radius = 0


def calc_heading(x2, y2, x1, y1):
    """Функция для вычисления направления полета ракеты"""
    dx = x2 - x1
    dy = y2 - y1
    length = (dx ** 2 + dy ** 2) ** 0.5
    cos_alpha = dx / length
    alpha = degrees(acos(cos_alpha))
    if dy < 0:
        alpha = -alpha
    return alpha


def fire_missile(x, y, pos_x=BASE_X, pos_y=BASE_Y):
    """Функция, запускающая ракету"""
    if pos_x != BASE_X:
        missile = Missile(x=BASE_X, y=BASE_Y, pos_x=pos_x, pos_y=pos_y, color='red')
        heading = calc_heading(x1=pos_x, y1=pos_y, x2=BASE_X, y2=BASE_Y)
    else:
        missile = Missile(x, y)
        heading = calc_heading(x1=pos_x, y1=pos_y, x2=x, y2=y)
    missile.pendown()
    missile.setheading(heading)
    missile.showturtle()
    missiles.append(missile)


# создаем окно игры:
window = Screen()
window.setup(1200 + 3, 800 + 3)
window.bgpic("images/background.png")
window.screensize(1200, 800)
# window.tracer(n=2, delay=0)

# инициализируем список для хранения объектов ракет:
missiles = []

# Запускаем вражеские ракеты:
for i in range(1, randint(2, N+1)):
    fire_missile(x=BASE_X, y=BASE_Y, pos_x=randint(-600, 600), pos_y=400)

# главный цикл игры:
while True:
    window.update()
    window.onclick(fire_missile)

    for missile in missiles:
        if missile.state == 'launched':
            missile.forward(4)
            if missile.distance(x=missile.target[0], y=missile.target[1]) < 20:
                missile.state = 'explode'
                missile.shape('circle')
        elif missile.state == 'explode':
            missile.radius += 1
            if missile.radius > 5:
                missile.clear()
                missile.hideturtle()
                missile.state = 'dead'
            else:
                missile.shapesize(missile.radius)

    dead_missiles = [item for item in missiles if item.state == 'dead']
    for dead in dead_missiles:
        missiles.remove(dead)
