import os
import operator
import random

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout

from kivy.lang import Builder

# our .kv design file 
# Builder.load_file('design/game.kv')

LightOut = os.path.join("img", "down.png")
LightNormal = os.path.join("img", "up.png")


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)

        self.game = GameGrid(size_hint_min_y=620)

        box = BoxLayout(orientation="vertical")
        box.add_widget(self.game)

        footer = BoxLayout(orientation="horizontal", size_hint_max_y=40)
        # footer.add_widget(Button(text="Restart", on_press=self.restart))
        footer.add_widget(Button(text="Back to menu", on_press=self.back))

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(box)

        layout.add_widget(footer)

        self.add_widget(layout)

    def back(self, btn):
        self.parent.transition.direction = "right"
        self.parent.current = "menu"


# in this class we define the visualization logic at which time the light is off or on
class LightGradient(Button):
    def __init__(self, up, id, **kwargs):
        super(LightGradient, self).__init__(**kwargs)
        
        self.toggled = 0
        self.always_release = True
        self.initialize(up)

    def initialize(self, up):
        if up:
            self.toggled = 1
            self.background_down = LightOut
            self.background_normal = LightNormal
        else:
            self.toggled = 0
            self.background_down = LightNormal
            self.background_normal = LightOut

    def flip(self):
        self.toggled = 0 if self.toggled else 1
        self.background_normal, self.background_down = self.background_down, self.background_normal

    def restore(self):
        if self.toggled:
            self.background_normal = LightNormal
        else:
            self.background_normal = LightOut


def dot(x1, x2):
    return sum(map(operator.mul, x1, x2))

# the mathematical flipping logic and the initialization of a game
class Game:
    def __init__(self):
        self.config = []
        self.ones = 0

    def load(self):
        x1 = [0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0]
        x2 = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1]

        self.config = [random.randint(0, 1) for _ in range(25)]
        while dot(self.config, x1) % 2 or dot(self.config, x2) % 2:
            self.config = [random.randint(0, 1) for _ in range(25)]

        self.ones = sum(self.config)

    # NOTE: the flipping logic -> has to be more complex for an advanced 'Light On'!
    def flip(self, position):
        self.config[position] = 0 if self.config[position] else 1

class GameGrid(GridLayout):
    def __init__(self, **kwargs):
        super().__init__()
        self.cols = 5
        self.spacing = 5

        self.game = Game()
        # self.moves = Moves()
        # self.manager = None
        # self.player_name = None
        # self.scheduled = None
        # self.toggled_last = None

        with self.canvas.before:
            Color(0.75, 0.75, 0.75, 0.75)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        # self.bind(pos=self.update_rect, size=self.update_rect)

        self.game.load()

        self.lights = []
        for i in range(25):
            
            # overgive the value of the lights (on vs off) to the visualization logic class
            self.lights.append(LightGradient(self.game.config[i], id=str(i)))#, on_press=self.toggle))
            self.add_widget(self.lights[i])