> Project page is [Keyboard as a Python Code](https://hackaday.io/project/188907-keyboard-as-a-python-code)

# Create firmware
The firmware uses [KMK Firmware](https://github.com/KMKfw/kmk_firmware), based on [CircuitPython](https://circuitpython.org/), which is an embedded Python Implementation.    
- CircuitPython https://circuitpython.org/
- KMK Firmware https://github.com/KMKfw/kmk_firmware

With the RP2040 and CircuitPython, you can simply write the Python code directly to the drive recognised. Of course, the code can be rewritten by editing the saved file itself.

## Install KMK Firmware
Install KMK Firmware following [Getting started guide](https://github.com/KMKfw/kmk_firmware/blob/master/docs/en/Getting_Started.md).

- Install CircuitPython 7.x for XIAO RP2040. (7.3.3 as of 2022/12)
https://circuitpython.org/board/seeeduino_xiao_rp2040/

## Install additional libraries
Install the packages required to use the OLED feature of KMK Firmware.

- Documentation for OLED feature
https://github.com/KMKfw/kmk_firmware/blob/master/docs/en/peg_oled_display.md

Download the bundle as described in the documentation. Copy `adafruit_display_text/` and `adafruit_displayio_ssd1306.mpy` in `adafruit-circuitpython-bundle-7.x~/lib/` to under `lib/` in the XIAO drive.

# Create firmware
KMK Firmware requires `kb.py` and `main.py`.
The firmware for this keyboard can be found in [firmware/](. /... /firmware/).

If you find `code.py` or `main.py` in the root of XIAO already, remove them once.   
Do not delete `boot.py`, `libs/`, and so on.

## kb.py
In `kb.py`, define the hardware information for the keyboard.

```python
# Board information defined in CircuitPython
# It depends on CircuitPython installed.
# print(dir(board)) to check the definition
import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation

class KMKKeyboard(_KMKKeyboard):
    # pin assigns for switch matrix
    row_pins = (board.D0, board.D5, board.D6)
    col_pins = (
        board.D7,
        board.D2,
        board.D3,
        board.D4,
    )
    # diode orientation
    diode_orientation = DiodeOrientation.COL2ROW

    # I2C pin assign for OLED
    SCL = board.D10
    SDA = board.D8

    # Linking the matrix to the actual key position
    # like LAYOUT in QMK
    # fmt: off
    coord_mapping = [
            1,  2,  3,
            5,  6,  7,
        8,  9, 10, 11
    ]
    # fmt: on

```

## main.py
In `main.py`, implement the keyboard keymap and behavior.   
It also prepares the image to be displayed on the OLED as a bitmap.

```python
import board

from kb import KMKKeyboard

from kmk.keys import KC
from kmk.modules.layers import Layers
# OLED extension
from kmk.extensions.peg_oled_Display import (
    Oled,
    OledDisplayMode,
    OledReactionType,
    OledData,
)

keyboard = KMKKeyboard()

# enable layer
layers_ext = Layers()
keyboard.modules.append(layers_ext)

# keyboard setting
keyboard.tap_time = 250
# debug
# If set to True, debug information is output to the serial port.
keyboard.debug_enabled = False

# OLED config
# # The image should be a black and white bitmap.
oled_ext = Oled(
    OledData(image={0: OledReactionType.STATIC, 1: ["oled_python.bmp"]}),
    toDisplay=OledDisplayMode.IMG,
    flip=True,
)
keyboard.extensions.append(oled_ext)

____ = KC.TRNS
L1_P0 = KC.LT(1, KC.P0)

# keymap
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

```

# Write to XIAO
Write `kb.py`, `main.py` and the image file to XIAO and check the working.   
Now it is complete!
