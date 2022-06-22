import luma_oled
import os
import time

def set_border(draw, opts):
  draw.rectangle(luma_oled.device.bounding_box, outline='white', fill='black')

def write_text(draw, opts):
  # print(opts)
  draw.rectangle(luma_oled.device.bounding_box, outline='white', fill='black')
  draw.multiline_text((50,30),opts, align='center', fill='white')

def dot(draw, opts):
  x = int(opts[0])
  y = int(opts[1])

  size = 3
  for i in range(size+1):
    for j in range(size+1):
      draw.point((x+i,y+j), fill='white')

def pixel_bounce():
  x = 0
  y = 0
  dx = 1.3
  dy = 1
  limit = 128
# for i in range(3):
  while(True):
    if y >= 64: 
      dy = -1
      border_y = 0
    if y <= 0: 
      dy = 1
      border_y = 64
    if x <= 0: 
      dx = 1.3
      border_x = 128
    if x >= 128:
      dx = -1.3
      border_y = 0
    x += dx
    y += dy
    luma_oled.frame(dot,(x,y),1/60)
    

  for i in range(3):
    delta = [1,1,-1,-1]
    border = [128,64,0,0]
    while(x<border[0]):
      x += delta[0]
      y += delta[1]
      if x == border[0]:
        delta[0] = -1
        border[0] = 0
      if y == border[1]:
        delta[1] = -1
        border[1] = 0
      luma_oled.frame(dot,(x,y),1/10)
    luma_oled.device.clear() 

def temp(draw, args):
  draw.text((10,10),cpu_temp)

while(True):
  luma_oled.frame(write_text,("Hello Ash!"),10)
  #luma_oled.frame(pixel_bounce)
  #pixel_bounce()

  # cpu_temp = os.popen("vcgencmd measure_temp").readline().replace("temp=", "")
  # luma_oled.frame(write_text, cpu_temp, 1)
