import pigpio


class LimitSwitchManager:
    def __init__(self, pi, pins, debounceMicros=5000):
        self.pi = pi
        self.pins = dict(pins)
        self.callbacks = []
        self.handlers = {}
        for name, pin in self.pins.items():
            pi.set_mode(pin, pigpio.INPUT)
            pi.set_pull_up_down(pin, pigpio.PUD_UP)
            pi.set_glitch_filter(pin, debounceMicros)

    def isPressed(self, name):
        return self.pi.read(self.pins[name]) == 0

    def anyPressed(self):
        return any(self.isPressed(name) for name in self.pins)

    def states(self):
        return {name: self.isPressed(name) for name in self.pins}

    def onPress(self, name, handler):
        self.handlers[name] = handler
        pin = self.pins[name]

        def wrapper(gpio, level, tick):
            if level == 0:
                handler(name)

        self.callbacks.append(self.pi.callback(pin, pigpio.FALLING_EDGE, wrapper))

    def close(self):
        for cb in self.callbacks:
            cb.cancel()
        self.callbacks = []


if __name__ == "__main__":
    import time

    pi = pigpio.pi()
    if not pi.connected:
        raise SystemExit("pigpiod is not running")

    limits = LimitSwitchManager(pi, {
        "limit1": 27,
        "limit2": 10,
        "limit3": 5,
        "limit4": 18,
    })

    for name in limits.pins:
        limits.onPress(name, lambda n: print(f"{n} pressed"))

    try:
        while True:
            time.sleep(0.5)
    finally:
        limits.close()
        pi.stop()
