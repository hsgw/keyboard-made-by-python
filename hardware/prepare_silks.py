from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

import numpy as np
from PIL import Image, ImageDraw, ImageOps

svgFile = "hardware/imgs/python-powered-w.svg"
outputPath = "hardware/imgs/"

imgArray = np.array(renderPM.drawToPIL(svg2rlg(svgFile)).convert("L"))
imgArray = np.uint8((imgArray < 127) * 255)
imgRaw = Image.fromarray(imgArray, mode="L")

logoMaskPos = (20, 0, 280, 280)
textMaskPos = (290, 0, 720, 280)

# draw = ImageDraw.Draw(imgRaw)
# draw.ellipse(logoMaskPos, outline=100)
# draw.rectangle(textMaskPos, outline=100)

# only logo
img = imgRaw.copy()
draw = ImageDraw.Draw(img)
draw.rectangle(textMaskPos, fill=0)
img.save(outputPath + "logo-python-powered-w-logo.png")

# only logo bg
draw.ellipse(logoMaskPos, fill=255)
img.save(outputPath + "logo-python-powered-w-logoBG.png")

# only text
img = imgRaw.copy()
draw = ImageDraw.Draw(img)
draw.ellipse(logoMaskPos, fill=0)
img.save(outputPath + "logo-python-powered-w-text.png")
