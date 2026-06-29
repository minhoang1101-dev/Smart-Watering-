#include <DHT.h>

#define DHT_PIN 4
#define DHTTYPE DHT11

#define SOIL_PIN 34

#define RELAY_PIN 26

#define DRY_LED_PIN 25
#define PUMP_LED_PIN 33

#define SOIL_THRESHOLD 2500

DHT dht(DHT_PIN, DHTTYPE);

void setup() {

  Serial.begin(115200);

  dht.begin();

  pinMode(RELAY_PIN, OUTPUT);
  pinMode(DRY_LED_PIN, OUTPUT);
  pinMode(PUMP_LED_PIN, OUTPUT);

  digitalWrite(RELAY_PIN, LOW);
}

void loop() {

  float temp = dht.readTemperature();
  float hum = dht.readHumidity();

  int soilValue = analogRead(SOIL_PIN);

  Serial.println("==============");
  Serial.print("Temp: ");
  Serial.println(temp);

  Serial.print("Humidity: ");
  Serial.println(hum);

  Serial.print("Soil: ");
  Serial.println(soilValue);

  if (soilValue > SOIL_THRESHOLD) {

    digitalWrite(RELAY_PIN, HIGH);

    digitalWrite(DRY_LED_PIN, HIGH);
    digitalWrite(PUMP_LED_PIN, HIGH);

    Serial.println("PUMP ON");
  }
  else {

    digitalWrite(RELAY_PIN, LOW);

    digitalWrite(DRY_LED_PIN, LOW);
    digitalWrite(PUMP_LED_PIN, LOW);

    Serial.println("PUMP OFF");
  }

  delay(2000);
}