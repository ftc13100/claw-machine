import pigpio

class LimitSwitchController:
    def __init__(self, pi, pins, debounceMicros=5000):
        self.pi = pi
        self.pins = list(pins)
        for pin in self.pins:
            pi.set_mode(pin, pigpio.INPUT)
            pi.set_pull_up_down(pin, pigpio.PUD_UP)
            pi.set_glitch_filter(pin, debounceMicros)

    def pressed(self, pins=None):
        pins = self.pins if pins is None else pins
        return any(self.pi.read(pin) == 0 for pin in pins)