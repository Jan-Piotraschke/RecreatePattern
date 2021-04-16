import os

import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen


from menu import MenuScreen
from game import GameScreen



class MyApp(App):

    def build(self):
        # add a logo 
        self.title = "Lights On"

        try:
            self.icon = os.path.join("img", "icon.png")
        except:
            pass

        # Create the manager to manage the multiple screens of the app
        sm = ScreenManager()

        # register the screens
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(GameScreen(name='game'))

        return sm


if __name__ == '__main__':
    MyApp().run()