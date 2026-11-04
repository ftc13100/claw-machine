import lgpio

class ServoManager:
    def __init__(self, servoPin, handle=None, chip=0, minPulse=500, maxPulse=2500, maxAngle=180, startAngle=None):
        self.servoPin = servoPin
        self.minPulse = minPulse
        self.maxPulse = maxPulse
        self.maxAngle = maxAngle
        self.ownsHandle = handle is None
        self.handle = lgpio.gpiochip_open(chip) if handle is None else handle
        lgpio.gpio_claim_output(self.handle, servoPin)
        self.angle = None
        if startAngle is not None:
            self.setPosition(startAngle)

    def setPosition(self, angle):
        self.angle = max(0, min(self.maxAngle, angle))
        pulse = self.minPulse + (self.angle / self.maxAngle) * (self.maxPulse - self.minPulse)
        result = lgpio.tx_servo(self.handle, self.servoPin, int(pulse))
        if result < 0:
            print(f"tx_servo error: {result}")

    def release(self):
        lgpio.tx_servo(self.handle, self.servoPin, 0)

    def close(self):
        self.release()
        lgpio.gpio_free(self.handle, self.servoPin)
        if self.ownsHandle:
            lgpio.gpiochip_close(self.handle)

    def __enter__(self):
        return self

    def __exit__(self, excType, excValue, traceback):
        self.close()
        return False
