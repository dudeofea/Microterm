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
        self.rck = digitalio.DigitalInOut(board.A0)
        self.width = DISPLAY_W
        self.height = DISPLAY_H
        #self.buffer = bytearray(1024)
        self.display_init()

    def display_init(self):
        self.rck.direction = digitalio.Direction.OUTPUT
        self.reset()
        time.sleep(0.001)
        for cmd in (
            CMD_DISPLAY_OFF,  # Display off
            CMD_SET_BIAS_9,  # Display drive voltage 1/9 bias
            CMD_SET_ADC_NORMAL,  # Reverse SEG
            CMD_SET_COL_NORMAL,  # Commmon mode normal direction
            CMD_SET_RESISTOR_RATIO + DISPLAY_RESISTOR_RATIO,  # V5 R ratio
            CMD_SET_VOLUME,  # Contrast
            DISPLAY_CONTRAST,  # Contrast value
                CMD_SET_POWER + DISPLAY_POWER_MODE):
            self.write_cmd(cmd)
        self.show()
        self.set_cursor(0, 0)
        self.write_cmd(CMD_DISPLAY_ON)

    def write_cmd(self, cmd):
        while not self.spi.try_lock():
            pass
        self.rck.value = True
        self.spi.write(bytes([0x01]))
        self.rck.value = False
        self.rck.value = True
        self.spi.write(bytes([cmd]))
        self.rck.value = False
        self.spi.write(bytes([0x00]))
        self.rck.value = True
        self.spi.unlock()

    def write_data(self, buf):
        while not self.spi.try_lock():
            pass
        self.rck.value = True
        self.spi.write(bytes([0x00]))
        self.rck.value = False
        self.rck.value = True
        self.spi.write(bytes(buf[1]))
        self.rck.value = False
        self.spi.write(buf[1:])
        self.rck.value = True
        self.spi.unlock()

    def set_contrast(self, value):
        if 0x1 <= value <= 0x3f:
            for cmd in (
                CMD_SET_VOLUME,
                    value):
                self.write_cmd(cmd)

    def set_cursor(self, x, y):
        self.write_cmd(CMD_SET_PAGE + (8 - y - 1))    # set row
        self.write_cmd(CMD_COLUMN_UPPER + (0xF0 & x))    # set ram addr msb
        self.write_cmd(CMD_COLUMN_LOWER + (0x0F & x))    # set ram addr lsb

    def reset(self):
        while not self.spi.try_lock():
            pass
        self.rck.value = True
        self.spi.write(bytes([0x02]))
        self.rck.value = False
        self.rck.value = True
        time.sleep(0.001)
        self.spi.write(bytes([0x00]))
        self.rck.value = False
        self.rck.value = True
        self.spi.unlock()

    def show(self):
        for i in range(8):
            self.write_cmd(CMD_SET_PAGE + i)
            self.write_cmd(CMD_COLUMN_UPPER)    # set ram addr to 0
            self.write_cmd(CMD_COLUMN_LOWER)
            #self.write_data(self.buffer[i*128:(i+1)*128])

    #def char(self, x, y, character, width):
    #    for i in range(len(character)):
    #        self.buffer[(8 - y - 1)*128 + x*width + i] = character[i]

    def string(self, input_str, input_pos, font_map):
        self.set_cursor(input_pos[0], input_pos[1])
        print(input_str, input_pos)
        # TODO: don't assume font's are 5x7 w/o spacing
        f_width = font_map["width"] + 1
        width = int((128 - (128 % f_width)) / f_width)
        height = 8
        pos = input_pos
        buf = [0x00] * width * f_width
        off = 1
        for c in input_str:
            if c == '\n':
                pos[0] = 0
                pos[1] += 1
                print(pos)
                off = 1
                self.write_data(bytes(buf))
                self.set_cursor(pos[0], pos[1])
                buf = [0x00] * width * f_width
                continue

            #self.char(pos[0], pos[1], font_map["data"][ord(c) - 32], f_width)
            char = font_map["data"][ord(c) - 32]
            buf[off:off+len(char)] = char
            off += f_width

            pos[0] += 1
            if pos[0] >= width:
                pos[1] += 1
                pos[0] = 0
                print(pos)
                off = 1
                self.write_data(bytes(buf))
                self.set_cursor(pos[0], pos[1])
                buf = [0x00] * width * f_width
        self.write_data(bytes(buf))
        return pos
