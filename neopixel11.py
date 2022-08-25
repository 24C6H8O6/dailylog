import board
import neopixel
import time

pixels = neopixel.NeoPixel(board.D18,8)

while True:
    pixels.fill((0,255,0))
    pixels.show()
    time.sleep(1)
    pixels.fill((0,0,255))
    pixels.show()
    time.sleep(1)
    