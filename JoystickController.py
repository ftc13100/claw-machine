import time
import RPi.GPIO as GPIO
from smbus2 import SMBus

class JoystickController:
    def __init__(self, switchPin=18, xChannel=1, yChannel=0, deadzone=0.1, busNumber=1, address=0x4b):
        self.switchPin = switchPin
        self.xChannel = xChannel
        self.yChannel = yChannel
        self.deadzone = deadzone
        self.address = address
        self.lastValues = {}

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.switchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.bus = SMBus(busNumber)
        self.xCenter = 128
        self.yCenter = 128
        self.calibrate()

    def readChannel(self, channel, retries=5):
        command = 0x84 | (((channel << 2 | channel >> 1) & 0x07) << 4)

        for i in range(retries):
            try:
                last = self.bus.read_byte_data(self.address, command)
                value = last

                for j in range(5):
                    value = self.bus.read_byte_data(self.address, command)
                    if value == last:
                        break
                    last = value
                
                self.lastValues[channel] = value
                return value
            except OSError:
                pass
        
        if channel in self.lastValues:
            return self.lastValues[channel]
        
        raise OSError("ADC not responding")

    def calibrate(self, samples=20):
        xTotal = 0
        yTotal = 0

        for i in range(samples):
            xTotal += self.readChannel(self.xChannel)
            yTotal += self.readChannel(self.yChannel)
            time.sleep(0.01)
        
        self.xCenter = xTotal / samples
        self.yCenter = yTotal / samples

    def normalize(self, value, center):
        if value >= center:
            result = (value - center) / (255 - center)
        else:
            result = (value - center) / center
        
        if abs(result) < self.deadzone:
            return 0.0
        
        return round(max(-1.0, min(1.0, result)), 2)

    def readX(self):
        return self.normalize(self.readChannel(self.xChannel), self.xCenter)

    def readY(self):
        return self.normalize(self.readChannel(self.yChannel), self.yCenter)

    def isPressed(self):
        return GPIO.input(self.switchPin) == GPIO.LOW

    def readAll(self):
        return self.readX(), self.readY(), self.isPressed()

    def __enter__(self):
        return self

    def __exit__(self, excType, exc, tb):
        self.bus.close()
        GPIO.cleanup(self.switchPin)


def main():
    with JoystickController() as joystick:
        lastState = None
        try:
            while True:
                state = joystick.readAll()
                if state != lastState:
                    x, y, pressed = state
                    print(f"x={x:+.2f}  y={y:+.2f}  pressed={pressed}")
                    lastState = state

                time.sleep(0.02)
        except KeyboardInterrupt:
            print("\nProgram Killed")


if __name__ == "__main__":
    main()
