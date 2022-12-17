from skidl import *
from pcbflow import *

if __name__ == "__main__":
    ### make netlist(circuit) by skidl

    KEY_COUNT = 10
    COL_COUNT = 4
    ROW_COUNT = 3

    # fmt: off
    # switch matrix mapping
    MATRIX_MAP = [
              (0,1),(0,2),(0,3),  
              (1,1),(1,2),(1,3),
        (2,0),(2,1),(2,2),(2,3)
    ]
    # fmt: on

    # add local libraries
    lib_search_paths[KICAD].append("hardware/kicad_libs")
    footprint_search_paths[KICAD].append("hardware/kicad_libs/kicad.pretty")

    # components
    diode = Part(
        "kicad_symbols", "D_Small_ALT", TEMPLATE, footprint="kicad:D_SOD123_hand"
    )
    switch = Part(
        "kicad_symbols",
        "SW_Push",
        TEMPLATE,
        footprint="kicad:SW_Cherry_MX_1.00u_PCB",
    )

    diodes = diode(KEY_COUNT)
    switches = switch(KEY_COUNT)

    xiao = Part("kicad_symbols", "xiao_rp2040", footprint="kicad:xiao_rp2040")
    oled = Part("kicad_symbols", "oled_i2c", footprint="kicad:oled_i2c")

    # if use netlist with pcbnew
    # hole = Part("kicad_symbols", "MountingHole", TEMPLATE, footprint="kicad:HOLE_D2.2")
    # holes = hole(4)

    # create net for key-matrix
    netRows = [Net(f"ROW{i}") for i in range(ROW_COUNT)]
    netCols = [Net(f"COL{i}") for i in range(COL_COUNT)]

    # wiring
    # print part object for see the pin description
    # print(oled)
    # print(xiao)

    # row -> sw -> diode -> col
    for sw, d, mapping in zip(switches, diodes, MATRIX_MAP):
        netRows[mapping[0]] & sw["1 2"] & d["K A"] & netCols[mapping[1]]

    # matrix -> xiao
    netCols[0] += xiao[8]
    netCols[1] += xiao[3]
    netCols[2] += xiao[4]
    netCols[3] += xiao[5]

    netRows[0] += xiao[1]
    netRows[1] += xiao[6]
    netRows[2] += xiao[7]

    # oled -> xiao
    Net("3.3V") & oled["Vcc"] & xiao["3.3V"]
    Net("GND") & oled["GND"] & xiao["GND"]
    Net("SDA") & oled["SDA"] & xiao[9]
    Net("SCL") & oled["SCL"] & xiao[11]

    # ERC()
    generate_netlist()

    ### place parts and draw trace by pcbflow

    # Calculate coordinates with origin in the upper left corner
    def pos(x, y):
        return (x, BOARD_HEIGHT - y)

    BOARD_WIDTH = 76.0
    BOARD_HEIGHT = 57.0

    LAYER_TOP = "GTL"
    LAYER_BOTTOM = "GBL"

    # DRC setting
    circuit = builtins.default_circuit
    # create board
    board = Board((BOARD_WIDTH, BOARD_HEIGHT))
    board.drc.trace_width = 0.5
    board.drc.via_drill = 0.6
    board.drc.via_annular_ring = 0.4
    board.drc.clearance = 0.4

    # assign placement position to skidl parts
    for sw, d, mapping in zip(switches, diodes, MATRIX_MAP):
        sw.pos = pos(mapping[1] * 19 + 9.5, mapping[0] * 19 + 9.5)
        sw.side = "top"
        d.pos = (sw.pos[0] + 6, sw.pos[1] + 5)
        d.side = "bottom"
        d.rotate = 0

    xiao.pos = pos(11.25, 11.5)
    xiao.side = "bottom"

    oled.pos = pos(9.5, 36)
    oled.side = "top"
    oled.rotate = 270

    # add holes
    board.add_hole(pos(38, 19), 2.2)
    board.add_hole(pos(57, 19), 2.2)
    board.add_hole(pos(57, 38), 2.2)
    board.add_hole(pos(19, 38), 2.2)

    # place parts on board
    for part in circuit.parts:
        try:
            rotate = part.rotate
        except:
            rotate = 0

        try:
            SkiPart(board.DC(part.pos).right(rotate), part, side=part.side)
        except AttributeError:
            print(f"{part.ref} has no pos or side")
            continue

    ### wiring
    xiaoRef = "U1"
    xiaoPart = board.get_part(xiaoRef)

    oledRef = "DISP1"
    oledPart = board.get_part(oledRef)

    # get connected pin number from skidl net
    # pin number is started from 1 in skidl, 0 in pcbflow
    def get_pin_number_from_net(netLabel, ref):
        net = Net.get(netLabel)
        return list((int(x.num) - 1 for x in net.pins if x.ref == ref))[0]

    # get access xiao pads by net label
    # convert to correct pin number for solving the complication of the kicad library
    # apply newpath() for bug fix (the initial value has a strange value)
    def xiao_pads(net: str):
        return xiaoPart.pads[get_pin_number_from_net(net, xiaoRef) + 14].newpath()

    # d -> sw
    for i in range(1, KEY_COUNT + 1):
        sw = board.get_part(f"SW{i}")
        d = board.get_part(f"D{i}")
        d.pads[0].set_layer(LAYER_BOTTOM).w("f 1 r 45").align_meet(sw.pads[1], "x")

    viaCol = [0] * 4
    # col d->d (col 1-3)
    for i in range(1, 4):
        d1 = board.get_part(f"D{i}")
        d2 = board.get_part(f"D{i+3}")
        d3 = board.get_part(f"D{i+7}")
        via = (
            d1.pads[1]
            .set_name(f"COL{i}")
            .set_layer(LAYER_BOTTOM)
            .w("l 180 f 1.25 r 45 f 2 l 45 f 6.5 l 45")
            .align(d2.pads[1], "y")
            .wire()
            .via()
        )
        viaCol[i] = via
        via.set_layer(LAYER_BOTTOM).meet(d2.pads[1])
        d2.pads[1].set_name(f"COL{i}").set_layer(LAYER_BOTTOM).w(
            "l 180 f 1 r 45 f 2 l 45 f 6.5 l 45"
        ).align_meet(d3.pads[1], "y")

    # col 0 xiao-> d
    xiao_pads("COL0").set_layer(LAYER_BOTTOM).w(
        "l 180 f 18 r 45 f 2 r 45 f 9.5 l 45"
    ).align_meet(board.get_part("D7").pads[1], "y")

    # col 1-3 via -> xiao
    viaCol[1].set_layer(LAYER_TOP).w("l 45 f 11 l 45").align_meet(
        xiao_pads("COL1"), "x"
    )
    viaCol[2].set_layer(LAYER_TOP).w("f 2 l 45 f 29.5 l 45").align_meet(
        xiao_pads("COL2"), "x"
    )
    viaCol[3].set_layer(LAYER_TOP).w("f 4 l 45 f 48.5 l 45").align_meet(
        xiao_pads("COL3"), "x"
    )

    # row xiao -> sw
    xiao_pads("ROW0").set_layer(LAYER_TOP).w("r 45").align_meet(
        board.get_part("SW1").pads[0], "x"
    )
    xiao_pads("ROW1").set_layer(LAYER_TOP).w("r 45").align_meet(
        board.get_part("SW4").pads[0], "y"
    )
    xiao_pads("ROW2").set_layer(LAYER_TOP).w("l 180 f 12 r 45").align_meet(
        board.get_part("SW8").pads[0], "y"
    )

    # row sw->sw
    for i in range(3):
        refs = list(x.ref for x in netRows[i].pins if x.ref.startswith("SW"))
        for j in range(len(refs) - 1):
            board.get_part(refs[j]).pads[0].newpath().set_layer(LAYER_TOP).w(
                "r 90 f 2 l 45 f 1 r 45 f 2.5 r 45 f1"
            ).meet(board.get_part(refs[j + 1]).pads[0])

    # xiao -> oled
    OLED_NETS = ["GND", "3.3V", "SCL", "SDA"]
    OLED_GAP = [0, 3.6, 7.2, 10.5]
    for net, gap in zip(OLED_NETS, OLED_GAP):
        oledPin = board.get_part(oledRef).pads[get_pin_number_from_net(net, "DISP1")]
        xiao_pads(net).set_layer(LAYER_TOP).left(135).align_meet(oledPin, "y")

    # for layer in [LAYER_TOP, LAYER_BOTTOM]:
    #     xiao_pads("GND").set_layer(layer).w(
    #         "r 90 f 1.5 r 180 f 3 r 180 f 1.5 r 90"
    #     ).wire()
    #     board.get_part(oledRef).pads[
    #         get_pin_number_from_net("GND", "DISP1")
    #     ].newpath().set_layer(layer).w("r 90 f 1.5 r 180 f 3 r 180 f 1.5 r 90").wire()

    # place logos
    board.add_bitmap(
        (47.5, 28.5), "hardware/imgs/python-logo.png", side="top", scale=0.85
    )

    board.add_bitmap(
        (11.25, 45),
        "hardware/imgs/QR.png",
        side="bottom",
        scale=0.75,
    )

    board.add_bitmap(
        (11, 28.5),
        "hardware/imgs/logo-python-powered-w-logo.png",
        side="bottom",
        layer="GBS",
        scale=0.7,
    )
    board.add_bitmap(
        (11, 28.5),
        "hardware/imgs/logo-python-powered-w-logoBG.png",
        side="bottom",
        layer="GBL",
        scale=0.7,
    )
    board.add_bitmap(
        (11, 28.5),
        "hardware/imgs/logo-python-powered-w-text.png",
        side="bottom",
        scale=0.7,
    )

    board.add_bitmap(
        (47.5, 22),
        "hardware/imgs/dm9-logo.png",
        side="bottom",
        scale=0.8,
    )

    board.add_bitmap(
        (66.5, 22),
        "hardware/imgs/hsgw-logo.png",
        side="bottom",
        scale=0.4,
    )

    # place texts
    board.add_text(
        (47.5, 41.5),
        "https://github.com/hsgw/keyboard_made_by_python",
        scale=1.25,
        side="bottom",
    )

    board.add_text(
        (BOARD_WIDTH - 39, 5),
        "KEYBOARD MADE BY PYTHON",
        scale=2,
        side="bottom",
        justify="left",
    )
    board.add_text(
        (BOARD_WIDTH - 44, 4.75),
        "Rev.1",
        scale=1.25,
        side="bottom",
        justify="left",
    )
    board.add_text(
        (BOARD_WIDTH - 47.5, 2.25),
        "(c) 2022, Takuya Urakawa / Dm9Records / 5z6p.com",
        scale=1.25,
        side="bottom",
        justify="left",
    )

    board.add_text(
        (11.5, 55),
        "JLCJLCJLCJLC",
        scale=1.1,
        side="bottom",
    )

    board.add_outline()
    board.save_png("kbd_python", subdir="hardware/build/pcb_png")
    board.save_gerbers("kbd_python", subdir="hardware/build/pcb_gerber")
