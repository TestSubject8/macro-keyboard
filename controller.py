import luma_oled
import socket
import os
import time

def set_border(draw, opts):
  draw.rectangle(luma_oled.device.bounding_box, outline='white', fill='black')

def write_text(draw, opts):
  # print(opts)
  draw.rectangle(luma_oled.device.bounding_box, outline='white', fill='black')
  draw.multiline_text((30,30),opts, align='center', fill='white')

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
    
def temp(draw, args):
  cpu_temp = os.popen("vcgencmd measure_temp").readline().replace("temp=", "")
  draw.text((10,10),cpu_temp)

def framerate(draw, args):
  global last
  now = time.time()
  fps = round(1/(now - args), 2)
  write_text(draw, str(fps))
  last = time.time()


def ip_echo():
  # hostname = socket.gethostname()
  # IPAddr = socket.gethostbyname(hostname)

  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.settimeout(0)
  try:
      # doesn't even have to be reachable
      s.connect(('10.254.254.254', 1))
      IP = s.getsockname()[0]
  except Exception:
      IP = '127.0.0.1'
  finally:
      s.close()

  luma_oled.frame(write_text, (IP), 10)
  

while(True):
  # luma_oled.frame(write_text,("Hello Ash!"),10)
  # luma_oled.frame(pixel_bounce)
  # pixel_bounce()
  ip_echo()
  # luma_oled.frame(temp, sleep_time=1)
