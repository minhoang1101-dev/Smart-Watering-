#include <DHT.h>

// =========================
// Smart Watering ESP32 Code
// =========================
// This source code reads real sensors, controls a relay pump,
// shows dry-soil warning with an LED, and prints status to Serial Monitor.

// Pin configuration.
const int SOIL_SENSOR_PIN = 34;
const int DHT_PIN = 27;
const int RELAY_PIN = 26;
const int LED_PIN = 25;

// Change to DHT11 if you buy a DHT11 sensor.
#define DHT_TYPE DHT22
DHT dht(DHT_PIN, DHT_TYPE);

// Soil moisture calibration.
// Update these after testing your real soil moisture sensor.
const int DRY_RAW_VALUE = 3200;
const int WET_RAW_VALUE = 1300;

// Many relay modules are active LOW.
// If your relay turns on when GPIO is HIGH, set this to false.
const bool RELAY_ACTIVE_LOW = true;

// Watering settings.
int moistureThreshold = 45;
int wateringDurationSeconds = 8;
const int MOISTURE_STOP_MARGIN = 8;

// Runtime state.
int soilRaw = 0;
int soilPercent = 0;
float temperatureC = NAN;
float humidityPercent = NAN;
bool automaticMode = true;
bool pumpRunning = false;
unsigned long pumpStartedAt = 0;

int moisturePercentFromRaw(int rawValue) {
  int percent = map(rawValue, DRY_RAW_VALUE, WET_RAW_VALUE, 0, 100);
  return constrain(percent, 0, 100);
}

void setPump(bool on) {
  pumpRunning = on;
  pumpStartedAt = on ? millis() : 0;

  if (RELAY_ACTIVE_LOW) {
    digitalWrite(RELAY_PIN, on ? LOW : HIGH);
  } else {
    digitalWrite(RELAY_PIN, on ? HIGH : LOW);
  }
}

void readSensors() {
  soilRaw = analogRead(SOIL_SENSOR_PIN);
  soilPercent = moisturePercentFromRaw(soilRaw);

  float newHumidity = dht.readHumidity();
  float newTemperature = dht.readTemperature();

  if (!isnan(newHumidity)) {
    humidityPercent = newHumidity;
  }

  if (!isnan(newTemperature)) {
    temperatureC = newTemperature;
  }
}

void updateDryWarningLed() {
  digitalWrite(LED_PIN, soilPercent < moistureThreshold ? HIGH : LOW);
}

void updateAutomaticWatering() {
  if (!automaticMode) {
    return;
  }

  if (!pumpRunning && soilPercent < moistureThreshold) {
    setPump(true);
  }

  if (pumpRunning) {
    bool timeFinished = millis() - pumpStartedAt >= wateringDurationSeconds * 1000UL;
    bool soilWetEnough = soilPercent >= moistureThreshold + MOISTURE_STOP_MARGIN;

    if (timeFinished || soilWetEnough) {
      setPump(false);
    }
  }
}

void printStatus() {
  Serial.print("Soil raw: ");
  Serial.print(soilRaw);
  Serial.print(" | Soil moisture: ");
  Serial.print(soilPercent);
  Serial.print("% | Temp: ");
  Serial.print(temperatureC);
  Serial.print(" C | Humidity: ");
  Serial.print(humidityPercent);
  Serial.print("% | Pump: ");
  Serial.println(pumpRunning ? "ON" : "OFF");
}

void setup() {
  Serial.begin(115200);

  pinMode(SOIL_SENSOR_PIN, INPUT);
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);

  dht.begin();
  setPump(false);
  digitalWrite(LED_PIN, LOW);

  Serial.println("Smart Watering System started");
}

void loop() {
  readSensors();
  updateDryWarningLed();
  updateAutomaticWatering();
  printStatus();

  delay(2000);
}
