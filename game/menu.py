from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

# our .kv design file 
Builder.load_file('design/menu.kv')

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)

    # def new_game(self, btn):
    def new_game(self):
        self.parent.transition.direction = "left"
        self.parent.current = "game"