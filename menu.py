# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import rotaryio
import digitalio
import usb_hid

import microcontroller

from adafruit_hid.keycode import Keycode
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

        self.buttons = (self.button1, self.button2, self.button3, )

        self.prev_round_trip = 0

        self.last_position = 0
        self.last_pressed = 0

        self.active = 0
        self.index = 0

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

    def next(self):
        self.index += 1
        self.index %= len(self.items)

    def set_menu(self, b):
        index = self.index + b
        index %= len(self.items)
        self.active = index

    def show(self):
        self.oled.fill(0)
        # self.items[active].show()
        # self.grid()

        # Time / countdown
        _, _, _, hour, minute, _, _, _, _ = time.localtime()
        time_string = '%02d'%(hour) + ':' + '%02d'%(minute)
        self.oled.text(time_string, 0,0, None)

        # FPS / Temp
        self.oled.text(str(self.prev_round_trip)[:4]+'s', 53, 0, None)
        self.oled.text(str(microcontroller.cpu.temperature)[:4] + ' C', 85,0, None)
        for i in range(0,10):
            self.oled.pixel(51,i,1) 
            self.oled.pixel(83,i,1) 

        # active label and custom display
        # self.oled.text(self.items[self.active].label, 38,10, None)
        self.items[self.active].show(self.oled)

        for i in range(3):
            ind = self.index+i 
            ind %= len(self.items)
            if ind == self.active:
                j = -4
                for k in range(15):
                    self.oled.pixel(i*40+k, 30, 1)
            else:
                j = 0
            self.oled.text(self.items[ind].label, i*40,24+j, None)

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
        if chg:
            # self.kbd.send(Keycode.UP_ARROW)
            self.items[self.active].rot_func(chg)
            self.last_position += chg
        
    def handle_buttons(self):
        for b in range(len(self.buttons)):
            if self.buttons[b].value:
                # print('key pressed', sc[1])
                self.led.value = True
                self.set_menu(b)
                  # debounce handled in button - allows for long press / modifier functionality
                self.led.value = False
            else:
                pass
        if not self.button_rot.value:
            self.next()
            


    def mainloop(self):
        while True:
            start_time = time.monotonic()

            self.handle_buttons()
            self.handle_rotation()

            self.show()

            self.prev_round_trip = time.monotonic() - start_time
