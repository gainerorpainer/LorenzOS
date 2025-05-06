#pragma once

#include <WString.h>

namespace LOS::Info
{
    /// @brief Collects info about the OS
    /// @return JSON string
    String getInfoJson();

    /// @brief Retrieves the log entries
    /// @return JSON string
    String getLog();
}