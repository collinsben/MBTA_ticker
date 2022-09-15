import setuptools

setuptools.setup(
  name='MBTA Ticker',
  version='0.0.1',
  author='Ben Collins',
  license='MIT',
  packages=setuptools.find_namespace_packages(),
  entry_points={
    'console_scripts':
      ['mbta_ticker = MBTA_ticker.ticker:run',
       'hello_world = MBTA_ticker.display_test:run'],
  },
  install_requires=[
    'Adafruit-Blinka',
    'adafruit-circuitpython-busdevice',
    'adafruit-circuitpython-framebuf',
    'adafruit-circuitpython-ssd1305',
    'RPi.GPIO',
  ]
)
