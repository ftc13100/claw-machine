import threading
import time
import RPi.GPIO as GPIO


class DisplayController:
    charMap = {
        "0": 0x3F, "1": 0x06, "2": 0x5B, "3": 0x4F, "4": 0x66,
        "5": 0x6D, "6": 0x7D, "7": 0x07, "8": 0x7F, "9": 0x6F,
        "A": 0x77, "b": 0x7C, "C": 0x39, "d": 0x5E, "E": 0x79,
        "F": 0x71, "H": 0x76, "L": 0x38, "P": 0x73, "U": 0x3E,
        "r": 0x50, "o": 0x5C, "n": 0x54, "-": 0x40, "_": 0x08, " ": 0x00,
    }

    def __init__(self, dataPin=23, latchPin=24, clockPin=25, digitCount=4, commonAnode=True, digitDelay=0.002):
        self.dataPin = dataPin
        self.latchPin = latchPin
        self.clockPin = clockPin
        self.digitCount = digitCount
        self.commonAnode = commonAnode
        self.digitDelay = digitDelay

        self.buffer = [0] * digitCount
        self.lock = threading.Lock()
        self.running = False
        self.thread = None

        GPIO.setmode(GPIO.BCM)
        GPIO.setup([self.dataPin, self.latchPin, self.clockPin], GPIO.OUT, initial=GPIO.LOW)

        self.start()

    def shiftOut(self, value):
        for bit in range(7, -1, -1):
            GPIO.output(self.dataPin, (value >> bit) & 1)
            GPIO.output(self.clockPin, GPIO.HIGH)
            GPIO.output(self.clockPin, GPIO.LOW)

    def writeBytes(self, segmentByte, digitByte):
        GPIO.output(self.latchPin, GPIO.LOW)
        self.shiftOut(digitByte)
        self.shiftOut(segmentByte)
        GPIO.output(self.latchPin, GPIO.HIGH)

    def writeFrame(self, pattern, index):
        if self.commonAnode:
            segmentByte = ~pattern & 0xFF
            digitByte = 1 << index
        else:
            segmentByte = pattern
            digitByte = ~(1 << index) & 0xFF
        self.writeBytes(segmentByte, digitByte)

    def blank(self):
        if self.commonAnode:
            self.writeBytes(0xFF, 0x00)
        else:
            self.writeBytes(0x00, 0xFF)

    def refresh(self):
        while self.running:
            for index in range(self.digitCount):
                with self.lock:
                    pattern = self.buffer[index]

                self.writeFrame(pattern, index)
                time.sleep(self.digitDelay)

    def start(self):
        if self.thread is not None and self.thread.is_alive():
            return
        self.running = True
        self.thread = threading.Thread(target=self.refresh, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False

        if self.thread is not None:
            self.thread.join()
            self.thread = None

        self.blank()

    def showText(self, text):
        patterns = []
        for char in text:
            if char == ".":
                if patterns and not patterns[-1] & 0x80:
                    patterns[-1] |= 0x80
                else:
                    patterns.append(0x80)
            else:
                patterns.append(
                    self.charMap.get(char, self.charMap.get(char.upper(), self.charMap.get(char.lower(), 0)))
                )

        patterns = patterns[-self.digitCount:]
        patterns = [0] * (self.digitCount - len(patterns)) + patterns

        with self.lock:
            self.buffer = patterns

    def showNumber(self, value, decimals=0, leadingZeros=False):
        text = f"{value:.{decimals}f}"
        cells = len(text.replace(".", ""))

        if cells > self.digitCount:
            self.showText("-" * self.digitCount)
            return

        padding = self.digitCount - cells
        fill = "0" if leadingZeros and value >= 0 else " "
        self.showText(fill * padding + text)

    def clear(self):
        with self.lock:
            self.buffer = [0] * self.digitCount

    def cleanup(self):
        self.stop()
        GPIO.cleanup([self.dataPin, self.latchPin, self.clockPin])

    def __enter__(self):
        return self

    def __exit__(self, excType, exc, tb):
        self.cleanup()
