#pragma once

#include <stdexcept>

#include <ArduinoJson.h>

/* _CODEGENERATED_INCLUDES */

namespace codegen::Serializable
{
    /// @brief Turns parameters into json
    /// @param in the parameters to serialze
    /// @param out will be cleared and written to
    /// @return the length of the string
    [[noreturn]]
    template <typename T>
    static inline int serialize(T const &in, String &out)
    {
        throw std::bad_function_call{"not implemented"};
    }

    /// @brief Attempts to parse as json
    /// @param in the string to parse
    /// @param out unchanged or if true is returned, the parsed data
    /// @return true if successful
    template <typename T>
    static inline bool tryParse(char const *in, T &out)
    {
        throw std::bad_function_call{"not implemented"};
    }

    /* _CODEGENERATED_FRAGMENTS */
}
