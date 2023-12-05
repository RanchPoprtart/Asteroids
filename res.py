import pyglet


pyglet.resource.path = ["./resources"]
pyglet.resource.reindex()

ship_img = pyglet.resource.image("Ship2.png", rotate=90)
asteroid_img = pyglet.resource.image("asteroid-large-1.png")
bullet_img = pyglet.resource.image("projectile.png")
fire_img = pyglet.resource.image("fire.png", rotate=90)
explosion_img = pyglet.resource.image("explosion.png")
explosion_seq = pyglet.image.ImageGrid(explosion_img, 1, 8)
boom = pyglet.resource.media("Bruh.wav",False)
background = pyglet.resource.image("bg_02_h.png")

def center_img(img):
    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2


center_img(ship_img)
center_img(asteroid_img)
center_img(bullet_img)

fire_img.anchor_x = fire_img.width * 1.5
fire_img.anchor_y = fire_img.height // 2

