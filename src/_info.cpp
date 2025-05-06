#include "_info.h"

#include <ArduinoJson.h>

#include "los.h"
#include "los_log.h"

namespace LOS::Info
{

    String getInfoJson()
    {
        JsonDocument doc;
        doc["hostname"] = _Storage.WifiConfig.HostName.asStr();

        String result;
        serializeJson(doc, result);
        return result;
    }

    String getLog()
    {
        JsonDocument doc;

        for (auto const & item : LOS::LOG::_LogEntries)
            doc.add(item);
        
        String result;
        serializeJson(doc, result);
        return result;
    }
}
