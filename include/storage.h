#pragma once

#include <EEPROM.h>
#include <CRC.h>

#include "structstr.h"

namespace LOS::Storage
{
    struct WifiConfig_t
    {
        StructStr_t<64> SSID{};
        StructStr_t<64> Password{};
        StructStr_t<24> HostName{};
    };

    struct PermanentData_t
    {
        char __parameter_data[FLASH_SECTOR_SIZE - (sizeof(uint8_t) + sizeof(WifiConfig_t) + sizeof(uint8_t))];
        uint8_t ParametersCRC;

        WifiConfig_t WifiConfig;
        uint8 WifiCRC;
    };
    static_assert(sizeof(PermanentData_t) == FLASH_SECTOR_SIZE);
    static_assert(offsetof(PermanentData_t, WifiCRC) == FLASH_SECTOR_SIZE - 1);

    class StorageHandler
    {
    private:
        PermanentData_t Data;

        template <typename T>
        static inline uint8_t getCrc(T const &input)
        {
            return calcCRC8(reinterpret_cast<uint8_t const *>(&input), sizeof(T));
        }

    public:
        WifiConfig_t &WifiConfig = Data.WifiConfig;

        /// @brief Initializes the storage by loading the data from eprom
        /// @param data Target to load data into
        /// @return If data loaded from eeprom has valid crc
        /// @remark If loading fails, default creates parameters and stores them into eprom
        StorageHandler()
        {
            Serial.println("Loading EEPROM data...");

            EEPROM.begin(sizeof(PermanentData_t));
            EEPROM.get(0, Data);

            if (getCrc(Data.WifiConfig) != Data.WifiCRC)
            {
                Serial.println("WifiConfig CRC err, defaults have been restored");
                // load default WifiConfig and store into eprom
                WifiConfig = WifiConfig_t{};
                storeToEEprom();
            }

            Serial.println("Wifi Config:");
            Serial.println("\tSSID: " + Data.WifiConfig.SSID.asStr());
            Serial.println("\tPW: " + Data.WifiConfig.Password.asStr());
            Serial.println("\tHostname: " + Data.WifiConfig.HostName.asStr());
        }

        template <typename PARAMETER_T>
        bool getParameters(PARAMETER_T &out)
        {
            static_assert(sizeof(PARAMETER_T) <= sizeof(PermanentData_t::__parameter_data));

            // validate parameters
            if (getCrc(Data.__parameter_data) != Data.ParametersCRC)
            {
                Serial.println("Parameters CRC err, defaults have been restored");
                // load default parameters and store into eprom
                setParameters(PARAMETER_T{});
                storeToEEprom();
                return false;
            }

            std::memcpy(&out, Data.__parameter_data, sizeof(PARAMETER_T));
            return true;
        }

        template <typename PARAMETER_T>
        void setParameters(PARAMETER_T const &in)
        {
            static_assert(sizeof(PARAMETER_T) <= sizeof(PermanentData_t::__parameter_data));

            std::memcpy(Data.__parameter_data, &in, sizeof(PARAMETER_T));
        }

        /// @brief Save parameters to permanent storage
        /// @remark Refreshes CRC for data
        void storeToEEprom()
        {
            // refresh crc
            Data.ParametersCRC = getCrc(Data.__parameter_data);
            Data.WifiCRC = getCrc(Data.WifiConfig);

            EEPROM.put(0, Data);
            EEPROM.commit();
        }
    };
}