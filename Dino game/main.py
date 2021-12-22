from kivy.config import Config

Config.set('graphics', 'resizable', True)

from kivy.core.window import Window

Window.size = (1170, 540)
Window.top = 150
Window.left = 100

from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivy.clock import Clock
from random import randint

# скорость движения земли и кактусов
GAME_SPEED = 4
ACCELERATION_OF_GRAVITY = 0.5
FALL_SPEED = 0


class Cactus(Widget):
    def move(self):
        self.pos = self.pos[0] - GAME_SPEED, self.pos[1]


class Dino(Widget):

    def move(self):
        global FALL_SPEED
        self.pos = self.pos[0], self.pos[1] + FALL_SPEED
        FALL_SPEED -= ACCELERATION_OF_GRAVITY
        if self.pos[1] <= 20:
            FALL_SPEED = 0
            self.pos = 50, 20


class Terra(Widget):
    def move(self):
        self.pos = self.pos[0] - GAME_SPEED, self.pos[1]


class MainScreen(Widget):
    def update(self, *args):
        global GAME_SPEED

        self.terra.move()
        self.cactus1.move()
        self.dino.move()

        # перемещение земли на исходную, когда правый край равен ширине окна
        if abs(self.terra.pos[0]) + Window.size[0] >= self.terra.size[0]:
            self.terra.pos = 0, 0

        if self.cactus1.pos[0] + self.cactus1.size[0] <= 0:
            self.cactus1.pos = self.size[0] + randint(100, 400), 20

        dino_left = self.dino.pos[0] + self.dino.size[0] - 10
        dino_bottom = self.dino.pos[1]

        if dino_left in [x for x in range(self.cactus1.pos[0], self.cactus1.pos[0] + self.cactus1.size[0])] and \
                dino_bottom in [x for x in range(self.cactus1.pos[1], self.cactus1.pos[1] + self.cactus1.size[1])]:
            GAME_SPEED = 0

    def on_touch_down(self, touch):
        global FALL_SPEED
        FALL_SPEED = 15


class MainApp(MDApp):
    def build(self):
        game = MainScreen()
        game.cactus1.pos[0] = -50
        game.dino.pos = 50, 20
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    MainApp().run()
