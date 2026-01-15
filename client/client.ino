#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include "Client.h"

#define MAX_LED_STRIPS 5
/* ===== WIFI CONFIG ===== */
const char* ssid     = "nimbus_wifi";
const char* password = "12345678";

#define IN1  D1
#define IN2  D2
#define ENA  D3

void ledOn() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(ENA, HIGH);
}

void ledOff() {
  digitalWrite(ENA, LOW);
}


/* ===== UDP TARGET ===== */
const char* udpAddress = "192.168.137.1";   // Target IP
const uint16_t udpPort = 8080;
uint8_t ledMask;               // Target port

WiFiUDP udp;
LedStrip *ledstrips[MAX_LED_STRIPS];
CRGB leds[NUM_LEDS_IN_EACH_STRIP * MAX_LED_STRIPS];

void decodeLedMaskandSetLED(uint8_t mask) {
  for (uint8_t i = 0; i < MAX_LED_STRIPS; i++) {

    bool ledOn = mask & (1 << i);
    ledOn ? ledstrips[i] -> powerON(): ledstrips[i] -> powerOFF();
    
    Serial.print("LED ");
    Serial.print(i+1);
    Serial.print(": ");
    Serial.println(ledOn ? "ON" : "OFF");
  }
  FastLED.show();
  Serial.println("----------------------------");
}

/* ===== SETUP ===== */

void setup() {
  Serial.begin(115200);
  delay(100);

  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  /* Wait for connection */
  wh
  ile (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected");
  Serial.print("ESP IP address: ");
  Serial.println(WiFi.localIP());

  /* Start UDP */
  udp.begin(udpPort);
  Serial.println("UDP started");

  udp.beginPacket(udpAddress, udpPort);
  udp.write(node_id);
  udp.endPacket();
  Serial.println("Node id sent");

  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENA, OUTPUT);

  // LED OFF initially
  digitalWrite(ENA, LOW);
  // FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS_IN_EACH_STRIP * MAX_LED_STRIPS);
  // FastLED.setBrightness(200);
}

/* ===== LOOP ===== */
void loop() {
  int packet_size = udp.parsePacket();
  if (packet_size){
    udp.read(&ledMask, 1);
    decodeLedMaskandSetLED(ledMask);
  }
}
