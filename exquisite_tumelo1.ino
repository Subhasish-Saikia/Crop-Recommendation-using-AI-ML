// Pin Definitions
#define SOIL_MOISTURE_PIN A0
#define PH_SENSOR_PIN A1
#define MQ135_PIN A2
#define LDR_PIN A3
#define RAIN_SENSOR_PIN A4
#define DHT_PIN A5
#define DHT_TYPE DHT11

void setup() {
  Serial.begin(9600);
  delay(10000);
  Serial.println("Starting sensor readings...");
}

void loop() {
  // Read soil moisture
  int soilMoistureValue = analogRead(SOIL_MOISTURE_PIN);
  
  // Read pH value (simulated)
  int phRaw = analogRead(PH_SENSOR_PIN);
  float voltage = phRaw * (5.0 / 1023.0);
  float pHValue = 7 + ((2.5 - voltage) / 0.18); // Approximate calibration

  // Read air quality
  int airQuality = analogRead(MQ135_PIN);

  // Read light intensity
  int lightValue = analogRead(LDR_PIN);

  // Read rain sensor
  int rainValue = analogRead(RAIN_SENSOR_PIN); // Can use digitalRead for digital module

  // Get the voltage reading from the TMP36
  int reading = analogRead(DHT_PIN);

  // Convert that reading into voltage
  // Replace 5.0 with 3.3, if you are using a 3.3V Arduino
  float voltage2 = reading * (5.0 / 1024.0);

  // Convert the voltage into the temperature in Celsius
  float temperatureC = (voltage2 - 0.5) * 100;
  
  // Print sensor data to serial monitor
  Serial.println("----- Sensor Readings -----");
  Serial.print("Soil Moisture: "); Serial.println(soilMoistureValue);
  Serial.print("pH Value: "); Serial.println(pHValue);
  Serial.print("Air Quality (MQ135): "); Serial.println(airQuality);
  Serial.print("Light Intensity (LDR): "); Serial.println(lightValue);
  Serial.print("Rain Sensor: "); Serial.println(rainValue);
  Serial.print("Temperature: ");
  Serial.print(temperatureC);
  Serial.print("\xC2\xB0"); // shows degree symbol
  Serial.print("C  |  ");

   float temperatureF = (temperatureC * 9.0 / 5.0) + 32.0;
  Serial.print(temperatureF);
  Serial.print("\xC2\xB0"); // shows degree symbol
  Serial.println("F");
  Serial.println("---------------------------\n");
  
  delay(10000); // Read every 10 seconds
}