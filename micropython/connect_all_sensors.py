from machine import ADC, Pin
from time import sleep, ticks_ms, ticks_diff
import dht

# ==================================================
# Smart Watering System - Connect All Sensors
# ==================================================
# This is the full connection file.
# Use the test files first, then use this file when every component works.
#
# Components connected:
# - Soil moisture sensor
# - DHT11/DHT22 temperature and humidity sensor
# - Relay module
# - Mini water pump
# - LED dry-soil warning

# Pin map. Keep this the same as the test files.
SOIL_SENSOR_PIN = 34
DHT_PIN = 27
RELAY_PIN = 26
LED_PIN = 25

# Change this to False if your relay turns ON when GPIO is HIGH.
RELAY_ACTIVE_LOW = True

# Change to "DHT11" if your sensor is DHT11.
DHT_SENSOR_TYPE = "DHT22"

# Soil calibration values.
# Adjust after reading raw values from tests/test_soil_sensor.py.
DRY_RAW_VALUE = 3200
WET_RAW_VALUE = 1300

# Watering control.
MOISTURE_THRESHOLD = 45
MOISTURE_STOP_MARGIN = 8
WATERING_TIME_MS = 8000
READ_DELAY_SECONDS = 2

soil_sensor = ADC(Pin(SOIL_SENSOR_PIN))
soil_sensor.atten(ADC.ATTN_11DB)
soil_sensor.width(ADC.WIDTH_12BIT)

led = Pin(LED_PIN, Pin.OUT)
relay = Pin(RELAY_PIN, Pin.OUT)

if DHT_SENSOR_TYPE == "DHT11":
    dht_sensor = dht.DHT11(Pin(DHT_PIN))
else:
    dht_sensor = dht.DHT22(Pin(DHT_PIN))

pump_running = False
pump_started_at = 0


def moisture_percent_from_raw(raw_value):
    percent = (raw_value - DRY_RAW_VALUE) * 100 / (WET_RAW_VALUE - DRY_RAW_VALUE)
    if percent < 0:
        return 0
    if percent > 100:
        return 100
    return int(percent)


def set_pump(on):
    global pump_running, pump_started_at

    pump_running = on
    pump_started_at = ticks_ms() if on else 0

    if RELAY_ACTIVE_LOW:
        relay.value(0 if on else 1)
    else:
        relay.value(1 if on else 0)


def read_soil_sensor():
    raw = soil_sensor.read()
    percent = moisture_percent_from_raw(raw)
    return raw, percent


def read_dht_sensor():
    try:
        dht_sensor.measure()
        return dht_sensor.temperature(), dht_sensor.humidity(), True
    except OSError:
        return None, None, False


def update_led(moisture_percent):
    led.value(1 if moisture_percent < MOISTURE_THRESHOLD else 0)


def update_pump(moisture_percent):
    if not pump_running and moisture_percent < MOISTURE_THRESHOLD:
        set_pump(True)
        print("Soil is dry -> pump ON")

    if pump_running:
        time_finished = ticks_diff(ticks_ms(), pump_started_at) >= WATERING_TIME_MS
        soil_wet_enough = moisture_percent >= MOISTURE_THRESHOLD + MOISTURE_STOP_MARGIN

        if time_finished or soil_wet_enough:
            set_pump(False)
            print("Pump OFF")


def print_system_status(raw, moisture, temperature, humidity, dht_ok):
    print("Soil raw:", raw, end=" | ")
    print("Moisture:", str(moisture) + "%", end=" | ")
    print("DHT OK:", dht_ok, end=" | ")
    print("Temp:", temperature, "C", end=" | ")
    print("Humidity:", humidity, "%", end=" | ")
    print("LED:", "ON" if moisture < MOISTURE_THRESHOLD else "OFF", end=" | ")
    print("Pump:", "ON" if pump_running else "OFF")


def main():
    print("Smart Watering System connected")
    print("Soil GPIO:", SOIL_SENSOR_PIN)
    print("DHT GPIO:", DHT_PIN)
    print("Relay GPIO:", RELAY_PIN)
    print("LED GPIO:", LED_PIN)

    set_pump(False)
    led.value(0)

    while True:
        soil_raw, soil_percent = read_soil_sensor()
        temperature, humidity, dht_ok = read_dht_sensor()

        update_led(soil_percent)
        update_pump(soil_percent)
        print_system_status(soil_raw, soil_percent, temperature, humidity, dht_ok)

        sleep(READ_DELAY_SECONDS)


main()
