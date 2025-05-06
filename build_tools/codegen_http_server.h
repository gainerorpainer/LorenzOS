#pragma once

#include <WString.h>

#include <los.h>

/* _CODEGENERATED_INCLUDES */

namespace codegen::Http_Server
{
    static inline void setup()
    {
        // GET /version
        LOS::_HttpServer.on("/version", []()
                            { LOS::_HttpServer.send(200, "text/plain", String{/* _CODEGENERATED_VERSIONSTR */}); });

        // GET /os
        LOS::_HttpServer.on("/os", []()
                            { LOS::_HttpServer.send(200, "application/json", LOS::Info::getInfoJson()); });

        // GET /log
        LOS::_HttpServer.on("/log", []()
                            { LOS::_HttpServer.send(200, "application/json", LOS::Info::getLog()); });

        /* USER CALLBACKS */
        /* _CODEGENERATED_CALLBACKS */
    }
}
