#pragma once

#include <WString.h>
#include <list>


namespace LOS::LOG
{
    extern std::list<String> _LogEntries;

    constexpr unsigned int LOG_CAPACITY = 128;

    void log(char * const message);
    void log(String message);
}