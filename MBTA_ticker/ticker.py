"""MBTA Ticker app"""
import time

import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1305

from pymbta_predictions import mbta, predictions

UPDATE_RATE_S = 15

# Time to stay on after movement
HOLD_ONTIME_S = 10

# Shhh global variable
off_time = 0

oled_reset = digitalio.DigitalInOut(board.D4)
motion_sense = digitalio.DigitalInOut(board.D17)
motion_sense.direction = digitalio.Direction.INPUT
motion_sense.pull = digitalio.Pull.DOWN

WIDTH = 128
HEIGHT = 32
BORDER = 8

# Use for I2C.
i2c = board.I2C()
oled = adafruit_ssd1305.SSD1305_I2C(WIDTH, HEIGHT, i2c, addr=0x3c, reset=oled_reset)


def check_motion_sense():
  # global off_time
  # if motion_sense.value:
  #   off_time = time.time() + HOLD_ONTIME_S
  # return time.time() < off_time
  return True


def run():

  font = ImageFont.load_default()
  width = oled.width
  height = oled.height

  # First define some constants to allow easy resizing of shapes.
  padding = -2
  top = padding
  bottom = height - padding
  # Move left to right keeping track of the current x position for drawing shapes.
  x = 0
  next_update = time.time()

  image = Image.new("1", (width, height))
  draw = ImageDraw.Draw(image)

  trains = []
  update_display = False
  display_state = False

  print("Starting...")

  while True:
    if time.time() > next_update:
      # Poll the server for updated info at a slower rate
      print("Checking for updates")
      try:
        # Get MBTA predictions
        trains = predictions.get_predictions_for_stop(
          mbta.place_keys['central'], 'Red', 2)
      except Exception as exc:
        print(exc)
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        draw.text((x, top), ".", font=font, fill=255)
        oled.image(image)
        oled.show()
        trains = []
        # Add in some extra delay here to cut down on the number of requests when things aren't
        # running (like a night)
        time.sleep(10)

      print(trains)
      update_display = True
      next_update += UPDATE_RATE_S

    if check_motion_sense():
      if not display_state:
        print("detected movement")
        update_display = True
      display_state = True
    else:
      display_state = False

    if display_state:
      if not update_display:
        continue
      print("updating display")
      update_display = False
      draw.rectangle((0, 0, width, height), outline=0, fill=0)
      disp_lines = []
      for direction in [0, 1]:
        for train_num in [0, 1]:
          try:
            disp_lines.append(
              f'{trains[direction][train_num]["headsign"]}: '
              f'{trains[direction][train_num]["display_str"]}')
          except:
            disp_lines.append('')

      y_val = top
      for line in disp_lines:
        draw.text((x, y_val), line, font=font, fill=255)
        y_val += 8

      oled.image(image)
      oled.show()
    time.sleep(0.1)
