import board

from kb import KMKKeyboard

from kmk.handlers.sequences import send_string, simple_key_sequence
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.extensions.peg_oled_Display import (
    Oled,
    OledDisplayMode,
    OledReactionType,
    OledData,
)

keyboard = KMKKeyboard()
layers_ext = Layers()
keyboard.modules.append(layers_ext)

keyboard.tap_time = 250
keyboard.debug_enabled = False

oled_ext = Oled(
    OledData(image={0: OledReactionType.STATIC, 1: ["oled_python.bmp"]}),
    toDisplay=OledDisplayMode.IMG,
    flip=True,
)
keyboard.extensions.append(oled_ext)

____ = KC.TRNS

L1_P0 = KC.LT(1, KC.P0)

# fmt: off
keyboard.keymap = [
    # default layer
    [     
           KC.P7, KC.P8, KC.P9,
           KC.P4, KC.P5, KC.P6,
    L1_P0, KC.P1, KC.P2, KC.P3 
    ],
    # Fn layer
    [     
           KC.ESC,  KC.DEL, KC.BSPC,
           KC.COMM, KC.NO,  KC.TAB,
    ____,  KC.DOT,  KC.SPC, KC.ENT 
    ],
]
# fmt: on

if __name__ == "__main__":
    keyboard.go()
