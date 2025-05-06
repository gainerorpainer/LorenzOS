#pragma once

#include <ESP8266WebServer.h>
#include <NTPClient.h>
#include <Timezone.h>

#include "_storage.h"
#include "_info.h"

namespace LOS
{
    /// @brief binds to a counter that increments each time the wifi disconnects
    extern int _NumWifiReconnects;

    /// @brief Binds to the LOS http server
    extern ESP8266WebServer _HttpServer;

    /// @brief Binds to the LOS storage handler
    extern Storage::StorageHandler _Storage;

    /// @brief cycle time for alive check
    constexpr int CYCLE_ALIVE_CHECK_MS = 5000;

    /// @brief cycle time for less time critical things
    constexpr int CYCLE_WIFI_MS = 30000;

    /// @brief call this function in your setup() function
    void setup();

    /// @brief call this function in your loop() function
    void loop();

    /// @brief Access the time retrieved from ntp
    /// @return the time as local time
    tmElements_t getLocalTime();

    /// @brief Access the time retrieved from ntp
    /// @return the utc time as unix timestamp
    unsigned long getUTC();

    /// @brief Access the time offset in hours between current local time and utc
    /// @return offset between local time and utc in hours
    double getLocalTimeOffset();
}
