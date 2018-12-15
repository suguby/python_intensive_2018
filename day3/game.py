import math
import os
import random
import turtle

BASE_PATH = os.path.dirname(os.path.dirname(__file__))
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


class Building:
    INITIAL_HEALTH = 1000

    def __init__(self, x, y, name):
        self.name = name
        self.x = x
        self.y = y
        self.health = self.INITIAL_HEALTH

        pen = turtle.Turtle()
        pen.hideturtle()
        pen.speed(0)
        pen.penup()
        pen.setpos(x=self.x, y=self.y)
        pic_path = os.path.join(BASE_PATH, "images", self.get_pic_name())
        window.register_shape(pic_path)
        pen.shape(pic_path)
        pen.showturtle()
        self.pen = pen

    def get_pic_name(self):
        if self.health < self.INITIAL_HEALTH * 0.2:
            return f"{self.name}_3.gif"
        if self.health < self.INITIAL_HEALTH * 0.8:
            return f"{self.name}_2.gif"
        return f"{self.name}_1.gif"

    def draw(self):
        pic_name = self.get_pic_name()
        pic_path = os.path.join(BASE_PATH, "images", pic_name)
        if self.pen.shape() != pic_path:
            window.register_shape(pic_path)
            self.pen.shape(pic_path)

    def is_alive(self):
        return self.health > 0


class MissileBase(Building):
    INITIAL_HEALTH = 2000

    def get_pic_name(self):
        for missile in our_missiles:
            if missile.distance(self.x, self.y) < 50:
                pic_name = f"{self.name}_opened.gif"
                break
        else:
            pic_name = f"{self.name}.gif"
        return pic_name


def fire_missile(x, y):
    info = Missile(color='white', x=BASE_X, y=BASE_Y + 30, x2=x, y2=y)
    our_missiles.append(info)


def fire_enemy_missile():
    x = random.randint(-600, 600)
    y = 400
    alive_buildings = [building for building in buildings if building.is_alive()]
    if alive_buildings:
        target = random.choice(alive_buildings)
        info = Missile(color='red', x=x, y=y, x2=target.x, y2=target.y)
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


def game_over():
    return base.health < 0


def check_impact():
    for enemy_missile in enemy_missiles:
        if enemy_missile.state != 'explode':
            continue
        for building in buildings:
            if enemy_missile.distance(building.x, building.y) < enemy_missile.radius * 10:
                building.health -= 100
                print(f'{building.name} - {building.health}')


window = turtle.Screen()
window.setup(1200 + 3, 800 + 3)
window.bgpic(os.path.join(BASE_PATH, "images", "background.png"))
window.screensize(1200, 800)
window.tracer(n=2)
window.onclick(fire_missile)

our_missiles = []
enemy_missiles = []
buildings = []


base = MissileBase(x=BASE_X, y=BASE_Y, name='base')
buildings.append(base)

building_infos = {
    'house': [BASE_X - 400, BASE_Y],
    'kremlin': [BASE_X - 200, BASE_Y],
    'nuclear': [BASE_X + 200, BASE_Y],
    'skyscraper': [BASE_X + 400, BASE_Y]
}

for name, position in building_infos.items():
    building = Building(x=position[0], y=position[1], name=name)
    buildings.append(building)


def draw_buildings():
    for building in buildings:
        building.draw()


while True:
    window.update()
    if game_over():
        continue
    draw_buildings()
    check_impact()
    check_enemy_count()
    check_interceptions()
    move_missiles(missiles=our_missiles)
    move_missiles(missiles=enemy_missiles)
