"""MBTA Ticker app"""
import time

import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1305

import pymbta_predictions

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
    predictions = pymbta_predictions.query.get_predictions_for_stop(
      pymbta_predictions.mbta.place_keys['central'])

    # Clear display.
    oled.fill(0)
    oled.show()
    image = Image.new("1", (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    draw.text((x, top + 0), predictions[0][0]['display_str'], font=font, fill=255)
    draw.text((x, top + 8), predictions[0][1]['display_str'], font=font, fill=255)
    draw.text((x, top + 16), predictions[1][0]['display_str'], font=font, fill=255)
    draw.text((x, top + 25), predictions[1][1]['display_str'], font=font, fill=255)

    oled.image(image)
    oled.show()
