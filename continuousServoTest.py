
import time
from ContinuousServoManager import ContinuousServoManager


def main():

    servo = None

    try:
        while True:

            print("\n======= CONTINUOUS SERVO TEST =======")

            pin = int(input("Enter BCM GPIO pin: "))
            speed = float(input("Enter speed (-1.0 to 1.0): "))
            duration = float(input("Enter run time (seconds): "))

            if not -1.0 <= speed <= 1.0:
                print("Error: Speed must be between -1.0 and 1.0.")
                continue

            if duration < 0:
                print("Error: Time cannot be negative.")
                continue

            # Initialize servo
            servo = ContinuousServoManager(
                servoPin=pin
            )

            print(f"\nServo connected to GPIO {pin}")
            print(f"Setting speed to {speed}")

            # Start servo
            servo.setSpeed(speed)

            print(f"Running for {duration} seconds...")

            time.sleep(duration)

            # Stop servo
            print("\nStopping servo...")
            servo.stop()

            # Release GPIO
            servo.close()
            servo = None

            print("Servo stopped and released.")

            again = input("\nTest another movement? (y/n): ").lower()

            if again != 'y':
                break

    except KeyboardInterrupt:
        print("\nTest interrupted.")

    finally:
        if servo is not None:
            servo.close()

        print("Servo test exited.")


if __name__ == "__main__":
    main()
