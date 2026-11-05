import time
from PIL import ImageFont
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306


class DisplayController:
    def __init__(self, busNumber=1, address=0x3C, width=128, height=64,
                 fontPath="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                 fontSize=19, lineSpacing=4):
        self.width = width
        self.height = height
        self.address = address
        self.fontPath = fontPath
        self.lineSpacing = lineSpacing

        self.serial = i2c(port=busNumber, address=self.address)
        self.device = ssd1306(self.serial, width=self.width, height=self.height)

        self.fontSize = fontSize
        self.font = ImageFont.truetype(self.fontPath, self.fontSize)

    def setFontSize(self, size):
        self.fontSize = int(size)
        self.font = ImageFont.truetype(self.fontPath, self.fontSize)

    def clear(self):
        self.device.clear()

    def showText(self, text, fontSize=None):
        if fontSize is not None and int(fontSize) != self.fontSize:
            self.setFontSize(fontSize)

        lines = str(text).split("\n")

        with canvas(self.device) as draw:
            boxes = [draw.textbbox((0, 0), line, font=self.font) for line in lines]
            heights = [box[3] - box[1] for box in boxes]
            totalHeight = sum(heights) + self.lineSpacing * (len(lines) - 1)
            y = (self.height - totalHeight) // 2

            for line, box, height in zip(lines, boxes, heights):
                x = (self.width - (box[2] - box[0])) // 2 - box[0]
                draw.text((x, y - box[1]), line, fill="white", font=self.font)
                y += height + self.lineSpacing

    def close(self):
        self.device.clear()
        self.device.cleanup()

    def __enter__(self):
        return self

    def __exit__(self, excType, exc, tb):
        self.close()