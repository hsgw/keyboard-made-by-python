> これは[キーボード #1 Advent Calendar 2022](https://adventar.org/calendars/7529)の20日目の記事の一部です。   
> トップページは[Pythonだけでキーボードを作る](https://5z6p.com/2022/12/21/ac2022/)です。

# ファームウェアを作る
ファームウェアは組み込み向けPythonの[CircuitPython](https://circuitpython.org/)ベースで実装された[KMK Firmware](https://github.com/KMKfw/kmk_firmware)を使用します。   
- CircuitPython https://circuitpython.org/
- KMK Firmware https://github.com/KMKfw/kmk_firmware

RP2040とCircuitPythonの環境なら認識されたドライブへ直接Pythonのコードを書き込むだけです。もちろん、保存したファイルを直接編集すればコードが書き換わります。

## KMK Firmwareをインストールする
KMK Firmwareの[Getting start guide](https://github.com/KMKfw/kmk_firmware/blob/master/docs/en/Getting_Started.md)を参考にしてインストールします。

- XIAO RP2040向けCircuitPythonの7.xをインストールします。(2022/12時点では7.3.3)
https://circuitpython.org/board/seeeduino_xiao_rp2040/

## 追加のライブラリをインストールする
KMK FirmwareのOLED機能を利用するために必要なパッケージを導入します。

- OLED機能のドキュメント
https://github.com/KMKfw/kmk_firmware/blob/master/docs/en/peg_oled_display.md

ドキュメントにある通り、bundleをダウンロードして`adafruit-circuitpython-bundle-7.x～/lib`内にある`adafruit_display_text`(ディレクトリごと)、`adafruit_displayio_ssd1306.mpy`を認識されたXIAOのドライブ内の`lib/`以下にコピーします。

# ファームウェア
KMK Fimwareでは`kb.py`と`main.py`が必要です。
このキーボード用のファームウェアは[firmware/](../../firmware/)内にあります。

XIAOのルートに予め`code.py`もしくは`main.py`がある場合は一旦削除します。   
`boot.py`や`libs/`などは削除しません。

## kb.py
`kb.py`では、キーボードのハードウェア情報を定義します。

```python
# CircuitPythonで定義されているboard情報
# 最初にダウンロードしたCircuitPythonによって変わる
# print(dir(board))で定義が確認できる
import board

from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation

class KMKKeyboard(_KMKKeyboard):
    # マトリクスのピン情報
    row_pins = (board.D0, board.D5, board.D6)
    col_pins = (
        board.D7,
        board.D2,
        board.D3,
        board.D4,
    )
    # マトリクスのダイオードの方向
    diode_orientation = DiodeOrientation.COL2ROW

    # oledで使用するi2cのピン
    SCL = board.D10
    SDA = board.D8

    # マトリクスと実際のキー位置の紐付け
    # QMKのLAYOUTみたいなもの
    # fmt: off
    coord_mapping = [
            1,  2,  3,
            5,  6,  7,
        8,  9, 10, 11
    ]
    # fmt: on

```

## main.py
`main.py`では、キーボードのキーマップや振る舞いを実装します。   
また、OLEDに表示する画像をビットマップとして用意します。

```python
import board

# kb.pyをインポート
from kb import KMKKeyboard

# キーコード
from kmk.keys import KC
# レイヤー機能
from kmk.modules.layers import Layers
# OLEDエクステンション
from kmk.extensions.peg_oled_Display import (
    Oled,
    OledDisplayMode,
    OledReactionType,
    OledData,
)

keyboard = KMKKeyboard()

# レイヤー機能を有効化
layers_ext = Layers()
keyboard.modules.append(layers_ext)

# キーボードの設定
keyboard.tap_time = 250
# デバッグ
# Trueにするとシリアルポートへデバッグ情報を出力する
keyboard.debug_enabled = False

# OLEDの設定
# 画像は白黒のビットマップとして用意する
oled_ext = Oled(
    OledData(image={0: OledReactionType.STATIC, 1: ["oled_python.bmp"]}),
    toDisplay=OledDisplayMode.IMG,
    flip=True,
)
keyboard.extensions.append(oled_ext)

# キーマップで使うキーコード
____ = KC.TRNS

L1_P0 = KC.LT(1, KC.P0)

# キーマップ
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

# XIAOに書き込む
`kb.py`と`main.py`、画像ファイルをXIAOへ書き込んで動作確認をします。   
キーボードとして正しく認識されているか、OLEDに正しい画像が表示されているか確認しました。
これで完成です!
