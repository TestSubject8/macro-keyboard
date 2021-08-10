import time

class Item:
    def __init__(self, menu, labels):
        # obs_labels = [('OBS', 0,0, None), ('Brightness->', 45, 0, None), ('Gaem', 0, 25, None), ('influencer', 40, 25, None), ('Table', 90, 25, None)]

        self.menu = menu

        # self.labels = 
        self.labels = labels
        self.menu.items.append(self)

        # self.menu.mainloop()

    def button_press(self, button):
        pass

    # def show(self):
    #     pass
        
class Keyboard(Item):
    def __init__(self, menu, labels, button_funcs, rot_change):
        Item.__init__(self, menu, labels)
        self.menu = menu
        self.button_funcs = button_funcs
        self.rot_change = rot_change
    
    def increment(self):
        self.menu.cc.send(self.rot_change[0])
    
    def decrement(self):
        self.menu.cc.send(self.rot_change[1])

    def button_press(self, button):
        self.menu.kbd.send(*self.button_funcs[button])
        time.sleep(0.1)
 