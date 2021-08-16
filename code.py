import menu, items

from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode

m = menu.Menu()


def vol(_, cc, chg):
	print('called')
	if chg < 0:
		for i in range(-chg):
			cc.send(ConsumerControlCode.VOLUME_DECREMENT)
			print('sent')
	elif chg > 0:
		for i in range(chg):
			cc.send(ConsumerControlCode.VOLUME_INCREMENT)

def bright(_, cc, chg):
	if chg < 0:
		for i in range(-chg):
			cc.send(ConsumerControlCode.BRIGHTNESS_DECREMENT)
	elif chg > 0:
		for i in range(chg):
			cc.send(ConsumerControlCode.BRIGHTNESS_INCREMENT)

# SCROLL Menu Item

def scroll_action(menu):
	chg = menu.encoder.position - menu.last_position
	if chg < 0:
		if menu.button_rot.value:
			code = Keycode.UP_ARROW
		else:
			code = Keycode.LEFT_ARROW
		for i in range(-chg):
			menu.kbd.send(code)

	elif chg > 0:
		if menu.button_rot.value:
			code = Keycode.DOWN_ARROW
		else:
			code = Keycode.RIGHT_ARROW
		for i in range(chg):
			menu.kbd.send(code)
	menu.last_position += chg

def scroll_disp(menu):
	menu.oled.text('Next time then', 20,20, None)

items.Item(m, scroll_disp, scroll_action)

# ensure screensaver is added first, make some timer to go back to index = 0
# items.Keyboard(m, 'VOL', vol)
# items.Keyboard(m, 'BRI', bright)
# items.Keyboard(m, 'SCR', scroll)
m.next()
