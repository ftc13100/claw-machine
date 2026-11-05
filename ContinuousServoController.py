import lgpio

class ContinuousServoController:
    def __init__(self, servoPin, handle=None, stopPulse=1500, maxOffset=500, chip=0):
        self.servoPin = servoPin
        self.stopPulse = stopPulse
        self.maxOffset = maxOffset
        self.ownsHandle = handle is None
        self.handle = lgpio.gpiochip_open(chip) if handle is None else handle
        lgpio.gpio_claim_output(self.handle, servoPin)
        self.speed = 0
        self.setSpeed(0)

    def setSpeed(self, speed):
        self.speed = max(-1, min(1, speed))
        result = lgpio.tx_servo(self.handle, self.servoPin, int(self.stopPulse + self.speed * self.maxOffset))
        if result < 0:
            print(f"tx_servo error: {result}")

    def stop(self):
        self.setSpeed(0)

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
