import font_utils
import st7565

class ScrollingDisplay():
    def __init__(self, font):
        self.display = st7565.ST7565()
        self.display.set_contrast(0x20)
        self.cursor = [0, 0]
        self.buf = ""
        self.buf_offset = 0
        self.disp_offset = 0
        self.font = font
        self.display_width = font_utils.get_max_char_width(font)

    def add_string(self, input_str):
        self.buf += input_str
        self.display.string(input_str, self.cursor, self.font)
        #self.display.show()

    def delete_char(self):
        self.buf = self.buf[:-1]
        # back up cursor
        self.cursor[0] -= 1
        if self.cursor[0] < 0 and self.cursor[1] > 0:
            self.cursor[1] -= 1
            self.cursor[0] = self.display_width - 1
        self.display.string(chr(127), [self.cursor[0], self.cursor[1]], self.font)
        #self.display.show()

    def redraw(self):
        # split lines longer than screen width
        lines = []
        for l in self.buf.split('\n'):
            while len(l) > 0:
                lines.append(l[:self.display_width])
                l = l[self.display_width:]

        # redraw all lines padded/
        for i in range(-self.disp_offset, len(lines)):
            # pad lines with blanks
            pad = self.display_width - len(lines[i])
            print(lines, pad)
            self.display.string(lines[i] + pad * " ",
                                [0, i + self.disp_offset],
                                self.font)
        #self.display.show()

    def scroll_down(self):
        self.disp_offset -= 1
        self.buf_offset = self.buf.find('\n', self.buf_offset)
        # blank out current line, then redraw
        self.display.string(self.display_width * " ",
                            [0, self.cursor[1]],
                            self.font)
        self.cursor[1] -= 1
        self.redraw()

    def scroll_up(self):
        pass
