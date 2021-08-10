import time

class Item:
    def __init__(self, menu, labels):
        self.menu = menu

        self.labels = labels
        self.menu.items.append(self)

    def button_press(self, button):
        pass

class Keyboard(Item):
    def __init__(self, menu, labels, button_funcs):
        Item.__init__(self, menu, labels)
        self.menu = menu
        self.button_funcs = button_funcs
    
    def button_press(self, button):
        if button == 3:
            self.menu.next()
        fn, args = self.button_funcs[button]
        fn(*args)
        time.sleep(0.1)
