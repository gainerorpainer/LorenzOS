#pragma once

#include <ArduinoJson.h>

/* _CODEGENERATED_INCLUDES */

namespace codegen::Parameters
{
    /// @brief Turns parameters into json
    /// @param input the parameters to serialze
    /// @param buffer will be cleared and written to
    /// @return the length of the string
    template <typename T>
    static inline int serialize(T const &in, String &out)
    {
        // reset buffer just in case
        out.clear();
        JsonDocument doc{};

        /* _CODEGENERATED_WRITE */

        return serializeJson(doc, out);
    }

    /// @brief Attempts to parse as json
    /// @param input the string to parse
    /// @param output unchanged or if true is returned, the parsed data
    /// @return true if successful
    template <typename T>
    static inline bool tryParse(char const *in, T &out)
    {
        JsonDocument doc{};
        DeserializationError const error = deserializeJson(doc, in);
        if (error)
            return false;

        /* _CODEGENERATED_READ */

        return true;
    }
}
