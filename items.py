import time

class Keyboard:
    def __init__(self, menu, label, handler):
        self.menu = menu
        self.handler = handler
        self.label = label  
        self.indicator = 0
        self.menu.items.append(self)

    def rot_func(self, chg):
        self.handler(self.menu.kbd, self.menu.cc, chg)
        self.indicator = chg

    def show(self, oled):
        if self.indicator < 0:
            oled.text('<-', 50,10, None)
        elif self.indicator > 0:
            oled.text('->', 50,10, None)
        self.indicator = 0
