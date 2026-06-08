# Smart Watering MicroPython Tests

These files test each component separately before running `main.py`.

## Files

- `test_soil_sensor.py`: checks soil moisture raw value and percentage.
- `test_dht_sensor.py`: checks temperature and humidity readings.
- `test_led.py`: blinks the dry-soil warning LED.
- `test_relay_pump.py`: turns the relay/pump on and off.
- `test_system_match.py`: checks all pins together with the same configuration as `main.py`.

## Pin Map

| Component | ESP32 Pin |
| --- | --- |
| Soil moisture sensor AO/SIG | GPIO34 |
| DHT11/DHT22 data | GPIO27 |
| Relay IN | GPIO26 |
| LED | GPIO25 |

## How To Use

Upload one test file at a time to the ESP32 as `main.py`, then reset the board and read the serial output.

After every component works, upload `../main.py` as the final program.
