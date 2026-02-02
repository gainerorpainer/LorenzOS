/// @brief Attempts to parse /* _CODEGENERATED_TYPE */ from json
/// @param in the string to parse
/// @param out unchanged or if true is returned, the parsed data
/// @return true if successful
static inline bool tryParse(char const *in, /* _CODEGENERATED_QUALIFIED_TYPE */ &out)
{
    JsonDocument doc;
    DeserializationError const error = deserializeJson(doc, in);
    if (error)
        return false;

    /* _CODEGENERATED_READ */

    // user extension code, if any
    /* _CODEGENERATED_EXTENSION_READ */

    return true;
}