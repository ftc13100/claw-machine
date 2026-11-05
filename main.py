# Imports
import time
import pigpio

from JoystickController import JoystickController
from DisplayController import DisplayController
from ServoController import ServoController
from ContinuousServoController import ContinuousServoController
from LimitSwitchController import LimitSwitchController

# Hardware Constants
pi = pigpio.pi()

CLAW_PIN = 10
CLAW_LIFT_PIN = 6

X_SERVO_PIN = 11
Y_SERVO_PIN = 9

X_SWITCH_PINS = [18, 27]
Y_SWITCH_PINS = [5, 21]

# Software Constants
UPDATE_RATE = 0.02
TICKS_TO_SECOND = 1 / UPDATE_RATE

# Game Constants
PLAY_TIME = 60

# Hardware Objects
claw = None
clawLift = None

xServo = None
yServo = None

xSwitches = None
ySwitches = None

joystick = None
display = None

def initHardware():
    claw = ServoController(
        servoPin=CLAW_PIN,
        maxAngle=300,
        startAngle=0
    )

    clawLift = ServoController(
        servoPin=CLAW_LIFT_PIN,
        maxAngle=300,
        startAngle=0
    )

    xServo = ContinuousServoController(
        servoPin=X_SERVO_PIN
    )

    yServo = ContinuousServoController(
        servoPin=Y_SERVO_PIN
    )

    xSwitches = LimitSwitchController(pi, X_SWITCH_PINS)
    ySwitches = LimitSwitchController(pi, Y_SWITCH_PINS)

    joystick = JoystickController()

    display = DisplayController()

# Claw Commands
def clawResetPos():
    axes = {"x": [xServo, xSwitches, False], "y": [yServo, ySwitches, False]}
    try:
        for servo, switches, done in axes.values():
            servo.setSpeed(1)
        while not all(axis[2] for axis in axes.values()):
            for axis in axes.values():
                servo, switches, done = axis
                if not done and switches.pressed():
                    servo.setSpeed(0)
                    axis[2] = True
            time.sleep(UPDATE_RATE)
    finally:
        xServo.setSpeed(0)
        yServo.setSpeed(0)

def clawUp(): clawLift.setPosition(0)
def clawDown(): clawLift.setPosition(300)
def clawOpen(): clawLift.setPosition(0)
def clawClose(): clawLift.setPosition(300)

# Game Functions
def setupGame():
    clawLift.setPosition(0)
    claw.setPosition(0)
    clawResetPos()
    display.showText("Press to play")

def playGame():
    buttonPressed = False

    while (not buttonPressed):
        x, y, pressed = joystick.readAll()
        xServo.setSpeed(-x)
        yServo.setSpeed(y)

        if (pressed):
            xServo.stop()
            yServo.stop()
            
            clawDown()
            time.sleep(5)
            clawClose()
            time.sleep(0.5)
            clawUp()
            clawResetPos()
            clawOpen()

            buttonPressed = True

        time.sleep(UPDATE_RATE)

# Main Program
try:
    initHardware()

    while True:
        setupGame()
        playGame()

finally:
    # Close here means unmounting hardware
    claw.close()
    clawLift.close()

    xServo.stop()
    xServo.close()

    yServo.stop()
    yServo.close()

    joystick.close()
    display.close()