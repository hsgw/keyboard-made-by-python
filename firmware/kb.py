import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation


class KMKKeyboard(_KMKKeyboard):
    row_pins = (board.D0, board.D5, board.D6)
    col_pins = (
        board.D7,
        board.D2,
        board.D3,
        board.D4,
    )
    diode_orientation = DiodeOrientation.COL2ROW

    # oled
    SCL = board.D10
    SDA = board.D8

    # fmt: off
    coord_mapping = [
            1,  2,  3,
            5,  6,  7,
        8,  9, 10, 11
    ]
    # fmt: on
