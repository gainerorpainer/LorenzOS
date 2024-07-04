/// @brief Turns /* _CODEGENERATED_TYPE */ into json
/// @param in the /* _CODEGENERATED_TYPE */ to serialze
/// @param out will be cleared and written to
/// @return the length of the string
int serialize(/* _CODEGENERATED_QUALIFIED_TYPE */ const &in, String &out)
{
    // reset buffer just in case
    out.clear();
    JsonDocument doc{};

    /* _CODEGENERATED_WRITE */

    return serializeJson(doc, out);
}

/// @brief Attempts to parse /* _CODEGENERATED_TYPE */ from json
/// @param in the string to parse
/// @param out unchanged or if true is returned, the parsed data
/// @return true if successful
bool tryParse(char const *in, /* _CODEGENERATED_QUALIFIED_TYPE */ &out)
{
    JsonDocument doc{};
    DeserializationError const error = deserializeJson(doc, in);
    if (error)
        return false;

    /* _CODEGENERATED_READ */

    return true;
}