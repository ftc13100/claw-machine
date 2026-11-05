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
    global claw, clawLift, xServo, yServo, xSwitches, ySwitches, joystick, display

    xSwitches = LimitSwitchController(pi, X_SWITCH_PINS)
    ySwitches = LimitSwitchController(pi, Y_SWITCH_PINS)

    claw = ServoController(servoPin=CLAW_PIN, maxAngle=300, startAngle=0)
    clawLift = ServoController(servoPin=CLAW_LIFT_PIN, maxAngle=300, startAngle=0)

    xServo = ContinuousServoController(servoPin=X_SERVO_PIN, limitSwitches=[xSwitches])
    yServo = ContinuousServoController(servoPin=Y_SERVO_PIN, limitSwitches=[ySwitches])

    joystick = JoystickController()
    display = DisplayController()

# Claw Commands
def clawResetPos():
    try:
        while not (xSwitches.pressed() and ySwitches.pressed()):
            xServo.setSpeed(1)
            yServo.setSpeed(1)
            time.sleep(UPDATE_RATE)
    finally:
        xServo.stop()
        yServo.stop()

def clawUp(): clawLift.setPosition(0)
def clawDown(): clawLift.setPosition(285)
def clawOpen(): claw.setPosition(160)
def clawClose(): claw.setPosition(200)

# Game Functions

def setupGame():
    clawUp()
    time.sleep(4)
    clawClose()
    clawResetPos()
    display.showText("Ready to play")

def waitForStart():
    while not joystick.isPressed():
        time.sleep(UPDATE_RATE)
    while joystick.isPressed():
        time.sleep(UPDATE_RATE)

def collect():
    xServo.stop()
    yServo.stop()
    
    clawOpen()
    clawDown()
    time.sleep(8)
    clawClose()
    time.sleep(0.5)
    clawUp()
    clawResetPos()
    clawOpen()

def playGame():
    endTime = time.monotonic() + PLAY_TIME
    lastSeconds = None

    while True:
        timeRemaining = endTime - time.monotonic()
        seconds = int(timeRemaining)
        
        if seconds != lastSeconds:
            display.showText(str(seconds) + "s Remaining")
            lastSeconds = seconds

        x, y, pressed = joystick.readAll()
        xServo.setSpeed(-x)
        yServo.setSpeed(y)

        if pressed or timeRemaining <= 0:
            display.showText("Collecting...")
            collect()
            break

        time.sleep(UPDATE_RATE)

# Main Program
try:
    initHardware()

    while (True):
        setupGame()
        waitForStart()
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