from machine import Pin
from time import sleep

# Test relay and mini pump only.
# Expected wiring:
# Relay IN -> ESP32 GPIO26
# Relay VCC -> 5V or relay module required VCC
# Relay GND -> ESP32 GND
# Pump uses external power through relay contacts.
#
# Warning: do not power the pump directly from ESP32.

RELAY_PIN = 26
RELAY_ACTIVE_LOW = True

relay = Pin(RELAY_PIN, Pin.OUT)


def set_relay(on):
    if RELAY_ACTIVE_LOW:
        relay.value(0 if on else 1)
    else:
        relay.value(1 if on else 0)


print("Relay/pump test started")
print("Pump will turn ON for 2 seconds, then OFF for 3 seconds.")

set_relay(False)
sleep(2)

while True:
    set_relay(True)
    print("Relay ON / Pump ON")
    sleep(2)

    set_relay(False)
    print("Relay OFF / Pump OFF")
    sleep(3)
