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

        self.light_properties_list: list = []
        for i in range(GAME_COLS * GAME_ROWS):
            light_properties = LightProperties(self.game.config[i], id=str(i), on_press=self.stimulusArea)
            self.light_properties_list.append(light_properties)  # store the properties for changing it later on
            self.add_widget(light_properties)  # give the light properties to the corresponding game tile


    def stimulusArea(self, light_selected):
        """ give a stimulus to the chosen area

        :param light_selected:
        :return:
        """
        position_ID = int(light_selected.id)  # defined in LightProperties

        stimulus_area_list: list = []
        stimulus_area_list.append(position_ID)
        # Todo: generalize this logic
        if position_ID > 4:
            stimulus_area_list.append(position_ID - 5)
        if position_ID < 20:
            stimulus_area_list.append(position_ID + 5)
        if position_ID % 5 > 0:
            stimulus_area_list.append(position_ID - 1)
        if position_ID % 5 < 4:
            stimulus_area_list.append(position_ID + 1)

        self.broker_order(stimulus_area_list)


    def broker_order(self, stimulus_area_list):
        """ this function implements the order from the broker to the logic of the game

        :param stimulus_area_list:
        :return:
        """
        for position_ID in stimulus_area_list:
            self.light_properties_list[position_ID].changeWavelength()


# the mathematical flipping logic and the initialization of a game
class Game:
    def __init__(self):
        self.config = []

    def generateRandomGame(self, game_tiles_number):
        return [random.randint(0, 1) for _ in range(game_tiles_number)]

    def load(self):
        game_tiles = GAME_COLS * GAME_ROWS
        x1 = [0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0]
        x2 = [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1]
        self.config = self.generateRandomGame(game_tiles)
        while dot(self.config, x1) % 2 or dot(self.config, x2) % 2:
            self.config = self.generateRandomGame(game_tiles)


class LightProperties(Button):
    # in this class we define the visualization logic at which time the light is off or on
    def __init__(self, waveLength, id, **kwargs):
        super(LightProperties, self).__init__(**kwargs)
        
        self.toggled = 0
        self.id = id
        self.initialize(waveLength)

    def initialize(self, waveLength):
        if waveLength == 1:
            self.toggled = 1
            self.background_down = lightOut
            self.background_normal = lightNormal
        else:
            self.toggled = 0
            self.background_down = lightNormal
            self.background_normal = lightOut

    # ! function is broken
    def changeWavelength(self):
        self.toggled = 0 if self.toggled else 1  # binary switch
        self.background_normal, self.background_down = self.background_down, self.background_normal   # binary switch