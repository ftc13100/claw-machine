from JoystickController import JoystickController
from DisplayManager import DisplayManager
import time

with JoystickController() as joystick, DisplayManager() as display:
    try:
        while True:
            x, y, z  = joystick.readAll()
            display.showText(f"{x}, {y}", fontSize=18)
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\nProgram Killed")
