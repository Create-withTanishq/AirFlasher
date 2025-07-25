#ifndef AIRFLASHERLIB_H
#define AIRFLASHERLIB_H

#include <WiFi.h>
#include <HTTPClient.h>
#include <Update.h>

class AirFlasher {
  public:
    AirFlasher(const char* ssid, const char* password, const char* firmwareUrl);
    void begin();
    void handle();  // Call repeatedly in loop()

  private:
    const char* _ssid;
    const char* _password;
    const char* _firmwareUrl;
    void checkAndUpdate();
};

#endif
