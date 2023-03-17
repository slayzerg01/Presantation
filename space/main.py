import pygame as pg
import random
import math

RES = WIDTH, HEIGHT = 1280, 720
NUM_STARS = 1000
ALPHA = 120

vec2, vec3 = pg.math.Vector2, pg.math.Vector3
CENTER = vec2(WIDTH // 2, HEIGHT // 2)
Z_DISTANCE = 30
logo = pg.image.load('logo.png')


class Star:
    def __init__(self, app):
        self.screen = app.screen
        self.pos3d = self.get_pos3d()

        self.vel = random.uniform(0.05, 0.25)

        self.screen_pos = vec2(0, 0)
        self.size = 10

    def get_pos3d(self, scale_pos=35):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.randrange(HEIGHT // scale_pos, HEIGHT) * scale_pos
        x = radius * math.sin(angle)
        y = radius * math.cos(angle)
        return vec3(x, y, Z_DISTANCE)

    def update(self):
        self.pos3d.z -= self.vel
        self.pos3d = self.get_pos3d() if self.pos3d.z < 1 else self.pos3d

        self.screen_pos = vec2(self.pos3d.x, self.pos3d.y) / self.pos3d.z + CENTER
        self.size = (Z_DISTANCE - self.pos3d.z) / (0.2 * self.pos3d.z) * 3

        self.pos3d.xy = self.pos3d.xy.rotate(0.2)

        mouse_pos = CENTER - vec2(pg.mouse.get_pos())
        self.screen_pos += mouse_pos

    def draw(self):
        log_transform = pg.transform.scale(logo, (self.size, self.size))
        self.screen.blit(log_transform, self.screen_pos)


class Starfield:
    def __init__(self, app):
        self.stars = [Star(app) for i in range(NUM_STARS)]

    def run(self):
        [star.update() for star in self.stars]
        self.stars.sort(key=lambda star: star.pos3d.z, reverse=True)
        [star.draw() for star in self.stars]


class App:
    def __init__(self):
        self.screen = pg.display.set_mode(RES)
        self.alpha_surface = pg.Surface(RES)
        self.alpha_surface.set_alpha(ALPHA)
        self.clock = pg.time.Clock()
        self.starfield = Starfield(self)

    def run(self):
        while True:
            self.screen.blit(self.alpha_surface, (0, 0))
            self.starfield.run()

            pg.display.flip()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            self.clock.tick(60)


if __name__ == '__main__':
    app = App()
    app.run()
