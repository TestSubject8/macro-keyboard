import time
from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import sh1106
import os

serial = spi(device=0, port=0) #, gpio_DC=6,gpio_RST=4,gpio_CS=5)
device = sh1106(serial, rotate=2)

device.clear()

last = time.time()

def frame(callback, args=None, sleep_time=0):
  global last
  now = time.time()
  fps = round(1/(now-last),2)
  with canvas(device) as draw:
    callback(draw, args)

    # Bottom text - FPS
    draw.rectangle((80,55,130,65),fill='black',outline='black')
    draw.text((80,50),str(fps),fill='white')

    # Middle text - Task
    draw.rectangle((8,8,110,27),fill='black',outline='white')
    draw.text((10,15),"START A NEW LOAD", align='center', fill='white', stroke_fill='black')
  time.sleep(sleep_time)
  device.clear()
  last = time.time()

#while True:
#  x = 2
#  y = 2
#  offset = 0
#  with canvas(device) as draw:
#  # draw.rectangle(device.bounding_box, outline="white", fill="black")
#    message = ["You are a genius","immortal who deserves","their high head"]
#    for i in range(len(message)):
#      draw.text((x, y+i*12), message[i], fill="white")
#  time.sleep(2)
#  print('done')
#    
#  device.clear()
#  points = []
#  for i in range(128):
#    for j in range(64):
#      with canvas(device) as draw:
#        points.append((i,j))
#        draw.point(points, fill='white')
#
#  time.sleep(2)
#  print('done')
