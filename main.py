from display import ST7565
from fonts import BASIC_FONT as DISPLAY_FONT
import font_utils
import supervisor
import sys

display = ST7565()
display.set_contrast(0x20)
display.string(">", [0, 0], DISPLAY_FONT)
#display.string(font_utils.gen_all_chars(), [0, 0], DISPLAY_FONT)
display.show()
SCREEN_CHAR_WIDTH = font_utils.get_max_char_width(DISPLAY_FONT)
print("max width:", SCREEN_CHAR_WIDTH)

def process_line(input_str):
    try:
        out = eval(input_str)
        return "\n" + "eval: " + str(out) + "\n>"
    except:
        pass
    try:
        exec(input_str)
        return "\n|  executed\n>"
    except:
        pass
    return "\nError\n>"

def delete_char(buf, pos):
    pos[0] -= 1
    if pos[0] < 0 and pos[1] > 0:
        pos[1] -= 1
        pos[0] = SCREEN_CHAR_WIDTH - 1
    return pos

line_pos = [1, 0]
line_buf = ">"
line_limit = 1
while True:
    if supervisor.runtime.serial_bytes_available:
        char_input = sys.stdin.read(1)
        # catch special characters
        char_ord = ord(char_input)
        display_char = True
        if char_ord == 10:  # NEWLINE
            newline_ind = line_buf.rfind('\n>') + 2

            output = process_line(line_buf[newline_ind:])
            display.string(output, line_pos, DISPLAY_FONT)
            line_buf += output
            line_limit = len(line_buf)
            display_char = False

        elif char_ord == 127:  #DEL
            if len(line_buf) > line_limit:
                # TODO: scroll back to previous newline in buffer
                line_pos = delete_char(line_buf, line_pos)
                display.string(char_input,
                               [line_pos[0], line_pos[1]],
                               DISPLAY_FONT)
                line_buf = line_buf[:-1]
            display_char = False

        # display character
        if display_char:
            line_buf += char_input
            line_pos = display.string(char_input, line_pos, DISPLAY_FONT)
        print([ord(c) for c in line_buf], line_pos)
        display.show()
