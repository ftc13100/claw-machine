import RPi.GPIO as GPIO

class BuzzerController:
    def __init__(self, buzzerPin=17):
        self.buzzerPin = buzzerPin
        self.pwm = None
        self.toneActive = False

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.buzzerPin, GPIO.OUT, initial=GPIO.LOW)

    def on(self):
        self.stopTone()
        GPIO.output(self.buzzerPin, GPIO.HIGH)

    def off(self):
        self.stopTone()
        GPIO.output(self.buzzerPin, GPIO.LOW)

    def playTone(self, frequency):
        if self.pwm is None:
            self.pwm = GPIO.PWM(self.buzzerPin, frequency)
        else:
            self.pwm.ChangeFrequency(frequency)
        if not self.toneActive:
            self.pwm.start(50)
            self.toneActive = True

    def stopTone(self):
        if self.toneActive:
            self.pwm.stop()
            self.toneActive = False

    def cleanup(self):
        self.off()
        GPIO.cleanup(self.buzzerPin)

    def __enter__(self):
        return self

    def __exit__(self, excType, exc, tb):
        self.cleanup()
