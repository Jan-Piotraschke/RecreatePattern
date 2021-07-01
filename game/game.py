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

lightOut = os.path.join("img", "blue.png")
lightNormal = os.path.join("img", "red.png")


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)

        self.game = GameGrid(size_hint_min_y=620)

        # create the play ground for the game
        playGround = BoxLayout(orientation="vertical")
        playGround.add_widget(self.game)

        # create the navigation bar
        navigationBar = BoxLayout(orientation="horizontal", size_hint_max_y=40)
        # navigationBar.add_widget(Button(text="Restart", on_press=self.restart))
        navigationBar.add_widget(Button(text="Back to menu", on_press=self.back))

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(playGround)
        layout.add_widget(navigationBar)

        self.add_widget(layout)

    # go back to the menu
    def back(self, btn):
        self.parent.transition.direction = "right"
        self.parent.current = "menu"


# in this class we define the visualization logic at which time the light is off or on
class Light(Button):
    def __init__(self, waveLength, id, **kwargs):
        super(Light, self).__init__(**kwargs)
        
        self.toggled = 0
        self.id = id
        self.initialize(waveLength)

    def initialize(self, waveLength):
        if waveLength==1:
            self.toggled = 1
            self.background_down = lightOut
            self.background_normal = lightNormal
        else:
            self.toggled = 0
            self.background_down = lightNormal
            self.background_normal = lightOut

    # ! function is broken
    def flip(self):
        self.toggled = 0 if self.toggled else 1
        self.background_normal, self.background_down = self.background_down, self.background_normal


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

        # ! important to know: 'self.cols' is mandatory for 'GridLayout'
        self.cols = 5
        # the space between the fields
        self.spacing = 5

        self.game = Game()
        # self.manager = None
        # self.player_name = None
        # self.scheduled = None

        with self.canvas.before:
            Color(0.75, 0.75, 0.75, 0.75)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect)

        self.game.load()

        self.lightsValue = []
        for i in range(25):
            
            # overgive the value of the lights (on vs off) to the visualization logic class
            self.lightsValue.append(Light(self.game.config[i], id=str(i), on_press=self.toggle))
            self.add_widget(self.lightsValue[i])

    def update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def toggle(self, lights):

        positionID = int(lights.id)

        self.flip(positionID)
        self.game.ones += 1 if self.game.config[positionID] else -1

        if positionID > 4:      self.flip(positionID - 5)
        if positionID < 20:     self.flip(positionID + 5)
        if positionID % 5 > 0:  self.flip(positionID - 1)
        if positionID % 5 < 4:  self.flip(positionID + 1)

    def flip(self, positionID):

        self.lightsValue[positionID].flip()
        self.game.flip(positionID)
        self.game.ones += 1 if self.game.config[positionID] else -1
