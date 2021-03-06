BASIC_W4 = {
    "width": 4,
    "data": [
    [0x00, 0x00, 0x00, 0x00, 0x00],  # SPACE
    [0x00, 0x00, 0xFA, 0x00],  # !
    [0x00, 0xC0, 0x00, 0xC0],  # "
    [0x28, 0x7C, 0x28, 0x7C],  # #
    [0x74, 0xFE, 0x5C, 0x00],  # $
    [0x24, 0x08, 0x10, 0x24],  # %
    [0x6C, 0x92, 0xAA, 0x46],  # &
    [0x00, 0x00, 0xC0, 0x00],  # '
    [0x00, 0x00, 0x7C, 0x82],  # (
    [0x00, 0x82, 0x7C, 0x00],  # )
    [0x54, 0x38, 0x38, 0x54],  # *
    [0x00, 0x10, 0x38, 0x10],  # +
    [0x00, 0x02, 0x04, 0x00],  # ,
    [0x00, 0x10, 0x10, 0x10],  # -
    [0x00, 0x00, 0x02, 0x00],  # .
    [0x06, 0x08, 0x10, 0x20],  # /

    # NUMBERS
    [0x7C, 0x8A, 0x92, 0x7C],  # 0
    [0x42, 0x42, 0xFE, 0x02],  # 1
    [0x46, 0x8A, 0x92, 0x62],  # 2
    [0x44, 0x92, 0x92, 0x6C],  # 3
    [0x18, 0x28, 0x48, 0xFE],  # 4
    [0xE4, 0xA2, 0xA2, 0x9C],  # 5
    [0x7C, 0x92, 0x92, 0x4C],  # 6
    [0x80, 0x9E, 0xA0, 0xC0],  # 7
    [0x6C, 0x92, 0x92, 0x6C],  # 8
    [0x64, 0x92, 0x92, 0x7C],  # 9

    # SPECIAL CHARS
    [0x00, 0x00, 0x24, 0x00],  # :
    [0x00, 0x02, 0x24, 0x00],  # ;
    [0x10, 0x28, 0x44, 0x82],  # <
    [0x28, 0x28, 0x28, 0x28],  # =
    [0x82, 0x44, 0x28, 0x10],  # >
    [0x40, 0x8A, 0x90, 0x60],  # ?
    #[0x7C, 0x82, 0x98, 0xA4, 0x78], # Original @
    [0x7C, 0x82, 0xBA, 0xA8],  # My @
    #[0x7C, 0x82, 0xB2, 0x8A, 0x74], # ROS@'s

    # UPPERCASE LETTERS
    [0x7E, 0x90, 0x90, 0x7E],  # A
    [0xFE, 0x92, 0x92, 0x6C],  # B
    [0x7C, 0x82, 0x82, 0x44],  # C
    [0xFE, 0x82, 0x82, 0x7C],  # D
    [0xFE, 0x92, 0x92, 0x82],  # E
    [0xFE, 0x90, 0x90, 0x80],  # F
    [0x7C, 0x82, 0x92, 0x5E],  # G
    [0xFE, 0x10, 0x10, 0xFE],  # H
    [0x82, 0xFE, 0x82, 0x00],  # I
    [0x04, 0x82, 0x82, 0xFC],  # J
    [0xFE, 0x10, 0x28, 0xC6],  # K
    [0xFE, 0x02, 0x02, 0x02],  # L
    [0xFE, 0x60, 0xFE, 0x00],  # M
    [0xFE, 0x20, 0x10, 0xFE],  # N
    [0x7C, 0x82, 0x82, 0x7C],  # O
    [0xFE, 0x90, 0x90, 0x60],  # P
    [0x7C, 0x82, 0x8A, 0x7A],  # Q
    [0xFE, 0x90, 0x98, 0x66],  # R
    [0x64, 0x92, 0x92, 0x4C],  # S
    [0x80, 0xFE, 0x80, 0x00],  # T
    [0xFC, 0x02, 0x02, 0xFC],  # U
    [0xF8, 0x04, 0x02, 0xFC],  # V
    [0xFE, 0x0C, 0xFE, 0x00],  # W
    [0xC6, 0x38, 0xC6, 0x00],  # X
    [0xE0, 0x10, 0x0E, 0xF0],  # Y
    [0x8E, 0x92, 0xA2, 0xC2],  # Z

    # SPECIAL CHARS
    [0x00, 0xFE, 0x82, 0x82],
    [0xC0, 0x20, 0x10, 0x08],
    [0x00, 0x82, 0x82, 0xFE],
    [0x00, 0x40, 0x80, 0x40],
    [0x02, 0x02, 0x02, 0x02],
    [0x00, 0x00, 0x80, 0x40],

    # LOWERCASE LETTERS
    [0x0C, 0x52, 0x52, 0x3C],  # A
    [0xFC, 0x22, 0x22, 0x1C],
    [0x3C, 0x42, 0x42, 0x24],
    [0x1C, 0x22, 0x22, 0xFC],
    [0x3C, 0x4A, 0x4A, 0x38],
    [0x00, 0x7E, 0x90, 0x80],
    [0x30, 0x4A, 0x4A, 0x3C],  # G
    [0xFE, 0x20, 0x20, 0x1E],
    [0x00, 0x20, 0xBC, 0x02],
    [0x04, 0x02, 0x22, 0xBC],
    [0xFE, 0x08, 0x14, 0x22],
    [0x00, 0x80, 0xFC, 0x02],
    [0x3E, 0x40, 0x3E, 0x40, 0x3E],  # m
    [0x3E, 0x40, 0x40, 0x3E],  # n
    [0x3C, 0x42, 0x42, 0x3C],  # o
    [0x3E, 0x48, 0x48, 0x30],  # p
    [0x30, 0x48, 0x48, 0x3E],  # q
    [0x00, 0x3E, 0x40, 0x40],  # r
    [0x24, 0x52, 0x4A, 0x24],  # s
    [0x00, 0x7C, 0x22, 0x22],  # t
    [0x7C, 0x02, 0x02, 0x7C],  # u
    [0x78, 0x04, 0x02, 0x7C],  # v
    [0x7C, 0x02, 0x3C, 0x02, 0x7C],  # w
    [0x42, 0x24, 0x18, 0x24],  # x
    [0x70, 0x0A, 0x0A, 0x7C],  # y
    [0x46, 0x4A, 0x52, 0x62],  # z

    # SPECIAL CHARS
    [0X00, 0x10, 0x6C, 0x82], # {
    [0x00, 0x00, 0x7E, 0x00], # |
    [0x00, 0x82, 0x6C, 0x10], # }
    [0x18, 0x20, 0x10, 0x08], # ~
    [0x00, 0x00, 0x00, 0x00, 0x00], # DEL
]}
