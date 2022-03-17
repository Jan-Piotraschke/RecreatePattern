# TODO: 3 verschiedene Farben der Kackeln


import os
import operator
import random
import numpy as np

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button, ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty
from kivy.lang import Builder

# our .kv design file 
Builder.load_file('design/game.kv')


GAME_COLS: int = 5
GAME_ROWS: int = 5


def dot(x1, x2):
    return sum(map(operator.mul, x1, x2))


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)

        self.game = GameGridBroker(size_hint_min_y=620)

        # create the play ground for the game
        playGround = BoxLayout(orientation="vertical")
        playGround.add_widget(self.game)

        # TODO: the pattern you have to recreate
        # goalLayout = BoxLayout(orientation="vertical")

        # create the navigation bar
        navigationBar = BoxLayout(orientation="horizontal", size_hint_max_y=40)
        navigationBar.add_widget(Button(text="Back to menu", on_press=self.back))

        # TODO: navigationBar.add_widget(Button(text="Restart", on_press=self.restart))

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(playGround)
        # layout.add_widget(goalLayout)
        layout.add_widget(navigationBar)

        self.add_widget(layout)

    # go back to the menu
    def back(self, btn):
        self.parent.transition.direction = "right"
        self.parent.current = "menu"


class GameGridBroker(GridLayout):
    """ this class coordinates the user input and the corresponding Game output """
    def __init__(self, **kwargs):
        super().__init__()

        self.cols = GAME_COLS  # ! important to know: 'self.cols' is mandatory for 'GridLayout'
        self.spacing = 5  # the space between the fields

        self.game = Game()  # inject the Game into the Grid
        self.game.load()  # start the Game
        self.neighbors = self.find_neighbours(arr=np.arange(GAME_COLS*GAME_ROWS).reshape((GAME_ROWS, GAME_COLS)))

        self.light_properties_list: list = []
        for i in range(GAME_COLS * GAME_ROWS):
            light_properties = LightProperties(self.game.config[i], id=str(i), on_press=self.stimulus_area)
            self.light_properties_list.append(light_properties)  # store the properties for changing it later on
            self.add_widget(light_properties)  # give the light properties to the corresponding game tile

    @staticmethod
    def find_neighbours(arr):

        neighbors = {}

        for i in range(len(arr)):
            for j, value in enumerate(arr[i]):

                if i == 0 or i == len(arr) - 1 or j == 0 or j == len(arr[i]) - 1:
                    # corners
                    new_neighbors = []
                    if i != 0:
                        new_neighbors.append(arr[i - 1][j])  # top neighbor
                    if j != len(arr[i]) - 1:
                        new_neighbors.append(arr[i][j + 1])  # right neighbor
                    if i != len(arr) - 1:
                        new_neighbors.append(arr[i + 1][j])  # bottom neighbor
                    if j != 0:
                        new_neighbors.append(arr[i][j - 1])  # left neighbor

                else:
                    # add neighbors
                    new_neighbors = [
                        arr[i - 1][j],  # top neighbor
                        arr[i][j + 1],  # right neighbor
                        arr[i + 1][j],  # bottom neighbor
                        arr[i][j - 1]  # left neighbor
                    ]

                neighbors[value] = new_neighbors

        return neighbors

    def stimulus_area(self, light_selected):
        """ give a stimulus to the chosen area

        :param light_selected:
        :return:
        """
        position_ID = int(light_selected.id)  # defined in LightProperties

        stimulus_area_list: list = []
        stimulus_area_list.append(position_ID)
        stimulus_area_list.extend(self.neighbors[position_ID])  # append the neighbors

        self.broker_order(stimulus_area_list)

    def broker_order(self, stimulus_area_list):
        """ this function implements the order from the broker to the logic of the game

        :param stimulus_area_list:
        :return:
        """
        for position_ID in stimulus_area_list:
            self.light_properties_list[position_ID].change_wavelength()


# the mathematical flipping logic and the initialization of a game
class Game:
    def __init__(self):
        self.config = []

    @staticmethod
    def generate_random_game(game_tiles_number):
        return [random.randint(0, 1) for _ in range(game_tiles_number)]

    def load(self):
        game_tiles = GAME_COLS * GAME_ROWS
        x1 = [0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0]
        x2 = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1]
        self.config = self.generate_random_game(game_tiles)
        while dot(self.config, x1) % 2 or dot(self.config, x2) % 2:
            self.config = self.generate_random_game(game_tiles)


# NOTE: General rule for programming in Kivy:
# if you want to change code depending on a property of a Widget/Object use a Kivy Property (like NumericProperty)
class LightProperties(ButtonBehavior, Label):
    # Easily manipulate widgets defined in the Kv language
    r = NumericProperty(0)  # make the property of this object variable

    # in this class we define the visualization logic at which time the light is off or on
    def __init__(self, wavelength, id, **kwargs):
        super(LightProperties, self).__init__(**kwargs)
        self.toggled = 0
        self.id = id
        self.initialize(wavelength)

    def initialize(self, wavelength):
        if wavelength == 1:
            self.toggled = 1
            self.r = 0
        else:
            self.toggled = 0
            self.r = 1

    # switch the light
    def change_wavelength(self):
        if self.r == 1.0:
            self.r -= 1
        else:
            self.r += 1
