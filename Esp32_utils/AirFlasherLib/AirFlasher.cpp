#include "AirFlasherLib.h"

AirFlasher::AirFlasher(const char *ssid, const char *password, const char *firmwareUrl)
{
    _ssid = ssid;
    _password = password;
    _firmwareUrl = firmwareUrl;
}

void AirFlasher::begin()
{
    WiFi.begin(_ssid, _password);
    Serial.print("Connecting to WiFi");

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }

    Serial.println();
    Serial.print("WiFi connected successfully! IP: ");
    Serial.println(WiFi.localIP());
    Serial.print("wiFi name : ");
    Serial.println(_ssid);
    
}

void AirFlasher::handle()
{
    if (WiFi.status() == WL_CONNECTED)
    {
        checkAndUpdate();
    }
    else
    {
        Serial.println("WiFi not connected. Skipping OTA check.");
    }
}

void AirFlasher::checkAndUpdate()
{
    HTTPClient http;
    http.begin(_firmwareUrl);
    int httpCode = http.GET();

    if (httpCode == HTTP_CODE_OK)
    {
        int contentLength = http.getSize();

        bool canBegin = Update.begin(contentLength);

        if (canBegin)
        {
            Serial.println("Starting OTA update...");

            WiFiClient &client = http.getStream();
            size_t written = Update.writeStream(client);

            if (written == contentLength)
            {
                Serial.println("OTA Written: " + String(written) + " bytes");
            }
            else
            {
                Serial.println("OTA Failed. Written only: " + String(written) + "/" + String(contentLength) + " bytes");
            }

            if (Update.end())
            {
                if (Update.isFinished())
                {
                    Serial.println("OTA update complete. Rebooting...");
                    ESP.restart();
                }
                else
                {
                    Serial.println("OTA not finished.");
                }
            }
            else
            {
                Serial.println("Error in OTA: " + String(Update.getError()));
            }
        }
        else
        {
            Serial.println("Not enough space for OTA update.");
        }
    }
    else if (httpCode == HTTP_CODE_NO_CONTENT)
    {
        Serial.println("No new firmware available.");
    }
    else
    {
        Serial.printf("Firmware check failed. HTTP code: %d\n", httpCode);
    }

    http.end();
}
