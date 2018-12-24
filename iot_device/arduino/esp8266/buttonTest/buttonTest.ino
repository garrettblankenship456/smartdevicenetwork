// Arduino script for wifi button

// Libs
#include <ESP8266WiFi.h>

// Wifi settings
const char* ssid = "Tina-2.4";
const char* password = "family5!";

// Server settings
const uint16_t port = 5623;
const char* host = "10.0.0.191";
WiFiClient client;

// Public variables
String lastWrote = "";

// Functions
void setID(){
  client.print("iot_remote");

  delay(500);
  while(client.available()){
    String line = client.readStringUntil('\n');
    Serial.println(line);
  }
}

// Main code
void setup() {
  Serial.begin(115200);

  // Connect to wifi
  WiFi.begin(ssid, password);
  while(WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.println("...");
  }

  Serial.print("Wifi connected with IP: ");
  Serial.println(WiFi.localIP());

  // Connect to IOT server and set up the ID
  Serial.println("Connecting to IOT");
  while(!client.connect(host, port)){
    Serial.println("Failed to connected to IOT server");

    delay(1000);
  }
  
  // Wait for handshake
  delay(500);
  while(client.available()){
    String line = client.readStringUntil('\n');
    Serial.println(line);
  }

  setID();
  Serial.println("Connected to IOT and ID has been set!");
}

bool seen = false;
void loop() {
  // Get input
  if(Serial.available()){
    lastWrote = Serial.readStringUntil('\n');
    Serial.println(lastWrote);

    seen = false;
  }

  // Send it to the server
  client.print(lastWrote);

  // Receive any data back
  delay(500);
  String line = "";
  while(client.available() && seen == false){
    line = client.readStringUntil('\n');
    Serial.println(line);
    seen = true;
  }
}
