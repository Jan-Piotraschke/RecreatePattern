import os

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

# our .kv design file 
# Builder.load_file('design/game.kv')

down = os.path.join("img", "down.png")
normal = os.path.join("img", "up.png")

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)

        footer = BoxLayout(orientation="horizontal", size_hint_max_y=40)
        # footer.add_widget(Button(text="Restart", on_press=self.restart))
        footer.add_widget(Button(text="Back to menu", on_press=self.back))

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(footer)

        self.add_widget(layout)

    def back(self, btn):
        self.parent.transition.direction = "right"
        self.parent.current = "menu"