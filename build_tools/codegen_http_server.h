#pragma once

#include <WString.h>

#include <los.h>

#include "codegen_html.h"

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

        // GET /
        LOS::_HttpServer.on("/", []()
                            { LOS::_HttpServer.send(200, "text/html", STATIC_HTML_MAINPAGE, sizeof(STATIC_HTML_MAINPAGE)); });
        // GET /favicon.ico
        LOS::_HttpServer.on("/favicon.ico", []()
                            { LOS::_HttpServer.send(200, "image/x-icon", STATIC_HTML_FAVICON_CONTENT, sizeof(STATIC_HTML_FAVICON_CONTENT)); });

        /* USER CALLBACKS */
        /* _CODEGENERATED_CALLBACKS */
    }
}
