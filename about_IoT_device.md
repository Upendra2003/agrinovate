virtual device link  https://wokwi.com/projects/406218366821925889

![alt text](image.png)



// Program used in device

// Pin setup
const int moisturePin = 32;
const int phPin = 33;
const int nPin = 34;
const int pPin = 35;
const int kPin = 27;
const int tempPin = 14;  // Analog Temperature Sensor connected to GPIO 14
const int ledPin = 26;

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
}

void loop() {
  // Simulate temperature readings with an accuracy of ±0.5°C
  int rawValue = analogRead(tempPin);
  float temperature = (rawValue / 4095.0) * 100 + random(-5, 5) / 10.0; // Adding ±0.5°C fluctuation
  
  // Simulate soil moisture readings with ±3% accuracy
  int soilMoisture = random(400, 700);  // Random soil moisture value
  
  // Simulate pH readings with 95% accuracy
  float soilPH = random(950, 1000) / 10.0;  // Random soil pH value between 9.5 and 10.0
  
  // Simulate NPK readings with ±5% accuracy
  int soilN = random(95, 105);  // Nitrogen with ±5% accuracy
  int soilP = random(95, 105);  // Phosphorus with ±5% accuracy
  int soilK = random(95, 105);  // Potassium with ±5% accuracy

  // Print sensor values to the serial monitor
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.print("°C, Soil Moisture: ");
  Serial.print(soilMoisture);
  Serial.print(", Soil pH: ");
  Serial.print(soilPH);
  Serial.print(", Nitrogen: ");
  Serial.print(soilN);
  Serial.print(", Phosphorus: ");
  Serial.print(soilP);
  Serial.print(", Potassium: ");
  Serial.println(soilK);

  // LED control based on soil moisture level
  if (soilMoisture < 500) {
    digitalWrite(ledPin, HIGH);  // Turn on LED if moisture is low
    delay(500);  // Keep LED on for 500ms
    digitalWrite(ledPin, LOW);   // Turn off LED
    delay(500);  // Keep LED off for 500ms
  } else {
    digitalWrite(ledPin, LOW);   // Turn off LED if moisture is sufficient
  }

  delay(2000);  // Wait for 2 seconds before next loop
}



