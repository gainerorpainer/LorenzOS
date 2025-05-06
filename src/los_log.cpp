#include "los_log.h"

namespace LOS::LOG
{
    std::list<String> _LogEntries = {};

    void log(char *const message)
    {
        log(String{message});
    }

    void log(String message)
    {
        if (_LogEntries.size() == LOG_CAPACITY)
            _LogEntries.pop_back();

        _LogEntries.push_front(message);
    }
}