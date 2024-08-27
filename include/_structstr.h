#pragma once

#include <cstring>

#include <array>

namespace LOS
{
    template <unsigned int STRLEN>
    struct StructStr_t
    {
        std::array<char, STRLEN> Data;
        char __terminator = '\0';

        explicit StructStr_t(char const *from = nullptr)
        {
            if (!from)
            {
                Data[0] = '\0';
                return;
            }

            // copy over and soft terminate if necessary (trims off excess string length)
            std::size_t const otherStrlen = std::strlen(from);
            std::memcpy(Data.begin(), from, std::min(otherStrlen, STRLEN));
            if (otherStrlen < STRLEN)
                Data[otherStrlen] = '\0';
        }

        StructStr_t &operator=(const String &other)
        {
            // copy over and soft terminate if necessary (trims off excess string length)
            std::memcpy(Data.begin(), other.begin(), std::min(other.length(), STRLEN));
            if (other.length() < STRLEN)
                Data[other.length()] = '\0';
            return *this;
        }

        String asStr()
        {
            // is zero terminated by design
            return String{Data.begin()};
        }

        char *c_str()
        {
            // is zero terminated by design
            return Data.begin();
        }

        bool isEmpty()
        {
            return Data.front() == '\0';
        }
    };

    static_assert(sizeof(StructStr_t<64>) == 64 + 1);
}