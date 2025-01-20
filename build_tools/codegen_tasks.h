#pragma once

#include <CycleLimit.h>

/* _CODEGENERATED_INCLUDES */

namespace codegen::Tasks
{
    static inline void call_once()
    {
        /* _CODEGENERATED_ONCE */
    }

    static inline void loop()
    {
        CycleLimit::Time_t const now = millis();
        
        /* _CODEGENERATED_LOOP */
    }
}
