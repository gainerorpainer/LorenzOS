/// @brief Turns /* CODEGENERATED_TYPE */ into json
/// @param in the /* CODEGENERATED_TYPE */ to serialze
/// @param out will be cleared and written to
/// @return the length of the string
template <>
static inline int serialize(/* CODEGENERATED_TYPE */ const &in, String &out)
{
    // reset buffer just in case
    out.clear();
    JsonDocument doc{};

    /* _CODEGENERATED_WRITE */

    return serializeJson(doc, out);
}

/// @brief Attempts to parse /* CODEGENERATED_TYPE */ as json
/// @param in the string to parse
/// @param out unchanged or if true is returned, the parsed data
/// @return true if successful
template <>
static inline bool tryParse(char const *in, /* CODEGENERATED_TYPE */ &out)
{
    JsonDocument doc{};
    DeserializationError const error = deserializeJson(doc, in);
    if (error)
        return false;

    /* _CODEGENERATED_READ */

    return true;
}