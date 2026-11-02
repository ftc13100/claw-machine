from JoystickController import JoystickController
from DisplayManager import DisplayManager
from ContinuousServoController import ContinuousServoController
import time

with JoystickController() as joystick, DisplayManager() as display, ConinuousServoController(servoPin=3) as crServo:
    try:
        while True:
            x, y, z  = joystick.readAll()
            display.showText(f"{x}, {y}", fontSize=18)
            crServo.setSpeed(x)
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\nProgram Killed")
