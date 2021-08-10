import items
import menu
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keycode import Keycode

m = menu.Menu()

items.Keyboard(m, {'name': 'Windows', 'rot_fun': 'Vol', \
    'but1': 'L WS', 'but2': 'WIN Tab', 'but3': 'R WS'}, \
    { 0: (Keycode.CONTROL, Keycode.WINDOWS, Keycode.LEFT_ARROW), \
      1: (Keycode.WINDOWS, Keycode.TAB), \
      2: (Keycode.CONTROL, Keycode.WINDOWS, Keycode.RIGHT_ARROW), \
    }, \
    (ConsumerControlCode.VOLUME_INCREMENT, ConsumerControlCode.VOLUME_DECREMENT) \
)

items.Keyboard(m, {'name': 'OBS', 'rot_fun': 'BRI', \
    'but1': 'FACE', 'but2': 'Gaemm', 'but3': 'Table'}, \
    { 0: (Keycode.ALT, Keycode.ONE), \
      1: (Keycode.ALT, Keycode.TWO), \
      2: (Keycode.ALT, Keycode.THREE) \
    }, \
    (ConsumerControlCode.BRIGHTNESS_INCREMENT, ConsumerControlCode.BRIGHTNESS_DECREMENT) \
)

m.mainloop()