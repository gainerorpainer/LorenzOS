#include "_info.h"

#include <ArduinoJson.h>

#include "los.h"

String LOS::Info::getInfoJson()
{
    String result{};

    JsonDocument doc{};
    doc["hostname"] = _Storage.WifiConfig.HostName.asStr();

    serializeJson(doc, result);
    return result;
}