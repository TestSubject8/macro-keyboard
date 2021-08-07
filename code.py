# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board

import digitalio
import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

from adafruit_hid.consumer_control import ConsumerControl


kbd = Keyboard(usb_hid.devices)

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

button3 = digitalio.DigitalInOut(board.GP15) 
button3.switch_to_input(pull=digitalio.Pull.DOWN)

button2 = digitalio.DigitalInOut(board.GP14)
button2.switch_to_input(pull=digitalio.Pull.DOWN)

button1 = digitalio.DigitalInOut(board.GP13)
button1.switch_to_input(pull=digitalio.Pull.DOWN)

encoder = rotaryio.IncrementalEncoder(board.D17, board.D16)
last_position = None

# buttons = {digitalio.DigitalInOut(board.GP15): Keycode.F1,
#           digitalio.DigitalInOut(board.GP14): Keycode.F2 }

# buttons = [(button3, Keycode.ONE), (button2, Keycode.TWO), (button1, Keycode.THREE)]
# buttons = [(button3, Keycode.RIGHT_ARROW), (button2, Keycode.UP_ARROW), (button1, Keycode.LEFT_ARROW)]
buttons =   [   (button3, (Keycode.CONTROL, Keycode.WINDOWS, Keycode.RIGHT_ARROW)), 
                (button2, (Keycode.WINDOWS, Keycode.TAB)), 
                (button1, (Keycode.CONTROL, Keycode.WINDOWS, Keycode.LEFT_ARROW))
            ]

# button1 = digitalio.DigitalInOut(board.GP15)
# button1.switch_to_input(pull=digitalio.Pull.DOWN)

# search = digitalio.DigitalInOut(board.D5)
# search.direction = digitalio.Direction.INPUT
# search.pull = digitalio.Pull.DOWN

def display():
    pass

while True:
    for sc in buttons:
        if sc[0].value:
            print('key pressed', sc[1])
            led.value = True
            kbd.send(*sc[1])
            time.sleep(0.2)
        else:
            led.value = False
            kbd.release_all()
    
    position = encoder.position
    if last_position is None or position != last_position:
        print(position)
    last_position = position


    # press CTRL+K, which in a web browser will open the search dialog
    # elif search.value:
    #     kbd.send(Keycode.CONTROL, Keycode.K)
