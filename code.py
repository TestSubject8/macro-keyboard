import menu, items

from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode

m = menu.Menu()

def scroll(kbd, _, chg):
	if chg < 0:
		for i in range(-chg):
			kbd.send(Keycode.UP_ARROW)
	elif chg > 0:
		for i in range(chg):
			kbd.send(Keycode.DOWN_ARROW)

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


items.Keyboard(m, 'VOL', vol)
items.Keyboard(m, 'BRI', bright)
items.Keyboard(m, 'SCR', scroll)


m.mainloop()
