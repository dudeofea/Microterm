import graphic_display
import time


display = graphic_display.GraphicDisplay()
sleep_time = 0.05

def circle_sweep(r_start, r_end, jump, clear=True):
    for r in range(r_start, r_end, jump):
        if clear:
            display.clear()
        display.circle(64, 32, r, True)
        display.refresh()
        if clear:
            time.sleep(sleep_time)
    #for r in range(r_end, r_start, -jump):
    #    display.circle(64, 32, r, True)
    #    if clear:
    #        time.sleep(sleep_time)
    #        display.clear()

while True:
    circle_sweep(1, 25, 1)

# circle in and out
#while True:
#    for r in range(15):
#        display.clear()
#        display.circle(64, 32, r, True)
#        time.sleep(sleep_time)
#    for r in range(15, 0, -1):
#        display.clear()
#        display.circle(64, 32, r, True)
#        time.sleep(sleep_time)

#y = 15
#x = 0
#for r in range(20):
#    display.circle(x, y, r, True)
#    x += 2 * r + 2
#    if x > 120:
#        x = r
#        y += 2 * r + 5
