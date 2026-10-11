from BuzzerController import BuzzerController
from JoystickController import JoystickController
import time

with JoystickController() as joystick, BuzzerController() as buzzer:
    print("Buzzer Test")
    for frequency in (262, 330, 392, 523):
        buzzer.playTone(frequency)
        time.sleep(0.25)
        buzzer.off()

    try:
        while True:
            x, y, z  = joystick.readAll()
            print(f"({x}, {y}) | Pressed: {z}")
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\nProgram Killed")
