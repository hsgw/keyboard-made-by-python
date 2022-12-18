import cadquery as cq

# use cq-server as gui, uncomment below line
# you can run cq-server `cd hardware && docker run -p 5000:5000 -v $(pwd):/data cadquery/cadquery-server run /data`
from cq_server.ui import ui, show_object

PCB_WIDTH = 76.0
PCB_HEIGHT = 57.0
PCB_THICKNESS = 1.6

CASE_MARGIN_TOP = 10.0
CASE_MARGIN_BOTTOM = 3.5
CASE_MARGIN_PCB = 0.5

CASE_FRAME = 2.0
CASE_BOTTOM = 3.0

SCREW_POINTS = [(19, 9.5), (19, -9.5), (-19, -9.5), (0, 9.5)]

USB_POS = (11.25, 1.2 + 3.15 / 2)
USB_HOLE_SIZE = [9, 3.2, 7.5]
USB_HOLE_MARGIN = 0.5
USB_CONN_SIZE = (11, 8)

INNER_HEIGHT = CASE_MARGIN_TOP + PCB_THICKNESS + CASE_MARGIN_BOTTOM
CASE_HEIGHT = INNER_HEIGHT + CASE_BOTTOM

# main body
case = (
    cq.Workplane("XY")
    .rect(
        PCB_WIDTH + (CASE_FRAME + CASE_MARGIN_PCB) * 2,
        PCB_HEIGHT + (CASE_FRAME + CASE_MARGIN_PCB) * 2,
    )
    .extrude(CASE_BOTTOM + INNER_HEIGHT)
    .edges("|Z")
    .fillet(2)
    .edges("|X")
    .chamfer(1)
)
# inner
case = (
    case.faces(">Z")
    .workplane()
    .rect(PCB_WIDTH + CASE_MARGIN_PCB * 2, PCB_HEIGHT + CASE_MARGIN_PCB * 2)
    .cutBlind(-INNER_HEIGHT)
)
# mounting holes
case = (
    case.faces(">Z")
    .workplane(offset=-INNER_HEIGHT)
    .tag("InnerBottom")
    .pushPoints(SCREW_POINTS)
    .circle(2.5)
    .extrude(CASE_MARGIN_BOTTOM)
    .workplaneFromTagged("InnerBottom")
    .pushPoints(SCREW_POINTS)
    .circle(1.1)
    .cutThruAll()
    .workplaneFromTagged("InnerBottom")
    .workplane(offset=-1)
    .pushPoints(SCREW_POINTS)
    .rect(4.2, 4.8)
    .cutBlind(-2)
)
# USB
case = (
    case.faces(">Y")
    .workplane(centerOption="CenterOfMass")
    .center(
        PCB_WIDTH / 2 - USB_POS[0],
        CASE_HEIGHT / 2 - CASE_MARGIN_TOP - PCB_THICKNESS - USB_POS[1],
    )
    .tag("USBCutout")
    .rect(USB_HOLE_SIZE[0] + USB_HOLE_MARGIN, USB_HOLE_SIZE[1] + USB_HOLE_MARGIN)
    .cutBlind(-(CASE_FRAME + USB_HOLE_SIZE[2] + 2))
    .workplaneFromTagged("USBCutout")
    .rect(USB_CONN_SIZE[0], USB_CONN_SIZE[1])
    .cutBlind(-1)
)

pcb = (
    cq.Workplane("XY")
    .workplane(offset=CASE_BOTTOM + CASE_MARGIN_BOTTOM)
    .rect(PCB_WIDTH, PCB_HEIGHT)
    .extrude(PCB_THICKNESS)
    .faces(">Z")
    .workplane()
    .pushPoints(SCREW_POINTS)
    .hole(2.2)
)

OLED_COVER_WIDTH = 19
OLED_COVER_HEIGHT = 19 * 2 - 3
OLED_COVER_THICKNESS = 10

oled_cover = (
    cq.Workplane("XY")
    .workplane(offset=CASE_BOTTOM + CASE_MARGIN_BOTTOM + PCB_THICKNESS)
    .center(-PCB_WIDTH / 2, PCB_HEIGHT / 2)
    .tag("PCB_ORIGIN")
    .center(OLED_COVER_WIDTH / 2, -OLED_COVER_HEIGHT / 2)
    .rect(OLED_COVER_WIDTH, OLED_COVER_HEIGHT)
    .extrude(OLED_COVER_THICKNESS)
)

# if use cq-server, uncomment
show_object(case, name="case")
show_object(pcb, name="pcb", options=dict(color=(0, 1, 0)))
show_object(oled_cover)

cq.exporters.export(case, "hardware/build/case/case.stl")
cq.exporters.export(oled_cover, "hardware/build/case/oled_cover.stl")
