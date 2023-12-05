import pyglet
import objects
import res
import random
import util

sets = {
    "num-asts": 4,
    "num-lives": 3,
    "time_new_asts": 12,
    "num_new_asts": 3,
    "rotate_speed": 2,
    "accelerate": 1
}



class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.score = 0
        self.batch = pyglet.graphics.Batch()
        self.player = objects.Player(sets, res.ship_img, self.width // 2, self.height // 2, batch=self.batch)
        self.player.rotation = -90
        self.asteroids = util.create_asteroids(sets["num-asts"], self.batch)
        self.game_objects = [self.player] +  self.asteroids
        self.push_handlers(self.player)
        self.push_handlers(self.player.key_handler)
        self.key_handler = pyglet.window.key.KeyStateHandler()
        self.frame = 0
        self.player_lives = util.create_player_lives(sets["num-lives"], 3, self.batch)
        self.done = False
        self.play_again = pyglet.text.Label("Game Over! Play Again?", "Arial", 48,
                                            x=self.width // 2,
                                            y = self.height // 2,
                                            anchor_x ="center",)
        self.score_label = pyglet.text.Label("Score: 0", "Arial", 16,
                                             x=20, y=self.height - 30, batch=self.batch)
        self.score = 0




    def on_draw(self):
        self.clear()
        res.background.blit(0, 0)
        self.batch.draw()
        if self.player.is_exploding:
            res.explosion_seq[self.frame].blit(self.player.x, self.player.y)
        if self.done:
            self.play_again.draw()

    def on_key_press(self, symbol, modifiers):
        if self.done:
            if symbol == pyglet.window.key.Y:
                self.asteroids = util.create_asteroids(5, self.batch)
                self.game_objects = [self.player] + self.asteroids
                self.player.reset()
                self.player_lives = util.create_player_lives(3, self.batch)
                self.done = False
                self.score = 0
            elif symbol == pyglet.window.key.N:
                pyglet.app.exit()

def explode_frame(dt):
    if win.frame == 7:
        pyglet.clock.unschedule(explode_frame)
        if len(win.player_lives) > 0:
            win.player.reset()
            del win.player_lives[-1]
        else:
            win.done = True
    else:
        win.frame += 1

def explode():
    win.player.dead = False
    win.player.is_exploding = True
    win.player.visible = False
    win.player.engine.visible = False
    pyglet.clock.schedule_interval(explode_frame, .2)
    win.frame = 0
    player = pyglet.media.Player()
    player.queue(res.boom)
    player.play()


def update(dt):
    for obj in win.game_objects:
        obj.update(dt)
    for i in range(len(win.game_objects)):
        for j in range(i + 1, len(win.game_objects)):
            if  win.game_objects[i].check_for_collision(win.game_objects[j]):
                win.game_objects[i].handle_collision()
                win.game_objects[j].handle_collision()

    new_list = []
    for obj in win.game_objects:
        new_list += obj.new_objects
        obj.new_objects  = []
        win.score += obj.score
        obj.score = 0



    if win.player.dead:
        explode()

    for to_remove in [obj for obj in win.game_objects if obj.dead]:
        win.game_objects.remove(to_remove)
        to_remove.delete()

    win.game_objects += new_list
    win.score_label.text = "score: {}".format(win.score)


def add_more(dt):
    if len(win.game_objects) < 25:
        win.game_objects += util.create_asteroids(3, win.batch, pos=win.player.position)
win = GameWindow(1200, 800, "Asteroids")


pyglet.clock.schedule_interval(update, 1.0 / 60)
pyglet.clock.schedule_interval(sets["num_new_asts"], sets["time_new_asts"])


if __name__ ==  "__main__":
    pyglet.app.run()