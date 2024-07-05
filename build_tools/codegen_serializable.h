#pragma once

#include <ArduinoJson.h>

/* _CODEGENERATED_INCLUDES */

namespace codegen::Serializable
{
    /* _CODEGENERATED_PLACEHOLDER BEGIN */
    /// @brief Turns parameters into json
    /// @param in the parameters to serialze
    /// @param out will be cleared and written to
    /// @return the length of the string
    template <typename T>
    int serialize(T const &in, String &out)
    {
        return 0;
    }

    /// @brief Attempts to parse as json
    /// @param in the string to parse
    /// @param out unchanged or if true is returned, the parsed data
    /// @return true if successful
    template <typename T>
    bool tryParse(char const *in, T &out)
    {
        return false;
    }
    /* _CODEGENERATED_PLACEHOLDER END */
    /* _CODEGENERATED_FRAGMENTS */
}
