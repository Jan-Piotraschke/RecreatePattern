from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class GameScreen(GridLayout):

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
