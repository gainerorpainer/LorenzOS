#include "los.h"

#include <cmath>

#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <ArduinoOTA.h>

#include <CycleLimit.h>
#include <WifiSetup.h>

#include "pwm.h"

namespace LOS
{
    using Time_t = decltype(millis());

    // static externs
    int _NumWifiReconnects = 0;
    ESP8266WebServer _HttpServer{80};
    Storage::StorageHandler _Storage{};

    // static publics
    WiFiUDP NtpUDP{};
    NTPClient TimeClient{NtpUDP, "pool.ntp.org", 0, 1000 * 60 * 60}; // NO timezone, 1h update interval
    // Central European Time (Berlin)
    Timezone CET(TimeChangeRule{
                     // Central European Summer Time
                     "CEST", Last, Sun, Mar, 2, 120},
                 // Central European Standard Time
                 TimeChangeRule{"CET ", Last, Sun, Oct, 3, 60});
    WifiSetup::SerialSetup SerialWifiSetup{};

    bool waitWifiConnected(Time_t timeOutMs = (Time_t)-1)
    {
        Serial.print("Wait for Wifi");
        auto const startOfCycle = millis();
        while (WiFi.status() != WL_CONNECTED)
        {
            digitalWrite(LED_BUILTIN, LOW);
            delay(500); // this is important to yield for the watchdog
            digitalWrite(LED_BUILTIN, HIGH);
            Serial.print(".");

            if ((millis() - startOfCycle) > timeOutMs)
            {
                Serial.println();
                return false;
            }
        }

        Serial.println();
        return true;
    }

    void setup()
    {
        // Initialize the LED_BUILTIN pin as an output
        pinMode(LED_BUILTIN, OUTPUT);

        // activate Serial
        Serial.begin(115200);
        Serial.println();

        Serial.println("Storage values:");
        Serial.printf("\tSSID: %s\n", _Storage.WifiConfig.SSID.c_str());
        Serial.printf("\tPW: %s\n", _Storage.WifiConfig.Password.c_str());
        Serial.printf("\tHostname: %s\n", _Storage.WifiConfig.HostName.c_str());

        // wifi setup
        WiFi.mode(WIFI_STA);
        WiFi.persistent(false);
        if (!_Storage.WifiConfig.HostName.isEmpty())
            WiFi.hostname(_Storage.WifiConfig.HostName.c_str());
        WiFi.begin(_Storage.WifiConfig.SSID.c_str(), _Storage.WifiConfig.Password.c_str());
        if (!waitWifiConnected(10000))
            Serial.println("Could not connect to wifi, time will not be available!");
        Serial.print("IP address: ");
        Serial.println(WiFi.localIP());

        // setup ota updates
        ArduinoOTA.onStart([]()
                           {
                      String type = ArduinoOTA.getCommand() == U_FLASH ? "sketch" : "filesystem";
                      Serial.println("Start updating " + type); });
        ArduinoOTA.onEnd([]()
                         { Serial.println("\nEnd"); });
        ArduinoOTA.onProgress([](unsigned int progress, unsigned int total)
                              { Serial.printf("Progress: %u%%\r", (progress / (total / 100))); });
        ArduinoOTA.onError([](ota_error_t error)
                           {
      Serial.printf("Error[%u]: ", error);
      if (error == OTA_AUTH_ERROR) Serial.println("Auth Failed");
      else if (error == OTA_BEGIN_ERROR) Serial.println("Begin Failed");
      else if (error == OTA_CONNECT_ERROR) Serial.println("Connect Failed");
      else if (error == OTA_RECEIVE_ERROR) Serial.println("Receive Failed");
      else if (error == OTA_END_ERROR) Serial.println("End Failed"); });
        ArduinoOTA.setPassword("sjalw8589slxcmcxyie2980tnsdas");
        ArduinoOTA.begin(false); // do not use mdns

        // 404
        _HttpServer.onNotFound([]()
                               { _HttpServer.send(404, "text/plain", "Not Found"); });
        // logging
        _HttpServer.addHook([](const String &method, const String &url, WiFiClient *client, ESP8266WebServer::ContentTypeFunction contentType)
                            { Serial.printf("HTML %s %s\n", method.c_str(), url.c_str());
                  return ESP8266WebServer::CLIENT_REQUEST_CAN_CONTINUE; });
        _HttpServer.begin();

        // ntp time client
        TimeClient.begin();
    }

    void wifiReconnectCycle()
    {
        static bool isConnected = false;

        if (WiFi.status() == WL_CONNECTED)
        {
            isConnected = true;
            return;
        }

        // only count up if previously connected
        if (isConnected)
        {
            _NumWifiReconnects += 1;
            isConnected = false;
        }

        WiFi.reconnect();
        waitWifiConnected(5000); // do not wait longer than 5000ms!
    }

    /// @brief LOOP
    void loop()
    {
        // blink
        digitalWrite(LED_BUILTIN, HIGH);

        // handle connected services
        if (WiFi.status() == WL_CONNECTED)
        {
            _HttpServer.handleClient();
            ArduinoOTA.handle();
            TimeClient.update();
        }

        // handle io in "realtime"
        static WifiSetup::WifiConfig wifiConfig{.SSID = _Storage.WifiConfig.SSID.asStr(), .Password = _Storage.WifiConfig.Password.asStr(), .Hostname = _Storage.WifiConfig.HostName.asStr()};
        if (SerialWifiSetup.checkInput(wifiConfig))
        {
            // copy over to permanent storage
            _Storage.WifiConfig.SSID = wifiConfig.SSID;
            _Storage.WifiConfig.Password = wifiConfig.Password;
            if (!wifiConfig.Hostname.isEmpty())
                _Storage.WifiConfig.HostName = wifiConfig.Hostname;
            _Storage.storeToEEprom();

            // apply changes to wifi directly
            WiFi.disconnect();
            if (!wifiConfig.Hostname.isEmpty())
                WiFi.hostname(wifiConfig.Hostname.c_str());
            WiFi.begin(wifiConfig.SSID, wifiConfig.Password);
        }

        // check wifi status every 30s
        static CycleLimit::CycleLimit cycleLimiterWifi{CYCLE_WIFI_MS};
        if (cycleLimiterWifi.IsCycleCooledDown())
            wifiReconnectCycle();

        // give alive status each 5s
        static CycleLimit::CycleLimit aliveCheckCycle{CYCLE_ALIVE_CHECK_MS};
        if (aliveCheckCycle.IsCycleCooledDown())
            // printouts
            Serial.printf("alive\n");

        digitalWrite(LED_BUILTIN, LOW);
    }

    tmElements_t getLocalTime()
    {
        tmElements_t localTime;
        breakTime(CET.toLocal(TimeClient.getEpochTime()), localTime);
        return localTime;
    }
}
