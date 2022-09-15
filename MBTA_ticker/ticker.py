"""MBTA Ticker app"""
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1305

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
  pass