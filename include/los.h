#pragma once

#include <ESP8266WebServer.h>
#include <NTPClient.h>
#include <Timezone.h>

#include "storage.h"

namespace LOS
{
    extern int _NumWifiReconnects;
    extern ESP8266WebServer _HttpServer;
    extern Storage::StorageHandler _Storage;

    /// @brief cycle time for alive check
    constexpr int CYCLE_ALIVE_CHECK_MS = 5000;

    /// @brief cycle time for less time critical things
    constexpr int CYCLE_WIFI_MS = 30000;

    void setup();

    void loop();

    tmElements_t getLocalTime();
}
