// Arduino script for wifi button

// Libs
#include <ESP8266WiFi.h>

// Wifi settings
const char* ssid = "";
const char* password = "";

// Server settings
const uint16_t port = 5623;
const char* host = "10.0.0.191";
WiFiClient client;

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

  // Set screen
  client.print("route lcd_device display Remote test");
  while(client.available()){
    String line = client.readStringUntil('\n');
    Serial.println(line);
  }

  delay(5000);

  client.print("route lcd_device shutdown");
  while(client.available()){
    String line = client.readStringUntil('\n');
    Serial.println(line);
  }

  Serial.println("Routed all requests, closing socket.");
  client.stop();
}

void loop() {}
