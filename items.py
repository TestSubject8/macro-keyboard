import time
import microcontroller

class Item:
    def __init__(self, menu, disp_func, action_func):
        self.menu = menu
        self.menu.items.append(self)
        self.disp_func = disp_func
        self.action_func = action_func

    def disp(self):
        o = self.menu.oled
        o.fill(0)
        # Time / countdown
        _, _, _, hour, minute, second, _, _, _ = self.menu.rtc.datetime
        time_string = '%02d'%(hour) + ':' + '%02d'%(minute)
        # + ':' + '%02d'%(second)
        o.text(time_string, 0,0, None)

        # FPS / Temp
        o.text(str(self.menu.prev_round_trip)[:4]+'s', 53, 0, None)
        o.text(str(microcontroller.cpu.temperature)[:4] + ' C', 85,0, None)
        for i in range(0,10):
            o.pixel(51,i,1) 
            o.pixel(83,i,1) 

        # active label and custom display
        # self.oled.text(self.items[self.active].label, 38,10, None)

        self.disp_func(self, self.menu)
        o.show()

    def action(self):
        if self.menu.button3.value and time.monotonic()-self.last_pressed>0.2:
            self.menu.next()
            self.last_pressed = time.monotonic()
        self.action_func(self, self.menu)

    def mainloop(self):
        while True:
            stime = time.monotonic()
            self.action_func(self, self.menu)
            self.disp()
            self.menu.prev_round_trip = time.monotonic() - stime
        
