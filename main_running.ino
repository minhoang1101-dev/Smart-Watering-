#define BLYNK_TEMPLATE_ID "TMPL6q-3ZwnN0"
#define BLYNK_TEMPLATE_NAME "SMART WATERING"
#define BLYNK_AUTH_TOKEN "TODXljKq45ZCiDMdDOqy_sHATVrh3yLm"

#include <WiFi.h>
#include <WiFiClient.h>
#include <BlynkSimpleEsp32.h>
#include <DHT.h>

// =====================
// WIFI
// =====================
char ssid[] = "12345";
char pass[] = "iamatomic";

// =====================
// PIN CONFIG
// =====================
#define DHTPIN 19
#define DHTTYPE DHT11

#define SOIL_PIN 34

#define RELAY_PIN 26
#define DRY_LED   25
#define PUMP_LED  33

// =====================
// SOIL CALIBRATION
// =====================
#define SOIL_DRY 4095
#define SOIL_WET 1200

DHT dht(DHTPIN, DHTTYPE);
BlynkTimer timer;

bool pumpState = false;

// =====================
// SENSOR UPDATE
// =====================

void sendData()
{
  float temp = dht.readTemperature();
  float hum  = dht.readHumidity();

  int soilRaw = analogRead(SOIL_PIN);

  int soilPercent = map(
    soilRaw,
    SOIL_DRY,
    SOIL_WET,
    0,
    100
  );

  soilPercent = constrain(
    soilPercent,
    0,
    100
  );

  // =====================
  // DEMO LOGIC
  // =====================

  if (soilPercent > 60)
  {
    // Đất ẩm

    digitalWrite(DRY_LED, HIGH);    // LED đỏ ON
    digitalWrite(PUMP_LED, LOW);    // LED vàng OFF

    digitalWrite(RELAY_PIN, HIGH);  // Relay OFF

    pumpState = false;
  }
  else
  {
    // Đất khô

    digitalWrite(DRY_LED, LOW);     // LED đỏ OFF
    digitalWrite(PUMP_LED, HIGH);   // LED vàng ON

    digitalWrite(RELAY_PIN, LOW);   // Relay ON

    pumpState = true;
  }

  // =====================
  // BLYNK UPDATE
  // =====================

  if (!isnan(temp))
    Blynk.virtualWrite(V0, temp);

  if (!isnan(hum))
    Blynk.virtualWrite(V1, hum);

  Blynk.virtualWrite(V2, soilPercent);
  Blynk.virtualWrite(V3, pumpState);

  // =====================
  // SERIAL DEBUG
  // =====================

  Serial.println("======================");

  Serial.print("Temperature: ");
  Serial.println(temp);

  Serial.print("Humidity: ");
  Serial.println(hum);

  Serial.print("Soil Raw: ");
  Serial.println(soilRaw);

  Serial.print("Soil %: ");
  Serial.println(soilPercent);

  Serial.print("Pump State: ");
  Serial.println(pumpState);
}

// =====================
// SETUP
// =====================

void setup()
{
  Serial.begin(115200);
  delay(2000);

  Serial.println("BOOT OK");

  pinMode(RELAY_PIN, OUTPUT);
  pinMode(DRY_LED, OUTPUT);
  pinMode(PUMP_LED, OUTPUT);

  digitalWrite(RELAY_PIN, HIGH);
  digitalWrite(DRY_LED, LOW);
  digitalWrite(PUMP_LED, LOW);

  dht.begin();

  Serial.println("Connecting WiFi + Blynk...");

  Blynk.begin(
    BLYNK_AUTH_TOKEN,
    ssid,
    pass
  );

  Serial.println("Blynk Connected!");

  // Update mỗi 2 giây
  timer.setInterval(2000L, sendData);

  sendData();

  Serial.println("SMART WATERING STARTED");
}

// =====================
// LOOP
// =====================

void loop()
{
  Blynk.run();
  timer.run();
}