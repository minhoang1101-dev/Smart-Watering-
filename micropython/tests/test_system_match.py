from machine import ADC, Pin
from time import sleep, ticks_ms, ticks_diff
import dht

# Quick full-system compatibility test.
# This checks whether every component responds on the same pins used by main.py.

SOIL_SENSOR_PIN = 34
DHT_PIN = 27
RELAY_PIN = 26
LED_PIN = 25

DRY_RAW_VALUE = 3200
WET_RAW_VALUE = 1300
MOISTURE_THRESHOLD = 45
RELAY_ACTIVE_LOW = True

soil_sensor = ADC(Pin(SOIL_SENSOR_PIN))
soil_sensor.atten(ADC.ATTN_11DB)
soil_sensor.width(ADC.WIDTH_12BIT)

dht_sensor = dht.DHT22(Pin(DHT_PIN))
relay = Pin(RELAY_PIN, Pin.OUT)
led = Pin(LED_PIN, Pin.OUT)


def moisture_percent_from_raw(raw_value):
    percent = (raw_value - DRY_RAW_VALUE) * 100 / (WET_RAW_VALUE - DRY_RAW_VALUE)
    if percent < 0:
        return 0
    if percent > 100:
        return 100
    return int(percent)


def set_pump(on):
    if RELAY_ACTIVE_LOW:
        relay.value(0 if on else 1)
    else:
        relay.value(1 if on else 0)


def read_dht():
    try:
        dht_sensor.measure()
        return dht_sensor.temperature(), dht_sensor.humidity(), True
    except OSError:
        return None, None, False


print("Smart Watering System match test started")
print("This test reads soil + DHT, controls LED, and briefly pulses relay.")

set_pump(False)
led.value(0)

last_relay_test = ticks_ms()

while True:
    raw = soil_sensor.read()
    moisture = moisture_percent_from_raw(raw)
    temperature, humidity, dht_ok = read_dht()

    led.value(1 if moisture < MOISTURE_THRESHOLD else 0)

    if ticks_diff(ticks_ms(), last_relay_test) > 10000:
        print("Relay pulse test: ON for 1 second")
        set_pump(True)
        sleep(1)
        set_pump(False)
        last_relay_test = ticks_ms()

    print("Soil raw:", raw, end=" | ")
    print("Moisture:", str(moisture) + "%", end=" | ")
    print("DHT OK:", dht_ok, end=" | ")
    print("Temp:", temperature, "C", end=" | ")
    print("Humidity:", humidity, "%", end=" | ")
    print("LED:", "ON" if moisture < MOISTURE_THRESHOLD else "OFF")

    sleep(2)
