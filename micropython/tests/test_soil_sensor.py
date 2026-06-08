from machine import ADC, Pin
from time import sleep

# Test soil moisture sensor only.
# Expected wiring:
# Soil sensor AO/SIG -> ESP32 GPIO34
# Soil sensor VCC -> 3.3V
# Soil sensor GND -> GND

SOIL_SENSOR_PIN = 34
DRY_RAW_VALUE = 3200
WET_RAW_VALUE = 1300

soil_sensor = ADC(Pin(SOIL_SENSOR_PIN))
soil_sensor.atten(ADC.ATTN_11DB)
soil_sensor.width(ADC.WIDTH_12BIT)


def moisture_percent_from_raw(raw_value):
    percent = (raw_value - DRY_RAW_VALUE) * 100 / (WET_RAW_VALUE - DRY_RAW_VALUE)
    if percent < 0:
        return 0
    if percent > 100:
        return 100
    return int(percent)


print("Soil moisture sensor test started")
print("Put the sensor in dry air, then wet soil/water, and compare raw values.")

while True:
    raw = soil_sensor.read()
    moisture = moisture_percent_from_raw(raw)

    print("Raw:", raw, "| Moisture:", str(moisture) + "%")
    sleep(1)
