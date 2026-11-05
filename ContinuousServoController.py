import lgpio

class ContinuousServoController:
    def __init__(self, servoPin, handle=None, stopPulse=1500, maxOffset=500, chip=0, limitSwitches=None):
        self.servoPin = servoPin
        self.stopPulse = stopPulse
        self.maxOffset = maxOffset
        self.ownsHandle = handle is None
        self.handle = lgpio.gpiochip_open(chip) if handle is None else handle
        lgpio.gpio_claim_output(self.handle, servoPin)
        self.speed = 0
        self.limitSwitches = limitSwitches

        self.setSpeed(0)

    def runServoSpeed(self):
        result = lgpio.tx_servo(self.handle, self.servoPin, int(self.stopPulse + self.speed * self.maxOffset))
        if result < 0:
            print(f"tx_servo error: {result}")

    def anyPressed(self):
        return any(switch.pressed() for switch in self.limitSwitches)

    def setSpeed(self, speed):
        speed = max(-1, min(1, speed))
        if self.anyPressed():
            if self.blockedDirection == 0 and self.speed != 0:
                self.blockedDirection = 1 if self.speed > 0 else -1
        else:
            self.blockedDirection = 0
        if speed != 0 and (1 if speed > 0 else -1) == self.blockedDirection:
            speed = 0
        self.speed = speed
        self.runServoSpeed()

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
