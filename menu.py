# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import rotaryio
import digitalio
import usb_hid

import microcontroller

from adafruit_hid.keyboard import Keyboard

from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

import busio as io
import adafruit_ssd1306 as adisp

class Menu:
    items = []

    def __init__(self):
        self.device_setup()
        self.pin_setup()

        self.buttons = (self.button1, self.button2, self.button3, self.button_rot)
        self.active = 0

        self.prev_round_trip = 0
        
        self.last_position = 0
        self.last_pressed = 0

    def next(self):
        self.active += 1
        self.active %= len(self.items)

    def device_setup(self):
        self.cc = ConsumerControl(usb_hid.devices)
        self.kbd = Keyboard(usb_hid.devices)
        self.i2c = io.I2C(board.GP5, board.GP4)
        self.oled = adisp.SSD1306_I2C(128, 32, self.i2c)

        self.encoder = rotaryio.IncrementalEncoder(board.GP16, board.GP17)
    # oled.setRotation(2)

    def pin_setup(self):
        self.led = digitalio.DigitalInOut(board.LED)
        self.led.direction = digitalio.Direction.OUTPUT


        self.button1 = digitalio.DigitalInOut(board.GP13)
        self.button1.switch_to_input(pull=digitalio.Pull.DOWN)

        self.button2 = digitalio.DigitalInOut(board.GP14)
        self.button2.switch_to_input(pull=digitalio.Pull.DOWN)

        self.button3 = digitalio.DigitalInOut(board.GP15) 
        self.button3.switch_to_input(pull=digitalio.Pull.DOWN)


        self.button_rot = digitalio.DigitalInOut(board.GP12) 
        self.button_rot.switch_to_input(pull=digitalio.Pull.UP)

    def show(self):
        self.oled.fill(0)
        # self.items[active].show()
        # self.grid()

        # Time / countdown
        _, _, _, hour, minute, _, _, _, _ = time.localtime()
        time_string = '%02d'%(hour) + ':' + '%02d'%(minute)
        self.oled.text(time_string, 0,0, None)

        # FPS / Temp
        self.oled.text(str(self.prev_round_trip)[:4]+'s', 53, 13, None)
        self.oled.text(str(microcontroller.cpu.temperature)[:4] + ' C', 85,13, None)
        for i in range(12,21):
            self.oled.pixel(83,i,1) 
            self.oled.pixel(51,i,1) 

        # menu item labels
        labels = self.items[self.active].labels
        # self.oled.text(labels[0], 80,12, None)
        self.oled.text(labels['but1'], 0,24, None)
        self.oled.text(labels['but2'], 40,24, None)
        self.oled.text(labels['but3'], 95,24, None)

        # handle individual spots on teh screen here, source only the text from the item obj
        self.oled.show()
    
    def grid(self):
        for i in range(0,128,10):
            for j in range(0,32,10):
                self.oled.pixel(i,j,1)
        # lines horizontal
        # for i in range(128):
        #     self.oled.pixel(i, 15, 1)
        #     self.oled.pixel(i, 25, 1)
        
        # # lines vertical
        # for i in range(32):
        #     self.oled.pixel(50, i, 1)
        #     self.oled.pixel(100, i, 1)

        # self.oled.text('Sameples', 0,0, None)
        # self.oled.text('Sameples', 10,10, None)

    
    def handle_rotation(self):
        # position = self.encoder.position
        chg = self.encoder.position - self.last_position
        stime = time.monotonic()
        # if position < self.last_position:
        if chg < 0:
            for i in range(-chg):
                self.decrement()
        # elif position > self.last_position:
        elif chg > 0:
            for i in range(chg):
                self.increment()
        self.last_position += chg
        
    def handle_buttons(self):
        for b in range(len(self.buttons)-1):
            if self.buttons[b].value:
                # print('key pressed', sc[1])
                self.led.value = True
                self.items[self.active].button_press(b)  # debounce handled in button - allows for long press / modifier functionality
                self.led.value = False
            else:
                pass
        if not self.button_rot.value:
            # self.led.value = True # pointless - it just blips out instantly
            self.last_pressed = time.monotonic()
            while not self.button_rot.value: # for a click to work, during the hold-down, keep the rotation going
                self.handle_rotation()
            if time.monotonic()-self.last_pressed < 0.3: # finally click if the release was within 0.3s 
                self.next()
            # self.led.value = False

    def increment(self):
        if self.button_rot.value:   # button_rot is wired such that is_pressed != value
            self.cc.send(ConsumerControlCode.VOLUME_INCREMENT)
        else:
            self.cc.send(ConsumerControlCode.BRIGHTNESS_INCREMENT)


    def decrement(self):
        if self.button_rot.value:
            self.cc.send(ConsumerControlCode.VOLUME_DECREMENT)
        else:
            self.cc.send(ConsumerControlCode.BRIGHTNESS_DECREMENT)


    def mainloop(self):
        while True:
            start_time = time.monotonic()

            self.show()

            self.handle_buttons()
            self.handle_rotation()


            # All display items between these 
            # show_labels(menu[2])
            
            # grid()

            # if not button_rot.value:
            #     handle_menu_selector()

            # all display items must be between theseP
            # oled.show()

            

            # time.sleep(0.2)

            self.prev_round_trip = time.monotonic() - start_time
            # press CTRL+K, which in a web browser will open the search dialog
            # elif search.value:
            #     kbd.send(Keycode.CONTROL, Keycode.K)
        
