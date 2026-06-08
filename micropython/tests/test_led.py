from machine import Pin
from time import sleep

# Test dry-soil warning LED only.
# Expected wiring:
# ESP32 GPIO25 -> 220 ohm resistor -> LED anode (+)
# LED cathode (-) -> GND

LED_PIN = 25
led = Pin(LED_PIN, Pin.OUT)

print("LED test started")

while True:
    led.value(1)
    print("LED ON")
    sleep(1)

    led.value(0)
    print("LED OFF")
    sleep(1)
