from time import sleep

# ==================================================
# Smart Watering System - No Sensor Diagnostic
# ==================================================
# Run this file on your computer with normal Python.
# It does not need ESP32, soil sensor, DHT sensor, relay, LED, or pump.
#
# Purpose:
# - Check if the watering logic makes sense.
# - Simulate dry soil, wet soil, DHT readings, LED, and pump status.

MOISTURE_THRESHOLD = 45
MOISTURE_STOP_MARGIN = 8
WATERING_TIME_STEPS = 4


class FakeHardware:
    def __init__(self):
        self.led_on = False
        self.pump_on = False

    def set_led(self, on):
        self.led_on = on

    def set_pump(self, on):
        self.pump_on = on


def fake_sensor_data():
    return [
        {"soil": 72, "temp": 27.0, "humidity": 61, "label": "wet soil"},
        {"soil": 51, "temp": 27.4, "humidity": 60, "label": "normal soil"},
        {"soil": 34, "temp": 28.1, "humidity": 58, "label": "dry soil"},
        {"soil": 28, "temp": 28.3, "humidity": 57, "label": "very dry soil"},
        {"soil": 39, "temp": 28.0, "humidity": 59, "label": "still dry"},
        {"soil": 55, "temp": 27.6, "humidity": 62, "label": "watered enough"},
        {"soil": 63, "temp": 27.2, "humidity": 64, "label": "stable wet soil"},
    ]


def run_diagnostic():
    hardware = FakeHardware()
    pump_steps_left = 0

    print("Smart Watering no-sensor diagnostic started")
    print("Threshold:", str(MOISTURE_THRESHOLD) + "%")
    print("-" * 72)

    for step, data in enumerate(fake_sensor_data(), start=1):
        soil = data["soil"]
        temp = data["temp"]
        humidity = data["humidity"]

        hardware.set_led(soil < MOISTURE_THRESHOLD)

        if not hardware.pump_on and soil < MOISTURE_THRESHOLD:
            hardware.set_pump(True)
            pump_steps_left = WATERING_TIME_STEPS

        if hardware.pump_on:
            pump_steps_left -= 1
            soil_wet_enough = soil >= MOISTURE_THRESHOLD + MOISTURE_STOP_MARGIN
            time_finished = pump_steps_left <= 0

            if soil_wet_enough or time_finished:
                hardware.set_pump(False)

        print(
            "Step:",
            step,
            "| Case:",
            data["label"],
            "| Soil:",
            str(soil) + "%",
            "| Temp:",
            str(temp) + "C",
            "| Humidity:",
            str(humidity) + "%",
            "| LED:",
            "ON" if hardware.led_on else "OFF",
            "| Pump:",
            "ON" if hardware.pump_on else "OFF",
        )

        sleep(0.5)

    print("-" * 72)
    print("Diagnostic finished")


if __name__ == "__main__":
    run_diagnostic()
