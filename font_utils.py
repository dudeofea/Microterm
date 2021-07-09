def get_max_char_width(font):
    f_width = font["width"] + 1
    return int((128 - (128 % f_width)) / f_width)

def gen_all_chars():
    out = ""
    for i in range(32, 128):
        out += chr(i)
        if i % 16 == 15:
            out += '\n'
    return out
