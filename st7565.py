from micropython import const
import time
import board
import busio
import digitalio

# LCD Commands definition
CMD_DISPLAY_ON = const(0xAF)
CMD_DISPLAY_OFF = const(0xAF)
CMD_SET_START_LINE = const(0x40)
CMD_SET_PAGE = const(0xB0)
CMD_COLUMN_UPPER = const(0x10)
CMD_COLUMN_LOWER = const(0x00)
CMD_SET_ADC_NORMAL = const(0xA0)
CMD_SET_ADC_REVERSE = const(0xA1)
CMD_SET_COL_NORMAL = const(0xC0)
CMD_SET_COL_REVERSE = const(0xC8)
CMD_SET_DISPLAY_NORMAL = const(0xA6)
CMD_SET_DISPLAY_REVERSE = const(0xA7)
CMD_SET_ALLPX_ON = const(0xA5)
CMD_SET_ALLPX_NORMAL = const(0xA4)
CMD_SET_BIAS_9 = const(0xA2)
CMD_SET_BIAS_7 = const(0xA3)
CMD_DISPLAY_RESET = const(0xE2)
CMD_NOP = const(0xE3)
CMD_TEST = const(0xF0)  # Exit this mode with CMD_NOP
CMD_SET_POWER = const(0x28)
CMD_SET_RESISTOR_RATIO = const(0x20)
CMD_SET_VOLUME = const(0x81)

# Display parameters
DISPLAY_W = const(128)
DISPLAY_H = const(64)
DISPLAY_CONTRAST = const(0x1B)
DISPLAY_RESISTOR_RATIO = const(5)
DISPLAY_POWER_MODE = 7

class ST7565:
    """ST7565 Display controller driver"""
    def __init__(self):
        self.spi = busio.SPI(board.SCK, MOSI=board.MOSI)
        while not self.spi.try_lock():
            pass
        self.spi.configure(baudrate=460800)
        self.spi.unlock()

        print("SPI Speed:", self.spi.frequency)
        self.reset_pin = digitalio.DigitalInOut(board.D6)
        self.cs_pin = digitalio.DigitalInOut(board.D10)
        self.a0_pin = digitalio.DigitalInOut(board.D9)
        self.width = DISPLAY_W
        self.height = DISPLAY_H
        self.display_init()

    def display_init(self):
        self.reset_pin.direction = digitalio.Direction.OUTPUT
        self.cs_pin.direction = digitalio.Direction.OUTPUT
        self.a0_pin.direction = digitalio.Direction.OUTPUT
        self.reset()
        time.sleep(0.001)
        self.write_cmds([
            CMD_DISPLAY_OFF,  # Display off
            CMD_SET_BIAS_9,  # Display drive voltage 1/9 bias
            CMD_SET_ADC_NORMAL,  # Reverse SEG
            CMD_SET_COL_NORMAL,  # Commmon mode normal direction
            CMD_SET_RESISTOR_RATIO + DISPLAY_RESISTOR_RATIO,  # V5 R ratio
            CMD_SET_VOLUME,  # Contrast
            DISPLAY_CONTRAST,  # Contrast value
            CMD_SET_POWER + DISPLAY_POWER_MODE
        ])
        self.clear()
        self.set_cursor(0, 0)
        self.write_cmds([CMD_DISPLAY_ON])

    def write_cmds(self, cmds):
        while not self.spi.try_lock():
            pass
        self.a0_pin.value = False
        self.cs_pin.value = False
        self.spi.write(bytes(cmds))
        self.cs_pin.value = True
        self.spi.unlock()

    def write_data(self, buf):
        while not self.spi.try_lock():
            pass
        self.a0_pin.value = True
        self.cs_pin.value = False
        try:
            self.spi.write(buf)
        except OSError:
            self.spi.write(buf)
        self.cs_pin.value = True
        self.spi.unlock()

    def set_contrast(self, value):
        if 0x1 <= value <= 0x3f:
            self.write_cmds([CMD_SET_VOLUME, value])

    def set_cursor(self, x, y):
        self.write_cmds([
            CMD_SET_PAGE + (7 - y),            # set row
            CMD_COLUMN_UPPER + ((0xF0 & x) >> 4),    # set ram addr msb
            CMD_COLUMN_LOWER + (0x0F & x)          # set ram addr lsb
        ])

    def reset(self):
        self.reset_pin.value = False
        time.sleep(0.001)
        self.reset_pin.value = True

    def clear(self):
        buf = [0x00] * 128
        for i in range(8):
            self.set_cursor(0, i)
            self.write_data(bytes(buf))

    def add_blocks(self, values, pos):
        self.set_cursor(pos[0], pos[1])
        self.write_data(bytes(values))

    def add_string(self, input_str, pos, font_map):
        self.set_cursor(pos[0], pos[1])
        font_width = font_map["width"] + 1
        width = int((128 - (128 % font_width)) / font_width)
        line_buf = [0x00] * width * font_width
        line_x = 0
        print("Add string:", pos)
        print_str = ""
        for c in input_str:
            # go down in y by 1 if newline
            if c == '\n':
                pos = [0, pos[1] + 1]
                self.write_data(bytes(line_buf))
                self.set_cursor(pos[0], pos[1])
                line_buf = [0x00] * width * font_width
                line_x = 0
                print_str += str(pos) + "\n"
                continue
            else:
                print_str += c

            # add character to line buffer
            char = font_map["data"][ord(c) - 32]
            line_buf[line_x:line_x+len(char)] = char
            line_x += font_width

            # increment x, and y if needed
            pos[0] += 1
            if pos[0] >= width:
                pos = [0, pos[1] + 1]
                self.write_data(bytes(line_buf))
                self.set_cursor(pos[0], pos[1])
                line_buf = [0x00] * width * font_width
                line_x = 0
                print_str += str(pos) + "\n"

        self.write_data(bytes(line_buf))
        print(print_str)
        return pos
