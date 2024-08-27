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

        /* _CODEGENERATED_CALLBACKS */
    }
}
