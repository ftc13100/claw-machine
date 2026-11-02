import lgpio

class ContinuousServoManager:
    def __init__(self, servoPin, handle=None, stopPulse=1500, maxOffset=500):
        self.servoPin = servoPin
        self.stopPulse = stopPulse
        self.maxOffset = maxOffset
        self.ownsHandle = handle is None
        self.handle = lgpio.gpiochip_open(0) if handle is None else handle
        self.speed = 0
        self.setSpeed(0)

    def setSpeed(self, speed):
        self.speed = speed
        lgpio.tx_servo(self.handle, self.servoPin, int(self.stopPulse + speed * self.maxOffset))

    def stop(self):
        self.setSpeed(0)

    def release(self):
        lgpio.tx_servo(self.handle, self.servoPin, 0)

    def close(self):
        self.release()
        if self.ownsHandle:
            lgpio.gpiochip_close(self.handle)
