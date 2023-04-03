import luma_oled
import socket
import os, sys
import time

def set_border(draw, opts):
  draw.rectangle(luma_oled.device.bounding_box, outline='white', fill='black')

def write_text(draw, opts):
  # print(opts)
  draw.rectangle(luma_oled.device.bounding_box, outline='white', fill='black')
  draw.multiline_text((15,25),opts, align='center', fill='white')

def overlay_text(draw, opts):
  draw.multiline_text((15,25),opts, align='center', fill='white')

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

def countdown(dur):
  start_time = time.monotonic()
  elapsed = 0
  while elapsed <= dur:
    elapsed = round(time.monotonic() - start_time, 0)
    rem = (dur - elapsed)/60
    remaining = round(rem, 3)
    # luma_oled.frame(write_text, (str(remaining)+' m'), 1)
    # luma_oled.frame(blocks, int(rem), 1)
    luma_oled.frame(notify, int(rem), 1)
  for i in ['white', 'black']:
    luma_oled.frame(flash, i, 0.5)

    # I can make this way more complex by adding the intended block of lights to represent minutes 
    # make it a separate thing
    # 
    # For each min remaining draw a little block and iterate the position of them dynamically
    # Keep a pointer to the next little block and update it to the right location if it crosses a border

def notify(draw, args):
  remaining = args
  count = 0

  row = 0
  column = 0

  for i in range(remaining):
    if i!=0 and i%5==0:
      row += 1
      column = 0
    block(draw, column*25, row*25)
    column += 1

    # In order to overlay the text on the blocks
    # luma_oled.frame(overlay_text,"PUTTING AWAY DRYS",10)

def block(draw, x, y):
  draw.rectangle((x,y,x+23,y+23), fill='white')

def flash(draw, args):
  draw.rectangle(luma_oled.device.bounding_box, fill=args)

try: 
  while(True):
    # luma_oled.frame(write_text,("Hello Ash!"),10)

    # mi = open('moon_info','r')
    # lines = mi.readlines()
    # print(''.join(lines))
    # luma_oled.frame(write_text,(''.join(lines)),10)
    # luma_oled.frame(pixel_bounce)
    # pixel_bounce()
    # ip_echo()
    # luma_oled.frame(temp, sleep_time=1)
    # countdown(2)
    countdown(10*60)
    # countdown(2*60)
except KeyboardInterrupt:
  luma_oled.device.cleanup()
  sys.exit()
