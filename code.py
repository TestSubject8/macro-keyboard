import items
import menu
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keycode import Keycode

m = menu.Menu()

items.Keyboard(m, {'name': 'Windows', 'rot_fun': 'Vol', \
    'but1': 'L WS', 'but2': 'WIN Tab', 'but3': 'R WS'}, \
    { 0: [m.kbd.send, (Keycode.CONTROL, Keycode.WINDOWS, Keycode.LEFT_ARROW)], \
      1: [m.kbd.send, (Keycode.WINDOWS, Keycode.TAB)], \
      2: [m.kbd.send, (Keycode.CONTROL, Keycode.WINDOWS, Keycode.RIGHT_ARROW)], \
    }, \
)

items.Keyboard(m, {'name': 'OBS', 'rot_fun': 'BRI', \
    'but1': 'FACE', 'but2': 'Gaem', 'but3': 'Table'}, \
    { 0: [m.kbd.send, (Keycode.ALT, Keycode.ONE)], \
      1: [m.kbd.send, (Keycode.ALT, Keycode.TWO)], \
      2: [m.kbd.send, (Keycode.ALT, Keycode.THREE)], \
    }, \
)

items.Keyboard(m, {'name': 'Media', 'rot_fun': 'BRI', \
    'but1': 'Play', 'but2': 'Prev', 'but3': 'Next'}, \
    { 0: [m.cc.send, (ConsumerControlCode.PLAY_PAUSE, )], \
      1: [m.cc.send, (ConsumerControlCode.SCAN_PREVIOUS_TRACK, )], \
      2: [m.cc.send, (ConsumerControlCode.SCAN_NEXT_TRACK, )], \
    }, \
)

m.mainloop()