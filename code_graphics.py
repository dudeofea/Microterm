import graphic_display
import time

display = graphic_display.GraphicDisplay()
for y in range(64):
    for x in range(128):
        display.pixel(x, y, True)
        time.sleep(0.1)
