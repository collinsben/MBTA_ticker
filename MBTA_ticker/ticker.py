"""MBTA Ticker app"""
import time

import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1305

from pymbta_predictions import mbta, predictions

UPDATE_RATE_S = 5

oled_reset = digitalio.DigitalInOut(board.D4)

# Change these
# to the right size for your display!
WIDTH = 128
HEIGHT = 32
BORDER = 8

# Use for I2C.
i2c = board.I2C()
oled = adafruit_ssd1305.SSD1305_I2C(WIDTH, HEIGHT, i2c, addr=0x3c, reset=oled_reset)

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

  while True:
    if time.time() < next_update:
      time.sleep(0.1)
      continue

    # Get MBTA predictions
    trains = predictions.get_predictions_for_stop(
      mbta.place_keys['central'])

    # Clear display.
    oled.fill(0)
    oled.show()
    image = Image.new("1", (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    disp_lines = []
    for direction in [0, 1]:
      for train_num in [0, 1]:
        disp_lines.append(
          f'{trains[direction][train_num]["headsign"]}: {trains[direction][train_num]["display_str"]}')

    y_val = top
    for line in disp_lines:
      draw.text((x, y_val), line, font=font, fill=255)
      y_val += 8

    oled.image(image)
    oled.show()
