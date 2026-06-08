from machine import ADC, Pin
from time import sleep, ticks_ms, ticks_diff
import dht

# Smart Watering System - ESP32 MicroPython version
# Components:
# - ESP32 board
# - Soil moisture sensor
# - Relay module
# - Mini water pump
# - DHT11 or DHT22 sensor
# - LED + 220 ohm resistor

# Pin configuration
SOIL_SENSOR_PIN = 34
DHT_PIN = 27
RELAY_PIN = 26
LED_PIN = 25

# Soil sensor calibration.
# Update these values after testing your real sensor.
DRY_RAW_VALUE = 3200
WET_RAW_VALUE = 1300

# Watering settings
MOISTURE_THRESHOLD = 45
MOISTURE_STOP_MARGIN = 8
WATERING_TIME_MS = 8000

# Many relay modules are active LOW.
RELAY_ACTIVE_LOW = True

soil_sensor = ADC(Pin(SOIL_SENSOR_PIN))
soil_sensor.atten(ADC.ATTN_11DB)
soil_sensor.width(ADC.WIDTH_12BIT)

relay = Pin(RELAY_PIN, Pin.OUT)
led = Pin(LED_PIN, Pin.OUT)

# Use dht.DHT11(...) if your module is DHT11.
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


def read_dht():
    try:
        dht_sensor.measure()
        return dht_sensor.temperature(), dht_sensor.humidity()
    except OSError:
        return None, None


def print_status(raw, moisture, temperature, humidity):
    print("Soil raw:", raw, end=" | ")
    print("Moisture:", str(moisture) + "%", end=" | ")
    print("Temp:", temperature, "C", end=" | ")
    print("Humidity:", humidity, "%", end=" | ")
    print("Pump:", "ON" if pump_running else "OFF")


def main():
    print("Smart Watering System started")
    set_pump(False)
    led.value(0)

    while True:
        raw = soil_sensor.read()
        moisture = moisture_percent_from_raw(raw)
        temperature, humidity = read_dht()

        led.value(1 if moisture < MOISTURE_THRESHOLD else 0)

        if not pump_running and moisture < MOISTURE_THRESHOLD:
            set_pump(True)
            print("Soil is dry. Pump ON.")

        if pump_running:
            time_finished = ticks_diff(ticks_ms(), pump_started_at) >= WATERING_TIME_MS
            soil_wet_enough = moisture >= MOISTURE_THRESHOLD + MOISTURE_STOP_MARGIN

            if time_finished or soil_wet_enough:
                set_pump(False)
                print("Pump OFF.")

        print_status(raw, moisture, temperature, humidity)
        sleep(2)


main()
