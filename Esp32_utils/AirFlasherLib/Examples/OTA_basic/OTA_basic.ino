#include <AirFlasherLib.h>

// Replace these with your actual values
const char* ssid = "Your_SSID";
const char* password = "Your_PASS";
const char* firmwareURL = "http://your-server.com/firmware.bin";

AirFlasher ota(ssid, password, firmwareURL);

void setup() {
  Serial.begin(115200);
  ota.begin();

  // Optional: check update once at startup
  ota.handle();
}

void loop() {
  // Optional: check for update periodically (e.g., every hour or day)
  // ota.handle();
  
  // Your regular loop code here
}
