from machine import Pin
from time import sleep
import dht

# Test DHT11 or DHT22 sensor only.
# Expected wiring:
# DHT data -> ESP32 GPIO27
# DHT VCC -> 3.3V
# DHT GND -> GND

DHT_PIN = 27

# Change DHT22 to DHT11 if your sensor is DHT11.
dht_sensor = dht.DHT22(Pin(DHT_PIN))

print("DHT sensor test started")

while True:
    try:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()

        print("Temperature:", temperature, "C | Humidity:", humidity, "%")
    except OSError as error:
        print("DHT read failed:", error)

    sleep(2)
