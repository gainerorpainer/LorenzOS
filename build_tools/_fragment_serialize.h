/// @brief Turns /* _CODEGENERATED_TYPE */ into json
/// @param in the /* _CODEGENERATED_TYPE */ to serialze
/// @param out will be cleared and written to
/// @return the length of the string
int serialize(/* _CODEGENERATED_QUALIFIED_TYPE */ const &in, String &out)
{
    // reset buffer just in case
    out.clear();
    JsonDocument doc;
    
    /* _CODEGENERATED_DEBUGINFO */

    /* _CODEGENERATED_WRITE */

    // user extension code, if any
    /* _CODEGENERATED_EXTENSION_WRITE */

    return serializeJson(doc, out);
}