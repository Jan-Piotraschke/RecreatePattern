import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.label import Label

from game import GameScreen
from menu import MenuScreen


class MyApp(App):

    def build(self):
        return MenuScreen()


if __name__ == '__main__':
    MyApp().run()