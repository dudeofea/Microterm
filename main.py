from basic_font_w4 import BASIC_W4 as DISPLAY_FONT
import font_utils
import scrolling_display
import supervisor
import sys

display = scrolling_display.ScrollingDisplay(DISPLAY_FONT)
display.add_string("> this is some text\nthat I added to test scrolling\nheyo")

def process_line(input_str):
    try:
        out = eval(input_str)
        return "\n" + str(out) + "\n>"
    except:
        pass
    try:
        exec(input_str)
        return "\n>"
    except Exception as e:
        return "\n" + str(e) + "\n>"

line_pos = [1, 0]
line_buf = ">"
line_limit = 1
display_buf_pos = 1
while True:
    if supervisor.runtime.serial_bytes_available:
        char_input = sys.stdin.read(1)
        # catch special characters
        char_ord = ord(char_input)
        display_char = True
        if char_ord == 10:  # NEWLINE
            newline_ind = line_buf.rfind('\n>') + 2

            output = process_line(line_buf[newline_ind:])
            display.add_string(output)
            line_buf += output
            line_limit = len(line_buf)
            display_char = False

        elif char_ord == 27:   # ESC CHAR
            # read next two chars
            char_input = sys.stdin.read(2)
            if char_input == "[A":
                display.scroll_up()
            elif char_input == "[B":
                display.scroll_down()
            elif char_input == "[C":
                print("Right arrow")
            else:
                print("Left arrow")
            display_char = False

        elif char_ord == 127:  #DEL
            if len(line_buf) > line_limit:
                display.delete_char()
                line_buf = line_buf[:-1]
            display_char = False

        # display character
        if display_char:
            line_buf += char_input
            display.add_string(char_input)
        print([ord(c) for c in line_buf], line_pos)
