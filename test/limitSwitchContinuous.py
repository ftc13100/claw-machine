
import RPi.GPIO as GPIO
import time
from datetime import datetime

# Raspberry Pi 3B GPIO pin mapping
# Format: Physical pin : BCM GPIO

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

# Reverse mapping: BCM GPIO -> Physical pin
GPIO_TO_PHYSICAL = {
    gpio: physical
    for physical, gpio in PIN_MAP.items()
}

def pin_triggered(channel):
    physical_pin = GPIO_TO_PHYSICAL[channel]

    timestamp = datetime.now().strftime("%H:%M:%S")

    print(
        f"[{timestamp}] LIMIT SWITCH ACTIVATED! "
        f"Physical Pin: {physical_pin} | "
        f"GPIO (BCM): {channel}"
    )


def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    print("--------------------------------------")
    print(" Raspberry Pi 3B GPIO Limit Monitor")
    print("--------------------------------------")

    print("\nConfiguring GPIO pins with pull-ups...\n")

    # Configure every available GPIO pin
    for physical_pin, gpio_pin in PIN_MAP.items():

        GPIO.setup(
            gpio_pin,
            GPIO.IN,
            pull_up_down=GPIO.PUD_UP
        )

        # Limit switches trigger when input goes LOW
        GPIO.add_event_detect(
            gpio_pin,
            GPIO.FALLING,
            callback=pin_triggered,
            bouncetime=200
        )

        print(
            f"Physical Pin {physical_pin:2} "
            f"| GPIO {gpio_pin:2} READY"
        )

    print("\n--------------------------------------")
    print("MONITORING ALL GPIO PINS")
    print("Activate a limit switch to trigger.")
    print("Press CTRL+C to exit.")
    print("--------------------------------------\n")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping GPIO monitor...")

    finally:
        GPIO.cleanup()
        print("GPIO pins cleaned up.")


if __name__ == "__main__":
    main()
