import objects
import res
import random
import math
import pyglet

def create_asteroids(qty, bat, x=None, y=None, max=10, pos=([0], [1])):
    """

    :param qty: number of asteroids
    :param bat: the batch for drawing
    :return: list of asteroid sprites
    """

    asteroids = []

    get_random = x == None
    for i in range(qty):
        if get_random:
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            while math.sqrt((x - 400) ** 2 + (y - 300) ** 2 )< 100:
                x = random.randint(0, 800)
                y = random.randint(0, 600)

        scale = random.randint(3, max) / 10
        rotation = random.randint(0, 360)
        ast = objects.Asteroid(res.asteroid_img, x, y, batch = bat)
        ast.scale = scale
        ast.rotation = rotation
        ast.speed_x = random.randint(-3, 3)
        while ast.speed_x == 0:
            ast.speed_x = random.randint(-3,3)
        ast.speed_y = random.randint(-3, 5)
        while ast.speed_y == 0:
            ast.speed_y = random.randint(-3, 3)
        asteroids.append(ast)
    return asteroids

def distance(obj1, obj2):
    a = (obj1.x - obj2.x) ** 2
    b = (obj1.y - obj2.y) ** 2
    return math.sqrt(a + b)

def create_player_lives(sets, count, bat):
    lives = []
    for i in range(count):
        ship = pyglet.sprite.Sprite(res.ship_img, 1100 - (i * 20), 770, batch=bat)
        ship.rotation = -90
        ship.scale = 0.7
        lives.append(ship)

    return lives