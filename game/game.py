from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from kivy.lang import Builder

# our .kv design file 
Builder.load_file('design/game.kv')


class GameScreen(GridLayout):

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
