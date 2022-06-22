import luma_oled
import os
import time

def set_border(draw, opts):
  draw.rectangle(luma_oled.device.bounding_box, outline='white', fill='black')

def temp(draw, args):
  draw.text((10,10),cpu_temp)

def split(draw, opts):
  split_point = (127/2, 63/2)
  db = luma_oled.device.bounding_box

  draw.rectangle((db[0],db[1],split_point[0],db[3]), outline='white', fill='black') 
  draw.rectangle((split_point[0],db[1],db[2],db[3]), outline='white', fill='black') 

while(True):
#  luma_oled.frame(write_text,("Hello Ash!"),10)
#  cpu_temp = os.popen("vcgencmd measure_temp").readline().replace("temp=", "")
#  luma_oled.frame(write_text, cpu_temp, 1)
  luma_oled.frame(split, None, 10)
