import pyglet
from pyglet.window import key
import res
import math
import util


Width = 1200
Height = 800
class Game_object(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dead = False
        self.speed_x = 0
        self.speed_y = 0
        self.new_objects = []
        self.score = 0

    def update(self, dt):
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x <= 0:
            self.x = Width
        elif self.x >= Width:
            self.x = 0
        if self.y <= 0:
            self.y = Height
        elif self.y >= Height:
            self.y = 0

    def check_for_collision(self, obj):
        if self.__class__ == obj.__class__:
            return False
        actual_distance = util.distance(self, obj)
        collision_distance = self.width // 2 + obj.width // 2
        return actual_distance < collision_distance

    def handle_collision(self):
        self.dead = True



class Player(Game_object):
    def __init__(self, sets, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.engine = pyglet.sprite.Sprite(res.fire_img, 0, 0, batch=self.batch)
        self.engine_visible = False
        self.keys = {"left":False , "right":False, "UP": False}
        self.key_handler = key.KeyStateHandler()
        self.velocity = 0
        self.is_exploding = False
        self.rotate_speed = sets["rotate_speed"]
        self.accelerate = sets['accelerate']

    def on_key_press(self, symbol, mod):
        if symbol == key.LEFT:
            self.keys["left"] = True
        if symbol == key.RIGHT:
            self.keys["right"] = True
        if symbol == key.UP:
            self.keys["UP"] = True
        if symbol == key.SPACE and not self.is_exploding:
            self.fire()

    def on_key_release(self, symbol, mod):
        if symbol == key.LEFT:
            self.keys["left"] = False
        if symbol == key.RIGHT:
            self.keys["right"] = False
        if symbol == key.UP:
            self.keys["UP"] = False




    def update(self, dt):
        if self.is_exploding:
            self.speed_y = 0
            self.speed_x = 0
            self.velocity = 0
            return

        if self.keys["left"]:
            self.rotation -= self.rotate_speed
        if self.keys["right"]:
            self.rotation += self.rotate_speed
        if self.keys["UP"]:

            self.set_speed(self.velocity + 1, dt)
            if self.velocity > 0:
                self.engine_visible = True
        else:
            self.engine_visible = False
            if self.velocity > 0:
                self.set_speed(self.velocity - 1, dt)


        self.engine.visible = self.engine_visible
        self.engine.x = self.x
        self.engine.y = self.y
        self.engine.rotation = self.rotation
        super().update(dt)

    def set_speed(self, speed, dt):
        self.velocity = speed
        radians = -math.radians(self.rotation)
        self.speed_x = math.cos(radians) * speed * dt * 15.0
        self.speed_y = math.sin(radians) * speed * dt * 15.0

    def check_for_collision(self, obj):
        if self.is_exploding:
            return False
        return super().check_for_collision(obj)

    def handle_collision(self):
        if not self.is_exploding:
            super().handle_collision()
        self.engine_visible = False
        self.engine.visible = False

    def fire(self):
        radians = -math.radians(self.rotation)
        bullet_x = self.x + math.cos(radians) * self.image.width
        bullet_y = self.y + math.sin(radians) * self.image.height
        bullet = Bullet(res.bullet_img, bullet_x, bullet_y, batch=self.batch)
        bullet.rotation = self.rotation
        bullet.speed_x = self.speed_x + math.cos(radians) * bullet.base_speed
        bullet.speed_y = self.speed_y + math.sin(radians) * bullet.base_speed
        self.new_objects.append(bullet)

    def reset(self):
        self.is_exploding = False
        self.y = Height // 2
        self.x = Width // 2
        self.rotation = -90
        self.visible = True


class Bullet(Game_object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pyglet.clock.schedule_once(self.self_destruct, 0.5)
        self.base_speed = 20

    def self_destruct(self,dt):
        self.dead = True




class Asteroid(Game_object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.new_object = None

    def check_for_collision(self, obj):
        if  obj.__class__.__name__== "Bullet":
            return super().check_for_collision(obj)
        return False


    def handle_collision(self):
        super().handle_collision()
        if self.scale >= .7:
            self.new_objects = util.create_asteroids(5, self.batch, self.x, self.y, 5)
            self.score += 5
        elif self.scale >= .5:
            self.new_object =  util.create_asteroids( 5, self.batch, self.x, self.y, 4)
            self.score += 10
        else:
            self.score += 15