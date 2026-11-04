import time

from JoystickController import JoystickController
from ContinuousServoManager import ContinuousServoManager
from ServoManager import ServoManager


# GPIO assignments (BCM)
X_SERVO_PIN = 11
Y_SERVO_PIN = 9

CLAW_PIN = 10
CLAW_LIFT_PIN = 6

UPDATE_RATE = 0.02


def main():

    joystick = None
    x_servo = None
    y_servo = None
    claw = None
    claw_lift = None

    try:
        print("Initializing servos...")

        # Initialize claw servos
        claw = ServoManager(
            servoPin=CLAW_PIN,
            maxAngle=300,
            startAngle=0
        )

        claw_lift = ServoManager(
            servoPin=CLAW_LIFT_PIN,
            maxAngle=300,
            startAngle=0
        )

        # Initialize continuous rotation servos
        x_servo = ContinuousServoManager(
            servoPin=X_SERVO_PIN
        )

        y_servo = ContinuousServoManager(
            servoPin=Y_SERVO_PIN
        )

        # Initialize joystick
        joystick = JoystickController()

        print("\nRobot ready!")
        print("X axis: GPIO 11")
        print("Y axis: GPIO 9")
        print("Claw: GPIO 10")
        print("Claw lift: GPIO 6")
        print("Press joystick button to activate claw.\n")

        button_was_pressed = False

        while True:

            # Read joystick
            x, y, pressed = joystick.readAll()

            # Always update drive servos
            x_servo.setSpeed(x)
            y_servo.setSpeed(y)

            # Detect new button press
            if pressed and not button_was_pressed:

                print("\nClaw sequence started!")

                # Stop movement while operating claw
                x_servo.stop()
                y_servo.stop()

                # Move claw down
                print("Moving claw down...")
                claw_lift.setPosition(300)

                # Wait 5 seconds
                print("Waiting 5 seconds...")
                time.sleep(5)

                # Close claw
                print("Closing claw...")
                claw.setPosition(300)

                time.sleep(0.5)

                # Raise claw
                print("Moving claw up...")
                claw_lift.setPosition(0)

                print("Claw sequence complete!\n")

                # Prevent held button from triggering again
                button_was_pressed = True

            elif not pressed:
                button_was_pressed = False

            time.sleep(UPDATE_RATE)

    except KeyboardInterrupt:
        print("\nStopping robot...")

    finally:

        # Stop continuous servos
        if x_servo is not None:
            x_servo.stop()
            x_servo.close()

        if y_servo is not None:
            y_servo.stop()
            y_servo.close()

        # Release position servos
        if claw is not None:
            claw.close()

        if claw_lift is not None:
            claw_lift.close()

        # Release joystick resources
        if joystick is not None:
            joystick.__exit__(None, None, None)

        print("All servos released.")


if __name__ == "__main__":
    main()
