import time
import board
import digitalio
import random
import microcontroller

import busio as io
import adafruit_ssd1306 as adisp

i2c = io.I2C(board.GP5, board.GP4)
oled = adisp.SSD1306_I2C(128, 32, i2c)

oled.fill(0)
oled.show()

button1 = digitalio.DigitalInOut(board.GP13)
button1.switch_to_input(pull=digitalio.Pull.DOWN)

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

dot_size = 3

xmax = 125 - dot_size
ymax = 30 - dot_size

living = []
cc = {}

# crowd_count = {}

# random select of pixels to start the game
# for i in range(100):
# 	temp = microcontroller.cpu.temperature
# 	end = temp * 10000
# 	# a = int(end)
# 	a = int(end) % 10
# 	end /= 10
# 	b = int(end) % 10
# 	end /= 10
# 	c = int(end) % 10
# 	end /= 10
# 	d = int(end) % 10

def draw_dot(x,y,status):
	for i in range(1,dot_size-1):
		for j in range(1,dot_size-1):
	# for i in range(0,dot_size):
	# 	for j in range(0,dot_size):
			xx = x + i 
			xx %= xmax
			yy = y+j
			yy %= ymax
			oled.pixel(xx,yy,status)

def show_living():
	oled.fill(0)
	for l in living:
		draw_dot(l[0],l[1],1)
	oled.show()

def reset_living(count=40):
	living.clear()
	led.value = True
	for i in range(count):
		x = random.randrange(0,xmax,dot_size)
		y = random.randrange(0,ymax,dot_size)
		if (x,y) not in living:
			living.append((x, y))
	time.sleep(0.5)
	led.value = False

def add_cc(x,y):
	if (x,y) in cc:
		cc[(x,y)] += 1
	else:
		cc[(x,y)] = 1

def check_surroundings(x,y):
	for dx in [-dot_size,0,dot_size]:
		for dy in [-dot_size,0,dot_size]:
			if dx == 0 and dy == 0: continue
			cx = x+dx
			cx %= xmax
			cy = y+dy
			cy %= ymax

			if (cx,cy) in living:
				add_cc(x,y)
			else:
				add_cc(cx,cy)

			# if (cy,cx) in living:
			# 	add_cc(y,x)
			# else:
			# 	add_cc(cy,cx)

	# for d in [-dot_size,0,dot_size]:
			# dx = dy = d

def run(init=None):
	if init:
		living.extend(init)
	else:
		reset_living(70)

	show_living()
	print(living)


	while living:
		# while not button1.value: pass
		if button1.value: reset_living(70)
		stime = time.monotonic()

		cc.clear()

		for x,y in living:
			cc[(x,y)] = 0
			check_surroundings(x,y)

		print(cc)
		# Conway rules: 
		for c in cc:
			if cc[c] < 2 or cc[c] > 3:
				if c in living:
					living.remove(c)
					# print(c, 'died')
			elif cc[c] == 3:
				if c not in living:
					living.append(c)
					# print(c,'born')
		show_living()
		
		# print(time.monotonic() - stime)
		
		time.sleep(0.25)


while True:
	# run([(10,15), (15,15), (10,10)])
	run()
	# run([(5,10),(10,15),(15,5),(15,10),(15,15)]) # glider 1



# print(oled.value(1,1))

# for i in range(xmax):
# 	for j in range(ymax):
		# oled.pixel(i,j,1)

