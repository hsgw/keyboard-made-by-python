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
keyboard.modules = [layers_ext]

keyboard.tap_time = 250
keyboard.debug_enabled = False

oled_ext = Oled(
    OledData(image={0: OledReactionType.STATIC, 1: ["oled_python.bmp"]}),
    toDisplay=OledDisplayMode.IMG,
    flip=True,
)

keyboard.extensions.append(oled_ext)

# fmt: off
keyboard.keymap = [
    [     
           KC.P7, KC.P8, KC.P9,
           KC.P4, KC.P5, KC.P6,
    KC.P0, KC.P1, KC.P2, KC.P3 
    ]
]
# fmt: on

if __name__ == "__main__":
    keyboard.go()
