
import RPi.GPIO as GPIO
from datetime import datetime

# Physical pin : BCM GPIO
PIN_MAP = {
    7: 4,
    11: 17,
    13: 27,
    15: 22,
    19: 10,
    21: 9,
    23: 11,
    29: 5,
    31: 6,
    33: 13,
    35: 19,
    37: 26,

    8: 14,
    10: 15,
    12: 18,
    16: 23,
    18: 24,
    22: 25,
    24: 8,
    26: 7,
    32: 12,
    36: 16,
    38: 20,
    40: 21
}


def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    try:
        print("\nRaspberry Pi 3B - Limit Switch Scan")
        print("------------------------------------")

        # Configure all pins as inputs with pull-ups
        for physical_pin, gpio_pin in PIN_MAP.items():
            GPIO.setup(
                gpio_pin,
                GPIO.IN,
                pull_up_down=GPIO.PUD_UP
            )

        # Allow inputs to stabilize
        import time
        time.sleep(0.05)

        print("\nScanning GPIO pins...\n")

        active_switches = []

        # Read each GPIO exactly once
        for physical_pin, gpio_pin in PIN_MAP.items():

            if GPIO.input(gpio_pin) == GPIO.LOW:
                active_switches.append(
                    (physical_pin, gpio_pin)
                )

        # Print results
        if active_switches:
            print("ACTIVE LIMIT SWITCHES:")
            print("----------------------")

            for physical_pin, gpio_pin in active_switches:
                print(
                    f"Physical Pin: {physical_pin} | "
                    f"GPIO (BCM): {gpio_pin} | ACTIVE"
                )

            print(f"\nTotal active switches: {len(active_switches)}")

        else:
            print("No active limit switches detected.")

        print("\nScan complete.")

    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
